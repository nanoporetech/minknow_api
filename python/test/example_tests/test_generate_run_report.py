import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Iterable

from mock_server import (
    ManagerServicer,
    Server,
    InstanceServicer,
)

from minknow_api import (
    manager_pb2,
    protocol_pb2,
    protocol_pb2_grpc,
)

example_root = Path(__file__).parent.parent.parent / "minknow_api" / "examples"

start_protocol_source = example_root / "generate_run_report.py"

TEST_PROTOCOL = protocol_pb2.ProtocolRunInfo(
    run_id=str(uuid.uuid4()),
)


class ProtocolServicer(protocol_pb2_grpc.ProtocolServiceServicer):
    def __init__(self):
        self.protocol_runs = []

    def list_protocol_runs(
        self, _request: protocol_pb2.ListProtocolsRequest, _context
    ) -> protocol_pb2.ListProtocolRunsResponse:
        """List all previously run protocols"""
        return protocol_pb2.ListProtocolRunsResponse(
            run_ids=[p.run_id for p in self.protocol_runs]
        )

    def generate_run_report(
        self, request: protocol_pb2.GenerateRunReportRequest, _context
    ) -> Iterable[protocol_pb2.GenerateRunReportResponse]:
        """Get info for protocol run"""

        for protocol in self.protocol_runs:
            if protocol.run_id == request.protocol_run_id:

                if not request.include_input_data:
                    # Don't fill in `input_data`
                    yield protocol_pb2.GenerateRunReportResponse(
                        protocol_run_id=protocol.run_id,
                        report_data=protocol.run_id,
                        remaining_length=5,
                        input_data="",
                        remaining_input_length=0,
                    )

                    yield protocol_pb2.GenerateRunReportResponse(
                        protocol_run_id=protocol.run_id,
                        report_data=":html",
                        remaining_length=0,
                        input_data="",
                        remaining_input_length=0,
                    )

                    return

                else:
                    # Do fill in `input_data`
                    yield protocol_pb2.GenerateRunReportResponse(
                        protocol_run_id=protocol.run_id,
                        report_data=protocol.run_id,
                        remaining_length=5,
                        input_data=protocol.run_id,
                        remaining_input_length=5,
                    )

                    yield protocol_pb2.GenerateRunReportResponse(
                        protocol_run_id=protocol.run_id,
                        report_data=":html",
                        remaining_length=0,
                        input_data=":json",
                        remaining_input_length=0,
                    )

                    return

        raise Exception("Failed to find protocol %s" % request.protocol_run_id)


def run_generate_run_report_example(port, args, exp_return_code=0):
    # setting an IP address for host (rather than using "localhost") significantly
    # speeds up tests on Windows
    p = subprocess.run(
        [
            sys.executable,
            str(start_protocol_source),
            "--host=127.0.0.1",
            "--port",
            str(port),
        ]
        + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if p.returncode != exp_return_code:
        print(p.stdout.decode("utf-8"))
    assert p.returncode == exp_return_code

    return p.stdout.decode("utf-8")


def test_basic_generate_run_report():
    """Verify basic arguments are passed correctly for getting run statistics."""

    protocol_servicer = ProtocolServicer()
    instance_servicer = InstanceServicer()

    # Add the protocol
    protocol_servicer.protocol_runs = [TEST_PROTOCOL]

    with Server([protocol_servicer, instance_servicer]) as sequencing_position:
        test_positions = [
            manager_pb2.FlowCellPosition(
                name="MN00000",
                state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                    secure=sequencing_position.port
                ),
            ),
        ]

        manager_servicer = ManagerServicer(positions=test_positions)
        with Server([manager_servicer]) as server:

            # Protocol not available
            run_generate_run_report_example(
                server.port, ["--protocol=not_a_protocol"], exp_return_code=1
            )

            # Non-existent position specified
            run_generate_run_report_example(
                server.port,
                [f"--protocol={TEST_PROTOCOL.run_id}", "--position=not_a_position"],
                exp_return_code=1,
            )

            # Generate to stdout, html
            out = run_generate_run_report_example(
                server.port, [f"--protocol={TEST_PROTOCOL.run_id}"]
            )
            assert out.strip() == f"{TEST_PROTOCOL.run_id}:html"

            # Generate to stdout, json
            out = run_generate_run_report_example(
                server.port, [f"--protocol={TEST_PROTOCOL.run_id}", "--json"]
            )
            assert out.strip() == f"{TEST_PROTOCOL.run_id}:json"

            # Generate to file with `--output`
            with tempfile.TemporaryDirectory() as output_dir:

                # Generate HTML
                output_path_html = Path(output_dir) / "out.html"
                run_generate_run_report_example(
                    server.port,
                    [
                        f"--protocol={TEST_PROTOCOL.run_id}",
                        "--output",
                        str(output_path_html),
                    ],
                )
                assert output_path_html.exists()
                assert output_path_html.read_text() == f"{TEST_PROTOCOL.run_id}:html"

                # Generate JSON
                output_path_json = Path(output_dir) / "out.json"
                run_generate_run_report_example(
                    server.port,
                    [
                        f"--protocol={TEST_PROTOCOL.run_id}",
                        "--json",
                        "--output",
                        output_path_json,
                    ],
                )
                assert output_path_json.exists()
                assert output_path_json.read_text() == f"{TEST_PROTOCOL.run_id}:json"
