import contextlib
import grpc
import json
import logging
import os
import pytest
import tempfile
from pathlib import Path
from typing import Callable, Optional, List
from unittest.mock import patch

import minknow_api
from minknow_api.examples.create_client_certificates import (
    key_to_pem,
    cert_to_pem,
    generate_certificate_and_key,
)
from minknow_api import (
    Connection,
    manager_pb2,
    basecaller_pb2,
    basecaller_pb2_grpc,
    clear_credentials_cache,
)
from minknow_api.manager import Manager
from mock_server import (
    Server,
    ManagerServicer,
    InstanceServicer,
    load_test_ca,
    set_trusted_ca,
)


class BasecallerServicer(basecaller_pb2_grpc.BasecallerServicer):
    """Just implements cancel() - we just want to check we can connect."""

    def cancel(
        self, request: basecaller_pb2.CancelRequest, context: grpc.ServicerContext
    ) -> basecaller_pb2.CancelResponse:
        return basecaller_pb2.CancelResponse()


class TokenCredentials(grpc.AuthMetadataPlugin):
    def __init__(self, key: str, token: str):
        self.key = key
        self.token = token

    def __call__(self, context, callback):
        metadata = ((self.key, self.token),)
        callback(metadata, None)


ALWAYS_ALLOW_METHODS = [
    # local_authentication_token_path needs to be allowed for the credentials code to
    # work
    "/minknow_api.manager.ManagerService/local_authentication_token_path",
]


class TokenCredentialsChecker(grpc.ServerInterceptor):
    def __init__(self, key: str, token: str):
        self.key = key
        self.token = token

        def deny(_, context):
            context.abort(
                grpc.StatusCode.UNAUTHENTICATED, f"Missing or invalid {key} token"
            )

        self._deny = grpc.unary_unary_rpc_method_handler(deny)

    def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Optional[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Optional[grpc.RpcMethodHandler]:
        if (
            handler_call_details.method in ALWAYS_ALLOW_METHODS
            or (self.key, self.token) in handler_call_details.invocation_metadata
        ):
            logging.debug("Accepting %s call", handler_call_details.method)
            return continuation(handler_call_details)
        else:
            logging.debug(
                "Rejecting %s call with metadata %s",
                handler_call_details.method,
                handler_call_details.invocation_metadata,
            )
            return self._deny


class ClientCertCredentialsChecker(grpc.ServerInterceptor):
    def __init__(self, expected_peer_identity=bytes):
        self.expected_peer_identity = expected_peer_identity

        def deny(_, context):
            context.abort(
                grpc.StatusCode.UNAUTHENTICATED, "Expected peer identity not found"
            )

        self._deny = grpc.unary_unary_rpc_method_handler(deny)

    @classmethod
    def find_handler_factory(cls, handler):
        if handler.unary_unary:
            return grpc.unary_unary_rpc_method_handler, handler.unary_unary
        elif handler.unary_stream:
            return grpc.unary_stream_rpc_method_handler, handler.unary_stream
        elif handler.stream_unary:
            return grpc.stream_unary_rpc_method_handler, handler.stream_unary
        elif handler.stream_stream:
            return grpc.stream_stream_rpc_method_handler, handler.stream_stream
        else:
            raise RuntimeError("Unknown RPC type")

    def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Optional[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Optional[grpc.RpcMethodHandler]:
        next_handler = continuation(handler_call_details)
        if handler_call_details.method in ALWAYS_ALLOW_METHODS:
            return next_handler

        handler_factory, handler_callable = self.find_handler_factory(next_handler)

        def check_peer_identity(request, context):
            logging.debug("Peer identity list: %s", context.peer_identities())
            if context.peer_identities() is None:
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "No peer identity found")
            elif self.expected_peer_identity not in context.peer_identities():
                context.abort(
                    grpc.StatusCode.UNAUTHENTICATED,
                    f"Expected identity {self.expected_peer_identity} not in {context.peer_identities()}",
                )
            return handler_callable(request, context)

        return handler_factory(
            check_peer_identity,
            request_deserializer=next_handler.request_deserializer,
            response_serializer=next_handler.response_serializer,
        )


class ServerSuite(object):
    def __init__(
        self,
        interceptors: Optional[List[grpc.ServerInterceptor]] = None,
        client_root_certs: Optional[bytes] = None,
    ):
        self.instance_servicer = InstanceServicer()
        self.position_server = Server(
            [self.instance_servicer],
            interceptors=interceptors,
            client_root_certs=client_root_certs,
        )
        self.basecaller_servicer = BasecallerServicer()
        self.basecaller_server = Server(
            [self.basecaller_servicer],
            interceptors=interceptors,
            client_root_certs=client_root_certs,
        )
        self.manager_servicer = mgr_servicer = ManagerServicer(
            positions=[
                manager_pb2.FlowCellPosition(
                    name="MN12345",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=self.position_server.port
                    ),
                ),
            ],
            basecaller_port=self.basecaller_server.port,
        )
        self.manager_server = Server(
            [mgr_servicer],
            interceptors=interceptors,
            client_root_certs=client_root_certs,
        )
        self._exit_stack = contextlib.ExitStack()

    def __enter__(self):
        self._exit_stack.__enter__()
        self._exit_stack.enter_context(self.position_server)
        self._exit_stack.enter_context(self.basecaller_server)
        self._exit_stack.enter_context(self.manager_server)
        return self

    def __exit__(self, *args):
        self._exit_stack.__exit__(*args)


class ScopedEnv:
    def __init__(self, env):
        self.env = env
        self._saved = {}

    def __enter__(self):
        for key, value in self.env.items():
            self._saved[key] = self.env.get(key)
        os.environ.update(self.env)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key in self.env.keys():
            saved = self._saved[key]
            if saved is None:
                del os.environ[key]
            else:
                os.environ[key] = saved


def redirect_local_auth_token_requests(manager_port: int):
    """Patch minknow_api to redirect local authentication token path requests to a
    specific port.

    This can be useful when using minknow_api.Connection() directly (to make local
    authentication tokens work, or just to avoid slowing down the test by timing out the
    request).
    """
    orig_method = minknow_api.get_local_authentication_token_file

    def replacement(*args, **kwargs):
        return orig_method("127.0.0.1", manager_port)

    return patch("minknow_api.get_local_authentication_token_file", new=replacement)


def test_read_ssl_certificate_respects_env_var():
    """
    Check that read_ssl_certificate()'s response can be overridden with the
    MINKNOW_TRUSTED_CA environment variable.
    """
    with set_trusted_ca():
        assert minknow_api.read_ssl_certificate() == load_test_ca()


def test_token_checker_rejects_unauthenticated_connections():
    """
    This is a self-test for TokenCredentialsChecker.
    """
    token_checker = TokenCredentialsChecker("test-auth", "my_token")
    with Server([ManagerServicer()], interceptors=[token_checker]) as mgr_server:
        with pytest.raises(grpc.RpcError):
            Manager(port=mgr_server.port).version


def test_custom_credentials_passed_through():
    """
    Check that custom credentials passed to minknow_api.Connection or
    minknow_api.manager.Manager are used, and Manager passes them through to child
    connections.
    """
    test_credentials = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(load_test_ca()),
        grpc.metadata_call_credentials(TokenCredentials("test-auth", "my_token")),
    )
    token_checker = TokenCredentialsChecker("test-auth", "my_token")

    with ServerSuite(interceptors=[token_checker]) as servers:
        position_conn = Connection(
            port=servers.position_server.port, credentials=test_credentials
        )
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        mgr = Manager(port=servers.manager_server.port, credentials=test_credentials)
        positions = next(mgr.flow_cell_positions())
        position_conn = positions.connect()
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        basecaller = mgr.basecaller()
        assert basecaller is not None
        # this will raise if auth fails:
        basecaller.stub.cancel(basecaller_pb2.CancelRequest())


def test_local_auth_token_is_used_if_provided():
    """
    Check that if a local authentication token is available, it is loaded and used for
    connections.
    """
    clear_credentials_cache()
    token_checker = TokenCredentialsChecker("local-auth", "my_token")

    with tempfile.TemporaryDirectory() as temp_dir, ServerSuite(
        interceptors=[token_checker]
    ) as servers:
        temp_dir = Path(temp_dir)
        token_file = temp_dir / "local-token.json"
        with open(token_file, "w") as f:
            json.dump(
                {
                    "expires": "2150-12-01T18:45:46.729624+00:00",
                    "token": "my_token",
                },
                f,
            )

        servers.manager_servicer.local_auth_token_path = str(token_file)

        # via the manager
        mgr = Manager(port=servers.manager_server.port)
        positions = next(mgr.flow_cell_positions())
        position_conn = positions.connect()
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        basecaller = mgr.basecaller()
        assert basecaller is not None
        # this will raise if auth fails:
        basecaller.stub.cancel(basecaller_pb2.CancelRequest())

        # using Connection directly
        with redirect_local_auth_token_requests(servers.manager_server.port):
            position_conn = Connection(port=servers.position_server.port)
            assert position_conn.instance.get_version_info().minknow.full == "4.0.0"


def test_protocol_auth_token_is_used_if_env_var_is_set():
    """
    Check that if a local authentication token is available, it is loaded and used for
    connections.
    """
    clear_credentials_cache()
    token_checker = TokenCredentialsChecker("protocol-auth", "my_token")

    env = {"PROTOCOL_TOKEN": "my_token"}
    with ScopedEnv(env), ServerSuite(interceptors=[token_checker]) as servers:
        # via the manager
        mgr = Manager(port=servers.manager_server.port)
        positions = next(mgr.flow_cell_positions())
        position_conn = positions.connect()
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        basecaller = mgr.basecaller()
        assert basecaller is not None
        # this will raise if auth fails:
        basecaller.stub.cancel(basecaller_pb2.CancelRequest())

        # using Connection directly
        with redirect_local_auth_token_requests(servers.manager_server.port):
            position_conn = Connection(port=servers.position_server.port)
            assert position_conn.instance.get_version_info().minknow.full == "4.0.0"


def test_developer_api_token_passed_to_server():
    """
    Check that if a local authentication token is available, it is loaded and used for
    connections.
    """
    clear_credentials_cache()
    # developer api tokens use "local-auth" metadata
    token_checker = TokenCredentialsChecker("local-auth", "my_token")

    with ServerSuite(interceptors=[token_checker]) as servers:
        # via the manager
        mgr = Manager(port=servers.manager_server.port, developer_api_token="my_token")
        positions = next(mgr.flow_cell_positions())
        position_conn = positions.connect()
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        basecaller = mgr.basecaller()
        assert basecaller is not None
        # this will raise if auth fails:
        basecaller.stub.cancel(basecaller_pb2.CancelRequest())

        # using Connection directly
        position_conn = Connection(
            port=servers.position_server.port, developer_api_token="my_token"
        )
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"


def test_ca_certificate_passed_to_server():
    """
    Check that if a root CA certificate is available, it is used for connections.
    """
    clear_credentials_cache()
    ca_certificate = load_test_ca()

    with ServerSuite() as servers:
        # via the manager
        mgr = Manager(port=servers.manager_server.port, ca_certificate=ca_certificate)
        positions = next(mgr.flow_cell_positions())
        position_conn = positions.connect()
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        basecaller = mgr.basecaller()
        assert basecaller is not None
        # this will raise if auth fails:
        basecaller.stub.cancel(basecaller_pb2.CancelRequest())

        # using Connection directly
        position_conn = Connection(
            port=servers.position_server.port, ca_certificate=ca_certificate
        )
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"


def test_client_certificates_can_be_used_for_auth():
    """
    Check that if a local authentication token is available, it is loaded and used for
    connections.
    """
    clear_credentials_cache()
    cert, key = generate_certificate_and_key("test client", days_valid=1)
    cert_pem = cert_to_pem(cert)
    key_pem = key_to_pem(key)
    cert_checker = ClientCertCredentialsChecker(expected_peer_identity=b"test client")

    with ServerSuite(
        interceptors=[cert_checker], client_root_certs=cert_pem
    ) as servers:
        # via the manager
        mgr = Manager(
            port=servers.manager_server.port,
            client_certificate_chain=cert_pem,
            client_private_key=key_pem,
        )
        positions = next(mgr.flow_cell_positions())
        position_conn = positions.connect()
        assert position_conn.instance.get_version_info().minknow.full == "4.0.0"

        basecaller = mgr.basecaller()
        assert basecaller is not None
        # this will raise if auth fails:
        basecaller.stub.cancel(basecaller_pb2.CancelRequest())

        # using Connection directly
        with redirect_local_auth_token_requests(servers.manager_server.port):
            position_conn = Connection(
                port=servers.position_server.port,
                client_certificate_chain=cert_pem,
                client_private_key=key_pem,
            )
            assert position_conn.instance.get_version_info().minknow.full == "4.0.0"
