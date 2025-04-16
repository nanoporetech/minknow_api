"""
DEPRECATED.

This was originally intended to provide users of minknow_api with a convenient test
harness for their code. However, it is quite strongly tied to minknow_api's own test
directory structure, and also proved to be too inflexible to use with even the tests for
minknow_api's own example code.

Consider taking inspiration from python/test/mock_server.py in the minknow_api source
repository instead.
"""

import inspect
import logging
import warnings
from concurrent import futures
from pathlib import Path

import grpc
from packaging.version import parse

import minknow_api
from minknow_api import _optional_services, _services, _import_submodule, SubmoduleType

LOGGER = logging.getLogger(__name__)
VERSION = parse(minknow_api.__version__)
# Get major, minor, micro from base_version over using the attrs as this
#   allows us to use older packaging versions
MAJOR, MINOR, MICRO = map(int, VERSION.base_version.split("."))
DEFAULT_SERVER_PORT = 0

found_test_certs_dir = None

warnings.warn(
    "minknow_api.testutils is deprecated and will be removed in a future release",
    DeprecationWarning,
)


def find_test_certs_dir(extra_stack_frames_up=0):
    global found_test_certs_dir
    if not found_test_certs_dir:
        frame = inspect.stack()[1 + extra_stack_frames_up]
        module = inspect.getmodule(frame[0])
        cert_root = Path(module.__file__).parent

        certs_dir = None
        while True:
            certs_dir = cert_root / "test_certs"
            if certs_dir.exists():
                break
            new_cert_root = cert_root.parent
            logging.info("%s %s", new_cert_root, cert_root)
            if new_cert_root == cert_root:
                raise Exception("Failed to find test certificates directory")
            cert_root = new_cert_root

        found_test_certs_dir = certs_dir
    return found_test_certs_dir


def make_secure_grpc_credentials(certs_dir):
    server_credentials = grpc.ssl_server_credentials(
        (
            (
                (certs_dir / "localhost.key").read_bytes(),
                (certs_dir / "localhost.crt").read_bytes(),
            ),
        ),
        (certs_dir / "ca.crt").read_bytes(),
    )
    return server_credentials


class AuthInterceptor(grpc.ServerInterceptor):
    def __init__(self, token, logger):
        self.token = token
        self.logger = logger

    def intercept_service(self, continuation, handler_call_details):
        authenticated = False
        for val in handler_call_details.invocation_metadata:
            if val.key == "test-auth":
                authenticated = True if val.value == self.token else False
                break

        if not authenticated:
            raise RuntimeError("Not authenticated!")

        cont = continuation(handler_call_details)
        return cont


class InstanceService(minknow_api.instance_pb2_grpc.InstanceServiceServicer):
    def get_version_info(self, _request, _context):
        """Find the version information for the instance"""
        return minknow_api.instance_pb2.GetVersionInfoResponse(
            minknow=minknow_api.instance_pb2.GetVersionInfoResponse.MinknowVersion(
                major=MAJOR,
                minor=MINOR,
                patch=MICRO,
                full=minknow_api.__version__,
            )
        )


class MockMinKNOWServer:
    """A MinKNOW server that is compatible with the minknow_api.Connection

    This is a minimal gRPC server that implements all the required methods
    for the minknow_api.Connection class. The server is easily extensible
    using custom service classes and provides an interface for testing code
    that interacts with MinKNOW without it being installed.

    Any documented service in the minknow_api module can be added to the
    server. The custom service should be passed as a keyword argument when
    initialising the server in the format ``{name}_service=MyClass`` where
    ``name`` is a valid minknow service.

    if ``auth_info`` is not None, then it is assumed that the server is
    hosted on a secure port
    """

    def __init__(
        self, port=DEFAULT_SERVER_PORT, certs_path=None, auth_token=None, **kwargs
    ):
        # Logging setup
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
        )
        self.logger = logging.getLogger(__name__)
        self.certs_path = certs_path
        if not self.certs_path:
            self.certs_path = find_test_certs_dir(extra_stack_frames_up=1)

        # Set the server port or get an available port
        self.port = port
        if self.port == 0:
            self.logger.info("Port will be assigned by operating system")

        # Initialise any interceptors
        interceptors = None
        if auth_token:
            interceptor = AuthInterceptor(auth_token, self.logger)
            interceptors = [interceptor]

        # Init the server
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            interceptors=interceptors,
        )

        for service in kwargs:
            # get service name excluding '_service'
            if service.endswith("_service"):
                service = service[: -len("_service")]
            if service in _services.keys():
                self.logger.info(f"Using user defined service for {repr(service)}")
            else:
                self.logger.warning(
                    f"Skipped user defined service {repr(service)}, not recognised"
                )

        # Store kwargs, add 'instance_service' here as it is the
        #   only service/method that minknow.Connection requires
        self.kwargs = kwargs
        if "instance_service" not in self.kwargs:
            self.kwargs["instance_service"] = InstanceService

        # Iterate the services defined in minknow_api._services
        #   adding the base Servicer unless another is specified
        #   via kwargs
        for name, svc in _services.items():
            svc_name = f"{name}_service"
            try:
                svc_module = _import_submodule(name, svc, SubmoduleType.PB2_GRPC)
            except ImportError:
                if name not in _optional_services:
                    raise
            else:
                # There should be only one entry for each service
                for svc_class_name in svc.services:
                    svc_servicer = f"{svc_class_name}Servicer"

                    # Get the user overridden module from kwargs
                    #   or fallback onto the baseclass from grpc
                    module = self.kwargs.get(
                        svc_name,
                        getattr(svc_module, svc_servicer),
                    )

                    # Same as: self.{name}_service = minknow_api.{name}_pb2_grpc.{svc}Servicer
                    #   or uses user defined module()
                    setattr(self, svc_name, module())

                    # Add servicer to server
                    func = f"add_{svc_servicer}_to_server"
                    add_servicer_to_server_func = getattr(svc_module, func)
                    add_servicer_to_server_func(getattr(self, svc_name), self.server)

            grpc_creds = None
            if self.certs_path:
                grpc_creds = make_secure_grpc_credentials(self.certs_path)
            bound = self.server.add_secure_port(f"[::]:{self.port}", grpc_creds)
        if bound == 0:
            raise ConnectionError(f"Could not connect using port {self.port}")
        self.port = bound

        self.logger.info(f"Using port {self.port}")

    def make_channel_credentials(self):
        certs_path = self.__dict__["certs_path"]
        if not certs_path:
            raise Exception("certs_path is not defined")
        return grpc.ssl_channel_credentials((certs_path / "localhost.crt").read_bytes())

    def __enter__(self):
        self.start()
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop(0)

    def __getattr__(self, item):
        """Delegate attribute access to the gRPC server"""
        # Is this a bad idea?
        return getattr(self.server, item)
