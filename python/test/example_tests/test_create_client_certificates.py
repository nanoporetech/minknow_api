import datetime
import logging
import subprocess
import sys
import tempfile
from pathlib import Path

import grpc
from cryptography import x509
from minknow_api import manager_service, instance_pb2
from mock_server import Server, load_test_ca

create_client_certs = (
    Path(__file__).parent.parent.parent
    / "minknow_api"
    / "examples"
    / "create_client_certificates.py"
)


class ManagerServicer(manager_service.ManagerServiceServicer):
    def __init__(self, expected_peer_identity: bytes):
        self.expected_peer_identity = expected_peer_identity

    def get_version_info(
        self,
        request: manager_service.GetVersionInfoRequest,
        context: grpc.ServicerContext,
    ) -> instance_pb2.GetVersionInfoResponse:
        logging.info("Request received from %s", context.peer_identities())
        assert context.peer_identities() is not None
        assert self.expected_peer_identity in context.peer_identities()
        return instance_pb2.GetVersionInfoResponse(
            minknow=instance_pb2.GetVersionInfoResponse.MinknowVersion(
                major=4, minor=0, patch=0, full="4.0.0"
            )
        )


def do_certs_test(client_key: bytes, client_cert_chain: bytes, root_certs: bytes):
    manager_servicer = ManagerServicer(expected_peer_identity=b"test client")
    with Server([manager_servicer], client_root_certs=root_certs) as server:
        client_creds = grpc.ssl_channel_credentials(
            root_certificates=load_test_ca(),
            private_key=client_key,
            certificate_chain=client_cert_chain,
        )
        channel = grpc.secure_channel(
            f"127.0.0.1:{server.port}",
            client_creds,
            options=[
                (
                    "grpc.ssl_target_name_override",
                    "localhost",
                )
            ],
        )
        mgr_service = manager_service.ManagerService(channel)
        version_info = mgr_service.get_version_info()
        assert version_info.minknow.full == "4.0.0"


def test_client_certs_accepted_by_grpc_self_signed():
    """The generated client certificates must be accepted by gRPC."""

    with tempfile.TemporaryDirectory() as client_certs_dir:
        client_certs_dir = Path(client_certs_dir)
        subprocess.run(
            [
                sys.executable,
                str(create_client_certs),
                str(client_certs_dir / "client"),
                "--common-name=test client",
                "--no-key-pass",
            ],
            check=True,
        )

        client_cert_path = client_certs_dir / "client_cert.pem"
        client_key_path = client_certs_dir / "client_key.pem"
        assert client_cert_path.exists()
        assert client_key_path.exists()
        client_cert = client_cert_path.read_bytes()

        do_certs_test(
            client_key=client_key_path.read_bytes(),
            client_cert_chain=client_cert,
            root_certs=client_cert,
        )


def test_client_certs_days_valid():
    """The days-valid option must alter certificate expiry."""

    with tempfile.TemporaryDirectory() as client_certs_dir:
        client_certs_dir = Path(client_certs_dir)
        subprocess.run(
            [
                sys.executable,
                str(create_client_certs),
                str(client_certs_dir / "client"),
                "--common-name=test client",
                "--no-key-pass",
                "--days-valid=1",
            ],
            check=True,
        )

        client_cert_path = client_certs_dir / "client_cert.pem"
        client_key_path = client_certs_dir / "client_key.pem"
        assert client_cert_path.exists()
        assert client_key_path.exists()
        client_cert = client_cert_path.read_bytes()

        do_certs_test(
            client_key=client_key_path.read_bytes(),
            client_cert_chain=client_cert,
            root_certs=client_cert,
        )

        # Check that it's valid for just one day (With 10 second tolerance)
        actual_expiry = x509.load_pem_x509_certificate(client_cert).not_valid_after
        expected_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=1)

        assert abs(actual_expiry.timestamp() - expected_expiry.timestamp()) < 10


def test_client_certs_accepted_by_grpc_with_ca():
    """The generated client certificates must be accepted by gRPC."""

    with tempfile.TemporaryDirectory() as client_certs_dir:
        client_certs_dir = Path(client_certs_dir)
        subprocess.run(
            [
                sys.executable,
                str(create_client_certs),
                str(client_certs_dir / "ca"),
                "--no-key-pass",
            ],
            check=True,
        )
        client_ca_cert_path = client_certs_dir / "ca_cert.pem"
        client_ca_key_path = client_certs_dir / "ca_key.pem"
        assert client_ca_cert_path.exists()
        assert client_ca_key_path.exists()
        client_ca_cert = client_ca_cert_path.read_bytes()

        subprocess.run(
            [
                sys.executable,
                str(create_client_certs),
                str(client_certs_dir / "client"),
                "--common-name=test client",
                "--no-key-pass",
                "--ca-cert",
                str(client_certs_dir / "ca_cert.pem"),
                "--ca-key",
                str(client_certs_dir / "ca_key.pem"),
            ],
            check=True,
        )

        client_cert_path = client_certs_dir / "client_cert.pem"
        client_key_path = client_certs_dir / "client_key.pem"
        assert client_cert_path.exists()
        assert client_key_path.exists()

        do_certs_test(
            client_key=client_key_path.read_bytes(),
            client_cert_chain=client_cert_path.read_bytes() + client_ca_cert,
            root_certs=client_ca_cert,
        )
