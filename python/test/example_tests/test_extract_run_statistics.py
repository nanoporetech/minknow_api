from pathlib import Path
import subprocess
import sys
import uuid

from minknow_api import acquisition_pb2, manager_pb2, protocol_pb2, statistics_pb2

from test_minknow_server import (
    FlowCellInfo,
    ManagerTestServer,
    PositionInfo,
    SequencingPositionTestServer,
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


def run_extract_run_statistics_example(port, args):
    p = subprocess.run(
        [sys.executable, str(start_protocol_source), "--port", str(port), "--verbose"]
        + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if p.returncode:
        print(p.stdout.decode("utf-8"))
    return p.returncode, p.stdout


def test_basic_start_protocol():
    """Verify basic arguments are passed correctly for getting run statistics."""

    position_info = PositionInfo(position_name="MN00000")

    with SequencingPositionTestServer(position_info) as sequencing_position:
        test_positions = [
            manager_pb2.FlowCellPosition(
                name=position_info.position_name,
                state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                    secure=sequencing_position.port
                ),
            ),
        ]

        with ManagerTestServer(positions=test_positions) as server:
            # No position supplied
            assert run_extract_run_statistics_example(server.port, [])[0] == 2

            # No protocols available
            assert (
                run_extract_run_statistics_example(
                    server.port,
                    [
                        "--position",
                        position_info.position_name,
                    ],
                )[0]
                == 1
            )

            # No acquisitions in protocol
            sequencing_position.set_protocol_runs([TEST_PROTOCOL])
            assert (
                run_extract_run_statistics_example(
                    server.port,
                    [
                        "--position",
                        position_info.position_name,
                    ],
                )[0]
                == 1
            )

            # Everything in place - should generate a valid report
            sequencing_position.set_protocol_runs([TEST_PROTOCOL_WITH_ACQUISTIIONS])
            sequencing_position.set_acquisition_runs([TEST_ACQUISITION])
            sequencing_position.set_acquisition_output_statistics(
                TEST_ACQUISITION.run_id, TEST_ACQUISITION_OUTPUT_STATS
            )
            assert (
                run_extract_run_statistics_example(
                    server.port,
                    [
                        "--position",
                        position_info.position_name,
                    ],
                )[0]
                == 0
            )

            expected_report = """Acquisition report
==================

Output snapshots for barcode: barcode1234, lamp_barcode_id: unclassified, lamp_target_id: unclassified, alignment_reference: unaligned
--------------------------------------------------------------------------------------------------------------------------------------

Timestamp(s)\tPassed Called reads\tFailed Reads\tBasecalled samples
60\t600\t0\t0

"""

            expected_output_path = Path(
                "acquisition_output_%s.md" % TEST_ACQUISITION.run_id
            )
            assert expected_output_path.exists()
            assert expected_output_path.read_text() == expected_report
