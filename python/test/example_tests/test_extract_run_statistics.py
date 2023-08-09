import subprocess
import sys
import tempfile
import textwrap
import uuid
from pathlib import Path

from mock_server import (
    ManagerServicer,
    Server,
    InstanceServicer,
)

from minknow_api import (
    acquisition_pb2_grpc,
    acquisition_pb2,
    manager_pb2,
    protocol_pb2,
    statistics_pb2,
    statistics_pb2_grpc,
    protocol_pb2_grpc,
)

example_root = Path(__file__).parent.parent.parent / "minknow_api" / "examples"

start_protocol_source = example_root / "extract_run_statistics.py"

TEST_ACQUISITION = acquisition_pb2.AcquisitionRunInfo(run_id=str(uuid.uuid4()))

TEST_PROTOCOL = protocol_pb2.ProtocolRunInfo(
    run_id=str(uuid.uuid4()),
)
TEST_PROTOCOL_WITH_ACQUISTIIONS = protocol_pb2.ProtocolRunInfo(
    run_id=str(uuid.uuid4()), acquisition_run_ids=[TEST_ACQUISITION.run_id]
)

TEST_ACQUISITION_OUTPUT_STATS = [
    statistics_pb2.StreamAcquisitionOutputResponse(
        snapshots=[
            statistics_pb2.StreamAcquisitionOutputResponse.FilteredSnapshots(
                filtering=[
                    statistics_pb2.AcquisitionOutputKey(
                        barcode_name="barcode1234",
                        lamp_barcode_id="unclassified",
                        lamp_target_id="unclassified",
                        alignment_reference="unaligned",
                    )
                ],
                snapshots=[
                    statistics_pb2.AcquisitionOutputSnapshot(
                        seconds=60,
                        yield_summary=acquisition_pb2.AcquisitionYieldSummary(
                            basecalled_pass_read_count=600
                        ),
                    )
                ],
            )
        ]
    )
]


class AcquisitionServicer(acquisition_pb2_grpc.AcquisitionServiceServicer):
    def __init__(self):
        self.acquisition_runs = []

    def get_acquisition_info(
        self, request: acquisition_pb2.GetAcquisitionRunInfoRequest, _context
    ) -> acquisition_pb2.AcquisitionRunInfo:
        """Find info on previously run acquisition"""
        for acquisition in self.acquisition_runs:
            if acquisition.run_id == request.run_id:
                return acquisition

        raise Exception("Failed to find acquisition %s" % request.run_id)


class StatisticsServicer(statistics_pb2_grpc.StatisticsServiceServicer):
    def __init__(self):
        self.acquisition_outputs_per_run = {}

    def stream_acquisition_output(
        self, request: statistics_pb2.StreamAcquisitionOutputRequest, _context
    ) -> statistics_pb2.StreamAcquisitionOutputResponse:
        """Stream acquisition output data from a requested acquisition"""
        for packet in self.acquisition_outputs_per_run[request.acquisition_run_id]:
            yield packet


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

    def get_run_info(
        self, request: protocol_pb2.GetRunInfoRequest, _context
    ) -> protocol_pb2.ProtocolRunInfo:
        """Find info on previously run protocols"""
        for protocol in self.protocol_runs:
            if protocol.run_id == request.run_id:
                return protocol

        raise Exception("Failed to find protocol %s" % request.run_id)


def run_extract_run_statistics_example(port, args, exp_return_code=0):
    # setting an IP address for host (rather than using "localhost") significantly
    # speeds up tests on Windows
    p = subprocess.run(
        [
            sys.executable,
            str(start_protocol_source),
            "--host=127.0.0.1",
            "--port",
            str(port),
            "--verbose",
        ]
        + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if p.returncode != exp_return_code:
        print(p.stdout.decode("utf-8"))
    assert p.returncode == exp_return_code


def test_basic_run_statistics():
    """Verify basic arguments are passed correctly for getting run statistics."""

    acquisition_servicer = AcquisitionServicer()
    instance_servicer = InstanceServicer()
    protocol_servicer = ProtocolServicer()
    statistics_servicer = StatisticsServicer()
    servicers = [
        acquisition_servicer,
        instance_servicer,
        protocol_servicer,
        statistics_servicer,
    ]
    with Server(servicers) as sequencing_position:
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
            # No position supplied
            run_extract_run_statistics_example(server.port, [], exp_return_code=2)

            # No protocols available
            run_extract_run_statistics_example(
                server.port, ["--position=MN00000"], exp_return_code=1
            )

            # No acquisitions in protocol
            protocol_servicer.protocol_runs = [TEST_PROTOCOL]
            run_extract_run_statistics_example(
                server.port, ["--position=MN00000"], exp_return_code=1
            )

            # Everything in place - should generate a valid report
            protocol_servicer.protocol_runs = [TEST_PROTOCOL_WITH_ACQUISTIIONS]
            acquisition_servicer.acquisition_runs = [TEST_ACQUISITION]
            statistics_servicer.acquisition_outputs_per_run[
                TEST_ACQUISITION.run_id
            ] = TEST_ACQUISITION_OUTPUT_STATS
            with tempfile.TemporaryDirectory() as output_dir:
                run_extract_run_statistics_example(
                    server.port, ["--position=MN00000", "--output-dir", output_dir]
                )

                expected_report = textwrap.dedent(
                    """\
                    Acquisition report
                    ==================

                    Output snapshots for barcode: barcode1234, lamp_barcode_id: unclassified, lamp_target_id: unclassified, alignment_reference: unaligned
                    --------------------------------------------------------------------------------------------------------------------------------------

                    Timestamp(s)\tPassed Called reads\tFailed Reads\tBasecalled samples
                    60\t600\t0\t0

                    """
                )

                exp_output_filename = f"acquisition_output_{TEST_ACQUISITION.run_id}.md"
                expected_output_path = Path(output_dir) / exp_output_filename
                assert expected_output_path.exists()
                assert expected_output_path.read_text() == expected_report
