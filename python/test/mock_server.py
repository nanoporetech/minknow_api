"""Test grpc server for minknow_api"""

import importlib.resources
import inspect
import logging
import os
from concurrent import futures
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional, Tuple, Sequence, Iterator
from minknow_api.tools.compatibility_helpers import read_binary_resource

import grpc

from minknow_api import (
    instance_pb2,
    instance_pb2_grpc,
    manager_pb2,
    manager_pb2_grpc,
)

LOGGER = logging.getLogger(__name__)


def load_server_certs() -> List[Tuple[bytes, bytes]]:
    """
    Load the test server certificates.

    You shouldn't typically need to call this if you are making use of `Server`.
    """
    key = read_binary_resource("test_certs", "localhost.key")
    cert = read_binary_resource("test_certs", "localhost.crt")
    return [(key, cert)]


def load_test_ca() -> bytes:
    """
    Load the CA for the test server certificates.

    Useful if you need to construct your own gRPC credentials for some reason.
    """
    return read_binary_resource("test_certs", "ca.crt")


@contextmanager
def set_trusted_ca() -> Iterator[Path]:
    """
    Set the MINKNOW_TRUSTED_CA environment variable to trust the certificates provided
    by `load_server_certs`.

    Intended to be used as a context manager:

    >>> with set_trusted_ca():
    >>>     make_connection_to_test_server()

    You shouldn't typically need to call this if you are making use of `Server`.
    """

    def open_ca_cert():
        try:
            return importlib.resources.as_file(
                importlib.resources.files("test_certs") / "ca.crt"
            )
        except AttributeError:
            return importlib.resources.path("test_certs", "ca.crt")

    with open_ca_cert() as ca_path:
        saved_env = os.environ.get("MINKNOW_TRUSTED_CA")
        os.environ["MINKNOW_TRUSTED_CA"] = str(ca_path)
        yield ca_path
        if saved_env is not None:
            os.environ["MINKNOW_TRUSTED_CA"] = saved_env
        else:
            del os.environ["MINKNOW_TRUSTED_CA"]


class InstanceServicer(instance_pb2_grpc.InstanceServiceServicer):
    """
    The most basic implementation of InstanceServicerServicer.

    get_version_info() must be implemented for minknow_api.Connection() to work.
    """

    def get_version_info(
        self,
        _request: instance_pb2.GetVersionInfoRequest,
        _context: grpc.ServicerContext,
    ) -> instance_pb2.GetVersionInfoResponse:
        """Find the version information for the instance"""
        return instance_pb2.GetVersionInfoResponse(
            minknow=instance_pb2.GetVersionInfoResponse.MinknowVersion(
                major=4, minor=0, patch=0, full="4.0.0"
            )
        )


class ManagerServicer(manager_pb2_grpc.ManagerServiceServicer):
    """
    A basic implementation of ManagerServiceServicer.

    ``local_authentication_token_path`` because it is called by the code that constructs
    the default gRPC channel credentials in `minknow_api`. By default it returns an
    empty string, which will ensure minknow_api won't look for a file.

    ``get_version_info`` is implemented because `minknow_api.manager.Manager()` calls it
    in its ``__init__()``.

    ``flow_cell_positions`` and ``basecaller_api`` are implemented because they are
    useful for tests that use the manager as just an entry point to other services.

    Args:
        positions: The starting value of the ``positions`` attribute.
        basecaller_port: The port the basecaller is listening on.

    Attrs:
        positions (List[manager_pb2.FlowCellPosition]): The list of positions that will
            be turned by the ``flow_cell_positions`` RPC.
        local_auth_token_path (str): Override the path reported for the local
            authentication token.
    """

    def __init__(
        self,
        positions: Optional[List[manager_pb2.FlowCellPosition]] = None,
        basecaller_port: int = 0,
    ):
        self.positions = positions if positions else []
        self.local_auth_token_path = ""
        self.basecaller_port = basecaller_port

        self.basecall_configurations = []

    def local_authentication_token_path(
        self,
        request: manager_pb2.LocalAuthenticationTokenPathRequest,
        context: grpc.ServicerContext,
    ) -> manager_pb2.LocalAuthenticationTokenPathResponse:
        return manager_pb2.LocalAuthenticationTokenPathResponse(
            path=self.local_auth_token_path
        )

    def get_version_info(
        self,
        _request: manager_pb2.GetVersionInfoRequest,
        _context: grpc.ServicerContext,
    ) -> instance_pb2.GetVersionInfoResponse:
        """Find the version information for the manager"""
        return instance_pb2.GetVersionInfoResponse(
            minknow=instance_pb2.GetVersionInfoResponse.MinknowVersion(
                major=4, minor=0, patch=0, full="4.0.0"
            )
        )

    def flow_cell_positions(
        self,
        _request: manager_pb2.FlowCellPositionsRequest,
        _context: grpc.ServicerContext,
    ):
        """Find which positions are connected to the host"""
        yield manager_pb2.FlowCellPositionsResponse(
            positions=self.positions, total_count=len(self.positions)
        )

    def basecaller_api(
        self, _request: manager_pb2.BasecallerApiRequest, _context: grpc.ServicerContext
    ) -> manager_pb2.BasecallerApiResponse:
        """The port to connect to the basecaller service on."""
        return manager_pb2.BasecallerApiResponse(secure=self.basecaller_port)

    def find_basecall_configurations(
        self,
        _request: manager_pb2.FindBasecallConfigurationsRequest,
        _context: grpc.ServicerContext,
    ) -> manager_pb2.FindBasecallConfigurationsResponse:
        """Get a list of basecall configurations."""
        return manager_pb2.FindBasecallConfigurationsResponse(
            configurations=self.basecall_configurations
        )


def _add_servicer_to_server(servicer: object, server: grpc.Server):
    """Adds an arbitrary servicer to a grpc server.

    The servicer must ultimately derive from the base servicer in the generated gRPC
    code (eg: minknow_api.manager.ManagerServiceServicer for the manager service).
    """
    # first, find the adder function - we'll assume the base servicer is just below
    # `object` in the class hierarchy
    base_servicer_type = inspect.getmro(type(servicer))[-2]
    pb2_grpc_module = inspect.getmodule(base_servicer_type)
    adder_name = f"add_{base_servicer_type.__name__}_to_server"
    adder = getattr(pb2_grpc_module, adder_name)
    adder(servicer, server)


class Server(object):
    """
    Runs a test gRPC server.

    Args:
        servicers: A list of servicers to add to the server. These should ultimately
            derive from the relevant servicer baseclass (eg:
            minknow_api.manager.ManagerServiceServicer for the manager service).
        interceptors: A list of interceptors to attach to the server.
        client_root_certs: Require clients to connect using a certificate with a root of
            trust in this PEM certificate bundle.

    Attrs:
        server (grpc.Server): The gRPC server.
        port (int): The port the server is listening on.

    The server will use the certificates provided by load_server_certs().

    This can be used as a context manager, like:

    >>> manager_servicer = ManagerServicer()
    >>> with Server([manager_servicer]) as server:
    >>>    manager = minknow_api.manager.Manager(port=server.port)

    The ``MINKNOW_TRUSTED_CA`` environment variable will be set during the ``with``
    block, allowing code from `minknow_api` to trust the TLS connection.
    """

    def __init__(
        self,
        servicers: Sequence[object],
        interceptors: Optional[List[grpc.ServerInterceptor]] = None,
        client_root_certs: Optional[bytes] = None,
    ):
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=2), interceptors=interceptors
        )

        for servicer in servicers:
            _add_servicer_to_server(servicer, self.server)

        server_certs = load_server_certs()
        self.port = self.server.add_secure_port(
            "127.0.0.1:0",
            grpc.ssl_server_credentials(
                server_certs,
                root_certificates=client_root_certs,
                # as of gRPC 1.41.0, you can't configure Python gRPC servers to request,
                # but not require, client certificates - this argument seems to control
                # both actions
                require_client_auth=client_root_certs is not None,
            ),
        )
        logging.debug(
            "gRPC server listening on %s with servicers: %s",
            self.port,
            [type(s) for s in servicers],
        )
        self.server.start()
        logging.debug("gRPC server started")

    def __enter__(self):
        self._trusted_ca = set_trusted_ca()
        self._trusted_ca.__enter__()
        return self

    def __exit__(self, *args):
        self._trusted_ca.__exit__(*args)
        logging.debug("gRPC server stopping")
        self.server.stop(0)
        logging.debug("gRPC server stopped")
