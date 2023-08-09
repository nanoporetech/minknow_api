"""
MinKNOW RPC Access
==================

Provides access to MinKNOW via RPC.

This RPC system is gRPC-based. You might want to look at the `gRPC documentation
<http://www.grpc.io/grpc/python/>`_ for more information, but most of the detail is hidden by the
code in this module.

For external systems accessing MinKNOW, start with `minknow_api.manager.Manager` - this will allow
you to access high-level information, and enumerate and access each flow cell position.

The central class for accessing a flow cell position is `Connection`.

The functionality available on a flow cell position is divided into services, covering related units
like controlling the device or managing data acquisition. Each service is available as a property on
a `Connection` object. For each service, the related Protobuf messages are available from
``minknow_api.<service>_service``, or as ``connection.<service>._pb`` (if ``connection`` is a
``Connection`` object).

.. _rpc-services:

Services
--------

The available services are:

acquisition
    Control data acquisition. See `acquisition_service.AcquisitionService` for a description of the
    available methods.
analysis_configuration
    Configure data acquisition. See `analysis_configuration_service.AnalysisConfigurationService`
    for a description of the available methods.
data
    Stream acquisition data. Note that this is for data directly produced during acquisition, rather
    than statistics about acquired data. See `data_service.DataService` for a description of the
    available methods.
device
    Get information about and control the attached device. This useful presents information and
    settings in a device-independent way, so it can be used on PromethIONs as easily as on MinIONs.
    See `device_service.DeviceService` for a description of the available methods.
keystore
    A service for storing and retreiving arbitrary data on the instance. This can be used to
    communicate with other users of the API. See `keystore_service.DeviceService` for a description
    of the available methods.
instance
    Get information about the instance of MinKNOW you are connected to (eg: software version). See
    `instance_service.InstanceService` for a description of the available methods.
log
    Get or produce general informational messages. See `log_service.LogService` for a description of
    the available methods.
minion_device
    MinION-specific device interface. This exposes low-level settings for MinIONs and similar
    devices (eg: GridIONs). See `minion_device_service.MinionDeviceService` for a
    description of the available methods.
protocol
    Control protocol scripts. See `protocol_service.ProtocolService` for a description of the
    available methods.
promethion_device
    PromethION-specific device interface. This exposes low-level settings for PromethIONs. See
    `promethion_device_service.PromethionDeviceService` for a description of the available methods.
run_until
    Get and set criteria, values and updates which relate to stopping an acquisition when certain
    run-until criteria are met.  See run_until_service.RunUntilService for a description of the
    available methods.
statistics
    Get statistics about an acquisition period. Statistics can be streamed live during acquisition,
    or retreived afterwards. See `statistics_service.StatisticsService` for a description of the
    available methods.

Helpers
-------

The `minknow_api.data`, `minknow_api.device` and `minknow_api.manager` modules contain helpers for
working with the services of the same name. See the documentation for those modules for more
information.

"""

import importlib
import json
import logging
import os
import sys
import threading
import warnings
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

import grpc
import pyrfc3339
import pytz

from . import data, manager

from minknow_api.manager import get_local_authentication_token_file

# Try and import from minknow_api_production package
try:
    from minknow_api_production import (
        production_pb2,
        production_pb2_grpc,
        production_service,
    )

    sys.modules["minknow_api.production_service"] = production_service
    sys.modules["minknow_api.production_pb2"] = production_pb2
    sys.modules["minknow_api.production_pb2_grpc"] = production_pb2_grpc
except ImportError:
    pass

#
# Services
#
_services = {
    "acquisition": ["AcquisitionService"],
    "analysis_configuration": ["AnalysisConfigurationService"],
    "data": ["DataService"],
    "device": ["DeviceService"],
    "instance": ["InstanceService"],
    "keystore": ["KeyStoreService"],
    "log": ["LogService"],
    "minion_device": ["MinionDeviceService"],
    "production": ["ProductionService"],
    "promethion_device": ["PromethionDeviceService"],
    "protocol": ["ProtocolService"],
    "run_until": ["RunUntilService"],
    "statistics": ["StatisticsService"],
    "traxion_device": ["TraxionDeviceService"],
}
_optional_services = ["production", "traxion_device"]


#
# Module meta-information
#

__all__ = [svc + "_service" for svc in _services] + [
    "Connection",
    "LocalAuthTokenCredentials",
    "data",
    "device",
    "load_grpc_credentials",
    "grpc_credentials",
    "read_ssl_certificate",
    "manager",
    "post_processing_protocol_connection",
]

try:
    from ._version import __version__
except ImportError:
    __version__ = None


#
# Submodule imports
#

# Convenience imports for each service

for svc in _services:
    try:

        # effectively does `import .{svc}_service as {svc}_service`
        importlib.import_module(".{}_service".format(svc), __name__)
    except ImportError:
        if svc not in _optional_services:
            raise

logger = logging.getLogger(__name__)

#
# Connection helpers
#

GRPC_CHANNEL_OPTIONS = [
    ("grpc.max_send_message_length", 16 * 1024 * 1024),
    ("grpc.max_receive_message_length", 16 * 1024 * 1024),
    ("grpc.http2.min_time_between_pings_ms", 1000),
    (
        "grpc.ssl_target_name_override",
        "localhost",
    ),  # that's what our cert's CN is
]


class LocalAuthTokenCredentials(grpc.AuthMetadataPlugin):
    """Token based auth that gets the token from a known
    location on the local filesystem. So only clients that
    have access to the local filesystem can read the token.

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """

    def __init__(self, local_auth_path):
        super().__init__()
        self.local_auth_path = local_auth_path
        self.lock = threading.Lock()
        self._refresh_local_token()

    def _refresh_local_token(self) -> None:
        with self.lock:
            try:
                with open(self.local_auth_path, "r") as f:
                    token_json = json.load(f)
                    self.token = token_json["token"]
                    # Remove 120 secs from expiry just to ensure a token refresh before the token
                    # actually expires
                    self.expires_at = pyrfc3339.parse(
                        token_json["expires"]
                    ) - timedelta(seconds=120)
                    logger.debug(
                        "Found local auth token %s[...], expires at %s",
                        self.token[:8],
                        token_json["expires"],
                    )
            except Exception as e:
                logger.warning("Local auth token unable to be refreshed: %s", e)
                self.token = None
                self.expires_at = None

    def __call__(self, context, callback):
        metadata = None
        if self.token:
            now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            if now >= self.expires_at:
                self._refresh_local_token()

            metadata = (("local-auth", self.token),)

        callback(metadata, None)


class DeveloperApiTokenCredentials(grpc.AuthMetadataPlugin):
    """Presents a developer API token to MinKNOW that was obtained from the MinKNOW UI.

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, context, callback):
        # it's not really a "local auth" token, but all the tokens share the same
        # namespace so it will work anyway
        metadata = (("local-auth", self.token),)
        callback(metadata, None)


class ProtocolTokenCredentials(grpc.AuthMetadataPlugin):
    """Simple token based auth that assumes that the token
    will last long enough for the duration of the experiment.

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, context, callback):
        metadata = (("protocol-auth", self.token),)
        callback(metadata, None)


def get_protocol_token_credentials(
    environ: Dict[str, str] = os.environ
) -> Optional[grpc.ChannelCredentials]:
    """If running as a protocol in MinKNOW, get the protocol token used to authenticate
    to MinKNOW.

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """
    token = environ.get("PROTOCOL_TOKEN")

    if token:
        return grpc.metadata_call_credentials(ProtocolTokenCredentials(token))
    else:
        logger.debug("No protocol token found")
        return None


def get_local_auth_token_credentials(
    manager_port: Optional[int],
) -> Optional[grpc.ChannelCredentials]:
    """Attempt to get the local authentication token.

    This will return None if local guest mode is not enabled or if MinKNOW is not
    running on the local machine.

    Note that if this returns a token, it can *only* be used to connect to MinKNOW
    running on localhost at the port given by `manager_port` (the default ports of 9501
    or 9502 if `manager_port` is None).

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """
    local_auth_path = get_local_authentication_token_file(port=manager_port)
    logger.debug("Retrieving local token from file: '%s'", local_auth_path)
    if local_auth_path:
        if os.path.exists(local_auth_path):
            return grpc.metadata_call_credentials(
                LocalAuthTokenCredentials(local_auth_path)
            )
        else:
            logger.warn(
                'Local authentication token should be at "%s", '
                + "but that file does not exist",
                local_auth_path,
            )

    return None


def get_developer_api_token_credentials(
    developer_api_token: str,
) -> grpc.ChannelCredentials:
    """Create a channel credentials object for the given developer API token.

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """
    if not isinstance(developer_api_token, str):
        raise Exception(
            "Invalid developer api token, expected str, got %s"
            % developer_api_token.__class__
        )
    return grpc.metadata_call_credentials(
        DeveloperApiTokenCredentials(developer_api_token)
    )


def read_ssl_certificate(environ: Dict[str, str] = os.environ) -> bytes:
    """Get the CA certificate that should be used to verify a TLS connection to MinKNOW.

    If the ``MINKNOW_TRUSTED_CA`` environment variable is set to the path to an
    existing file, its contents will be used. Otherwise, an internal copy of MinKNOW
    Core's default CA will be used.

    You probably want to use `grpc_credentials()` instead. This is mostly a helper for
    that function.
    """
    try:
        with open(environ["MINKNOW_TRUSTED_CA"], "rb") as f:
            return f.read()
    except KeyError:
        pass
    except OSError:
        logger.warning(
            "$MINKNOW_TRUSTED_CA set but failed to read '%s'",
            environ.get("MINKNOW_TRUSTED_CA"),
        )

    try:
        # python 3.7+
        import importlib.resources as importlib_resources
    except ImportError:
        # python 3.5/3.6
        import importlib_resources
    # using the syntax that works with python 3.7
    return importlib_resources.read_binary("minknow_api", "ca.crt")


def _is_localhost(host: str) -> bool:
    # common cases:
    if host == "localhost" or host == "localhost.localdomain":
        return True
    if host == "127.0.0.1" or host == "::1":
        return True

    # It is an IP address?
    # IPv6 addresses in particular have multiple equivalent representations.
    try:
        import ipaddress

        address = ipaddress.ip_address(host)
    except ValueError:
        # it wasn't an ip address
        pass
    else:
        # it was an ip address: is it it the loopback address?
        return address == ipaddress.IPv6Address(
            "::1"
        ) or address == ipaddress.IPv4Address("127.0.0.1")

    # Is it just our own hostname?
    try:
        lowercase_host = host.lower()
        import socket

        if (
            lowercase_host == socket.gethostname().lower()
            or lowercase_host == socket.getfqdn().lower()
        ):
            return True
    except OSError:
        logger.exception(
            'Failed to get hostname (cannot check whether "%s" is localhost)', host
        )

    return False


def _try_client_cert_from_env_vars(
    environ: Dict[str, str] = os.environ
) -> Tuple[Optional[bytes], Optional[bytes]]:
    cert_chain_path = environ.get("MINKNOW_API_CLIENT_CERTIFICATE_CHAIN")
    cert_key_path = environ.get("MINKNOW_API_CLIENT_KEY")
    if cert_chain_path is None or cert_key_path is None:
        if cert_chain_path is not None:
            logger.warn(
                "MINKNOW_API_CLIENT_CERTIFICATE_CHAIN environment variable set "
                "but MINKNOW_API_CLIENT_KEY is not set"
            )
        elif cert_key_path is not None:
            logger.warn(
                "MINKNOW_API_CLIENT_KEY environment variable set "
                "but MINKNOW_API_CLIENT_CERTIFICATE_CHAIN is not set"
            )
        return (None, None)

    try:
        with open(cert_chain_path, "rb") as f:
            cert_chain = f.read()
    except IOError as e:
        logger.warn(
            "Cannot load %s (from MINKNOW_API_CLIENT_CERTIFICATE_CHAIN): %s",
            cert_chain_path,
            e,
        )
        return (None, None)
    try:
        with open(cert_key_path, "rb") as f:
            cert_key = f.read()
    except IOError as e:
        logger.warn(
            "Cannot load %s (from MINKNOW_API_CLIENT_KEY): %s", cert_key_path, e
        )
        return (None, None)

    return (cert_chain, cert_key)


def load_grpc_credentials(
    manager_port: Optional[int] = None,
    developer_api_token: Optional[str] = None,
    host: Optional[str] = None,
    client_certificate_chain: Optional[bytes] = None,
    client_private_key: Optional[bytes] = None,
    _warning_stacklevel: int = 0,
    environ: Dict[str, str] = os.environ,
) -> grpc.ChannelCredentials:
    """Load gRPC credentials.

    Args:
        manager_port: The port the Manager is running on. This is used to find the
            location of the local authentication token.
        developer_api_token: A developer API token obtained from the UI for
            authentication. This is deprecated, and it is recommended to use
            `client_cert` and `client_private_key` instead.
        host: The name of the host being connected to. This is used to decide whether to
            try to use the local authentication token.
        client_cert_chain: The (PEM-encoded) certificate chain linking
            `client_private_key` to a certificate in ``conf/rpc-client-certs`` in the
            MinKNOW installation directory.
        client_private_key: The (PEM-encoded) private key for the first certificate in
            `client_cert_chain`.

    This is the same as `grpc_credentials`, but does not cache the result. You should
    probably be using that function instead.
    """

    if developer_api_token is not None:
        warnings.warn(
            "`developer_api_token` is deprecated",
            DeprecationWarning,
            stacklevel=_warning_stacklevel,
        )

    logger.debug("Reading ssl certificate")
    if (client_certificate_chain is None) != (client_private_key is None):
        raise TypeError(
            "client_cert_chain and client_private_key must either both "
            "be provided, or both be omitted"
        )
    if client_certificate_chain is None:
        client_certificate_chain, client_private_key = _try_client_cert_from_env_vars(
            environ
        )
    ssl_creds = grpc.ssl_channel_credentials(
        root_certificates=read_ssl_certificate(environ),
        private_key=client_private_key,
        certificate_chain=client_certificate_chain,
    )

    # First use developer api token, if supplied:
    call_creds = None
    if developer_api_token is not None:
        logger.debug("Using developer api token")
        call_creds = get_developer_api_token_credentials(developer_api_token)

    # Next try and get a token from the local filesystem if available:
    if not call_creds:
        local_token_override = environ.get("MINKNOW_API_USE_LOCAL_TOKEN")
        if local_token_override is None:
            # (allow host==None for backwards compatiblity)
            try_local_token = host is None or _is_localhost(host)
        elif local_token_override.lower() in ("", "0", "no"):
            try_local_token = False
        else:
            try_local_token = True
        if try_local_token:
            logger.debug("Getting local token")
            call_creds = get_local_auth_token_credentials(manager_port)

    if not call_creds:
        # No local token, so check if there is a token provided from starting as a
        # protocol.
        # NB: We try this *after* the local token because Bream currently needs to talk
        # to the manager (where the protocol token doesn't work) - see CORE-3605 - but
        # this may change in the future.
        logger.debug("Getting protocol token")
        call_creds = get_protocol_token_credentials(environ)

    if call_creds:
        grpc_creds = grpc.composite_channel_credentials(ssl_creds, call_creds)
    else:
        grpc_creds = ssl_creds

    return grpc_creds


_grpc_credentials_cache: Dict[Any, grpc.ChannelCredentials] = dict()


def grpc_credentials(
    manager_port: Optional[int] = None,
    developer_api_token: Optional[str] = None,
    host: Optional[str] = None,
    client_certificate_chain: Optional[bytes] = None,
    client_private_key: Optional[bytes] = None,
    _warning_stacklevel: int = 0,
    environ: Dict[str, str] = os.environ,
) -> grpc.ChannelCredentials:
    """Get a grpc.ChannelCredentials object for connecting to secure versions of MinKNOW"s gRPC
    services.

    Args:
        manager_port: The port the Manager is running on. This is used for caching and
            for finding the location of the local authentication token.
        developer_api_token: A developer API token obtained from the UI for
            authentication. This is deprecated, and it is recommended to use
            `client_cert` and `client_private_key` instead.
        host: The name of the host being connected to. This is used for caching and also
            to decide whether to try to use the local authentication token.
        client_certificate_chain: The (PEM-encoded) certificate chain linking
            `client_private_key` to a certificate in ``conf/rpc-client-certs`` in the
            MinKNOW installation directory.
        client_private_key: The (PEM-encoded) private key for the first certificate in
            `client_cert_chain`.

    Use like:

    >>> import grpc
    >>> channel = grpc.secure_channel("localhost:9502", grpc_credentials())

    If run from the Python embedded in MinKNOW, this will find the correct certificate
    automatically. Otherwise, you may need to set the ``MINKNOW_TRUSTED_CA`` to point to the CA
    certificate used by MinKNOW (which can be found at ``conf/rpc-certs/ca.crt`` in the MinKNOW
    installation).
    """
    cache_key = (
        manager_port,
        developer_api_token,
        host,
        client_certificate_chain,
        client_private_key,
    )

    global _grpc_credentials_cache

    try:
        creds = _grpc_credentials_cache[cache_key]
        logger.debug("Using grpc credentials with cache key: (%s)", cache_key)
        return creds
    except KeyError:
        pass

    creds = load_grpc_credentials(
        manager_port,
        developer_api_token,
        host,
        client_certificate_chain,
        client_private_key,
        _warning_stacklevel=_warning_stacklevel + 1,
        environ=environ,
    )
    _grpc_credentials_cache[cache_key] = creds
    return creds


def clear_credentials_cache() -> None:
    """
    Clears the gRPC credentials cache.

    This can be useful in tests, such as when the manager is being restarted.
    """
    global _grpc_credentials_cache
    _grpc_credentials_cache = dict()


#
# Connection class
#


class Connection(object):
    """A connection to a MinKNOW flow cell sequencing position via RPC.

    The port for a given flow cell position is provided by the manager service. See
    `minknow_api.manager.Manager`.

    Args:
        port: The port to connect to.
        host: The host MinKNOW is running on (defaults to localhost).
        credentials: gRPC credentials to use. If None, then
            minknow_api.grpc_credentials() is called (using the other arguments) to
            obtain credentials.
        developer_api_token: A token obtained from the MinKNOW UI. Will be used to
            authorise to MinKNOW if provided. This is deprecated, and it is recommended
            to use `client_certificate_chain` and `client_private_key` instead. Note: if
            `credentials` is provided, this parameter is ignored.
        client_certificate_chain: The (PEM-encoded) certificate chain linking
            `client_private_key` to a certificate in ``conf/rpc-client-certs`` in
            the MinKNOW installation directory. Note: if `credentials` is provided,
            this parameter is ignored.
        client_private_key: The (PEM-encoded) private key for the first certificate
            in `client_cert_chain`. Note: if `credentials` is provided, this
            parameter is ignored.

    If no port is provided, the MINKNOW_RPC_PORT environment variable will be used
    (MinKNOW sets this when running protocol scripts, for example). If this environment
    variable does not exist (or is not a number), an exception will be raised.

    Each service is available as a property of the same name on the Connection
    object. See :ref:`rpc-services` for a list.

    Given a connection object ``connection``, for each service,
    ``connection.<service>`` is a "service object". This exposes the RPC methods
    for that service in a more convenient form than gRPC's own Python bindings
    do.

    For example, when calling ``start_protocol`` on the ``protocol`` service,
    instead of doing

    >>> protocol_service.start_protocol(
    >>>     protocol_service._pb.StartProtocolMessage(path="my_script"))

    you can do

    >>> connection.protocol.start_protocol(path="my_script")

    Note that you must use keyword arguments - no positional parameters are
    available.

    This "unwrapping" of request messages only happens at one level, however. If
    you want to change the target temperature settings on a MinION, you need to do
    something like

    >>> temp_settings = connection.minion_device._pb.TemperatureRange(min=37.0, max=37.0)
    >>> connection.minion_device.change_settings(
    >>>     temperature_target=temp_settings)
    """

    def __init__(
        self,
        port: Optional[int] = None,
        host: str = "127.0.0.1",
        credentials: Optional[grpc.ChannelCredentials] = None,
        developer_api_token: Optional[str] = None,
        client_certificate_chain: Optional[bytes] = None,
        client_private_key: Optional[bytes] = None,
        environ: Dict[str, str] = os.environ,
    ):
        import time
        import grpc

        self.environ = environ

        self.host = host
        if port is None:
            port = int(self.environ["MINKNOW_RPC_PORT_SECURE"])
        self.port = port

        if credentials is not None:
            if developer_api_token is not None:
                warnings.warn(
                    "`developer_api_token` ignored as `credentials` was provided"
                )
            if client_certificate_chain is not None or client_private_key is not None:
                warnings.warn(
                    "`client_certificate_chain` and `client_private_key` ignored as `credentials` was provided"
                )

        error = None
        retry_count = 5
        for i in range(retry_count):
            if not credentials:
                try:
                    manager_port = int(self.environ["MINKNOW_MANAGER_TEST_PORT"])
                except KeyError:
                    manager_port = None
                credentials = grpc_credentials(
                    manager_port=manager_port,
                    developer_api_token=developer_api_token,
                    host=host,
                    client_certificate_chain=client_certificate_chain,
                    client_private_key=client_private_key,
                    _warning_stacklevel=1,
                    environ=self.environ,
                )

            self.channel = grpc.secure_channel(
                "{}:{}".format(host, port),
                credentials=credentials,
                options=GRPC_CHANNEL_OPTIONS,
            )

            # One entry for each service
            for name, svc_list in _services.items():
                for svc in svc_list:
                    try:
                        # effectively does `self.{name} = {name}_service.{svc}(self.channel)`
                        setattr(
                            self,
                            name,
                            getattr(globals()[name + "_service"], svc)(self.channel),
                        )
                    except KeyError:
                        if name not in _optional_services:
                            raise

            # Ensure channel is ready for communication
            try:
                logger.debug("Calling get_version_info to test connection")
                self.instance.get_version_info()
                error = None
                break
            except grpc.RpcError as e:
                logger.info("Error received from rpc")
                if (
                    e.code() == grpc.StatusCode.INTERNAL
                    and e.details() == "GOAWAY received"
                ):
                    logger.warning(
                        "Failed to connect to minknow instance (retry %s/%s): %s",
                        i + 1,
                        retry_count,
                        e.details(),
                    )
                elif e.code() == grpc.StatusCode.UNAVAILABLE:
                    logger.warning(
                        "Failed to connect to minknow instance (retry %s/%s): %s",
                        i + 1,
                        retry_count,
                        e.details(),
                    )
                else:
                    raise
                error = e
                time.sleep(0.5)

        if error:
            raise error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()
