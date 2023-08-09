import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from mock_server import (
    InstanceServicer,
    ManagerServicer,
    Server,
)

from minknow_api import (
    acquisition_pb2,
    device_pb2,
    device_pb2_grpc,
    manager_pb2,
    protocol_pb2,
    protocol_pb2_grpc,
    run_until_pb2,
)
from minknow_api.protocol_pb2 import BarcodeUserData
from minknow_api.tools.any_helpers import make_uint64_any

example_root = Path(__file__).parent.parent.parent / "minknow_api" / "examples"

start_protocol_source = example_root / "start_protocol.py"

TEST_PROTOCOL_IDENTIFIER = "foo-identifier"
TEST_KIT_NAME = "foo-bar-kit"
TEST_BASECLL_MODEL = "test.cfg"
TEST_BASECLL_MODEL_OTHER = "test2.cfg"
TEST_BARCODING_KIT = "foo-barcodes"
TEST_PROTOCOL = protocol_pb2.ProtocolInfo(
    identifier=TEST_PROTOCOL_IDENTIFIER,
    tag_extraction_result=protocol_pb2.ProtocolInfo.TagExtractionResult(success=True),
    tags={
        "kit": protocol_pb2.ProtocolInfo.TagValue(string_value=TEST_KIT_NAME),
        "experiment type": protocol_pb2.ProtocolInfo.TagValue(
            string_value="sequencing"
        ),
        "default basecall model": protocol_pb2.ProtocolInfo.TagValue(
            string_value=TEST_BASECLL_MODEL
        ),
        "available basecall models": protocol_pb2.ProtocolInfo.TagValue(
            array_value='["%s","%s"]' % (TEST_BASECLL_MODEL, TEST_BASECLL_MODEL_OTHER)
        ),
    },
)
TEST_BARCODING_PROTOCOL = protocol_pb2.ProtocolInfo(
    identifier=TEST_PROTOCOL_IDENTIFIER,
    tag_extraction_result=protocol_pb2.ProtocolInfo.TagExtractionResult(success=True),
    tags={
        "kit": protocol_pb2.ProtocolInfo.TagValue(string_value=TEST_KIT_NAME),
        "experiment type": protocol_pb2.ProtocolInfo.TagValue(
            string_value="sequencing"
        ),
        "default basecall model": protocol_pb2.ProtocolInfo.TagValue(
            string_value=TEST_BASECLL_MODEL
        ),
        "available basecall models": protocol_pb2.ProtocolInfo.TagValue(
            array_value='["%s","%s"]' % (TEST_BASECLL_MODEL, TEST_BASECLL_MODEL_OTHER)
        ),
        "barcoding": protocol_pb2.ProtocolInfo.TagValue(bool_value=True),
        "barcoding kits": protocol_pb2.ProtocolInfo.TagValue(
            array_value='["%s"]' % (TEST_BARCODING_KIT)
        ),
    },
)
TEST_RUN_UNTIL_CRITERIA = acquisition_pb2.TargetRunUntilCriteria(
    stop_criteria=run_until_pb2.CriteriaValues(
        criteria={"runtime": make_uint64_any(72 * 60 * 60)}
    )
)


@dataclass
class FlowCellInfo:
    flow_cell_id: str
    has_flow_cell: bool


class DeviceServicer(device_pb2_grpc.DeviceServiceServicer):
    def __init__(self):
        self.flow_cell_info = FlowCellInfo(flow_cell_id="", has_flow_cell=False)

    def get_flow_cell_info(
        self, _request: device_pb2.GetFlowCellInfoRequest, _context
    ) -> device_pb2.GetFlowCellInfoResponse:
        """Find the version information for the connected flow cell"""
        return device_pb2.GetFlowCellInfoResponse(
            channel_count=512,
            wells_per_channel=4,
            has_flow_cell=self.flow_cell_info.has_flow_cell,
            flow_cell_id=self.flow_cell_info.flow_cell_id,
            has_adapter=False,
        )


class ProtocolServicer(protocol_pb2_grpc.ProtocolServiceServicer):
    def __init__(self):
        self.protocol_list = []
        self.protocol_runs = []

    def list_protocols(
        self, _request: protocol_pb2.ListProtocolsRequest, _context
    ) -> protocol_pb2.ListProtocolsResponse:
        """Find the available protocols to start"""
        return protocol_pb2.ListProtocolsResponse(protocols=self.protocol_list)

    def start_protocol(
        self, request: protocol_pb2.StartProtocolRequest, _context
    ) -> protocol_pb2.StartProtocolResponse:
        """Start a new protocol"""
        self.protocol_runs.append(request)
        return protocol_pb2.StartProtocolResponse(run_id=str(len(self.protocol_runs)))


class SequencingPositionTestServer(Server):
    """
    Test server runs grpc manager service on a port.
    """

    def __init__(self):
        self.device_service = DeviceServicer()
        self.instance_service = InstanceServicer()
        self.protocol_service = ProtocolServicer()

        super().__init__(
            [
                self.device_service,
                self.instance_service,
                self.protocol_service,
            ]
        )

    def set_flow_cell_info(self, flow_cell_info):
        """Set connected flow cell info"""
        self.device_service.flow_cell_info = flow_cell_info

    def set_protocol_list(self, protocol_list):
        """Set available protocols on the position"""
        self.protocol_service.protocol_list = protocol_list


def run_start_protocol_example(port, args):
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
        capture_output=True,
    )
    if p.returncode:
        print(p.stdout.decode("utf-8"))
    return p.returncode, p.stdout


def test_basic_start_protocol():
    """Verify basic arguments are passed correctly for starting protocols."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:

            # Missing kit argument
            assert run_start_protocol_example(server.port, [])[0] == 2

            # Missing position/flow cell/sample sheet argument
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                    ],
                )[0]
                == 2
            )

            # Invalid position argument
            assert (
                run_start_protocol_example(
                    server.port, ["--kit", TEST_KIT_NAME, "--position", "NotAPosition"]
                )[0]
                == 1
            )

            # Invalid flow-cell-id argument
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--flow-cell-id", "NotAFlowCellId"],
                )[0]
                == 1
            )

            # Invalid sample-sheet argument (file not found)
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--sample-sheet", "NotASampleSheet"],
                )[0]
                == 1
            )

            # Invalid sample-sheet argument (bad sample sheet)
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--sample-sheet",
                        sample_sheet_csv_path("bad_column_names", "no_columns"),
                    ],
                )[0]
                == 1
            )

            # Too many position arguments
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        "abc",
                        "--flow-cell-id",
                        "def",
                        "--sample-sheet",
                        "ghi",
                    ],
                )[0]
                == 2
            )

            # No flow cell
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=False, flow_cell_id="")
            )
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--position=MN00000"],
                )[0]
                == 1
            )

            # Flow cell inserted
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )

            # No protocols available
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--position=MN00000"],
                )[0]
                == 1
            )

            # Protocols available
            sequencing_position.set_protocol_list([TEST_PROTOCOL])

            # Position argument supplied should work...
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--position=MN00000"],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--flow-cell-id", test_flow_cell_id],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 2
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA


def test_naming_start_protocol():
    """Verify naming experiments works as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list([TEST_PROTOCOL])

            # Position argument supplied should work...
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--sample-id",
                        "my-sample-id",
                        "--experiment-group",
                        "my-experiment-group",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == "my-sample-id"
            assert protocol.user_info.protocol_group_id.value == "my-experiment-group"
            assert protocol.args == [
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA


def test_basecalling_start_protocol():
    """Verify basecalling arguments work as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list([TEST_PROTOCOL])

            # Basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--basecalling",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--basecalling",
                        "--basecall-config",
                        TEST_BASECLL_MODEL_OTHER,
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 2
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--guppy_filename=%s" % TEST_BASECLL_MODEL_OTHER,
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA


def test_barcoding_start_protocol():
    """Verify basecalling barcoding arguments work as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list(
                [TEST_PROTOCOL, TEST_BARCODING_PROTOCOL]
            )

            # Basecalling not enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--barcoding",
                    ],
                )[0]
                == 2
            )

            # Barcoding with basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--basecalling",
                        "--barcoding",
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--barcoding",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Barcoding with all options
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--basecalling",
                        "--barcoding",
                        "--barcode-kits",
                        TEST_BARCODING_KIT,
                        "--trim-barcodes",
                        "--barcodes-both-ends",
                        "--detect-mid-strand-barcodes",
                        "--min-score",
                        "5",
                        "--min-score-rear",
                        "6",
                        "--min-score-mid",
                        "7",
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 2
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--barcoding",
                "barcoding_kits=['foo-barcodes',]",
                "trim_barcodes=on",
                "require_barcodes_both_ends=on",
                "detect_mid_strand_barcodes=on",
                "min_score=5.0",
                "min_score_rear=6.0",
                "min_score_mid=7.0",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA


def test_alignment_start_protocol():
    """Verify basecalling alignment arguments work as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list(
                [TEST_PROTOCOL, TEST_BARCODING_PROTOCOL]
            )

            alignment_ref = "foo.fasta"
            bed_file = "bar.bed"

            # Basecalling not enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--alignment-reference",
                        alignment_ref,
                    ],
                )[0]
                == 2
            )
            # Alignment not enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--bed-file",
                        bed_file,
                    ],
                )[0]
                == 2
            )

            # Alignment with basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--basecalling",
                        "--alignment-reference",
                        alignment_ref,
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--alignment",
                "reference_files=['foo.fasta',]",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Alignment with bed file
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--basecalling",
                        "--alignment-reference",
                        alignment_ref,
                        "--bed-file",
                        bed_file,
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 2
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--alignment",
                "reference_files=['foo.fasta',]",
                "bed_file='bar.bed'",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA


def test_output_start_protocol():
    """Verify output options work as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list([TEST_PROTOCOL])

            # Fastq
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--fastq",
                        "--fastq-reads-per-file",
                        "5000",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--fast5=off",
                "--pod5=off",
                "--fastq=on",
                "--fastq_data",
                "compress",
                "--fastq_reads_per_file=5000",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Fast5
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--fast5",
                        "--fast5-reads-per-file",
                        "501",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 2
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--fast5=on",
                "--fast5_data",
                "trace_table",
                "fastq",
                "raw",
                "vbz_compress",
                "--fast5_reads_per_file=501",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Pod5
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--pod5",
                        "--pod5-reads-per-file",
                        "502",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 3
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--fast5=off",
                "--pod5=on",
                "--pod5_reads_per_file=502",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # BAM
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--bam",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 4
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=on",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA


def sample_sheet_csv_path(*args):
    return str(
        Path(__file__).parent.joinpath("sample_sheets", *args).with_suffix(".csv")
    )


def test_sample_sheet_start_protocol():
    """Verify that the `--sample-sheet` argument works as expected."""
    """Verify basecalling barcoding arguments work as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list(
                [TEST_PROTOCOL, TEST_BARCODING_PROTOCOL]
            )

            # Sample sheet specifies position_id
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--sample-sheet",
                        sample_sheet_csv_path(
                            "good", "start_protocol_test_with_position_id"
                        ),
                        "--basecalling",
                        "--barcoding",
                        "--barcode-kits",
                        TEST_BARCODING_KIT,
                        "--trim-barcodes",
                        "--barcodes-both-ends",
                        "--detect-mid-strand-barcodes",
                        "--min-score",
                        "5",
                        "--min-score-rear",
                        "6",
                        "--min-score-mid",
                        "7",
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.user_info.sample_id.value == "my_sample"
            assert protocol.user_info.protocol_group_id.value == "my_experiment"
            assert protocol.args == [
                "--base_calling=on",
                "--barcoding",
                "barcoding_kits=['foo-barcodes',]",
                "trim_barcodes=on",
                "require_barcodes_both_ends=on",
                "detect_mid_strand_barcodes=on",
                "min_score=5.0",
                "min_score_rear=6.0",
                "min_score_mid=7.0",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Get the sorted barcode user info
            actual_barcode_user_info = [
                el for el in protocol.user_info.barcode_user_info
            ]

            def barcode_user_info_key(el):
                return el.barcode_name, el.lamp_barcode_id

            actual_barcode_user_info = sorted(
                actual_barcode_user_info, key=barcode_user_info_key
            )

            # Make the expected values
            expected_barcode_user_info = [
                BarcodeUserData(
                    barcode_name="barcode01",
                    alias="alias01",
                    type=BarcodeUserData.SampleType.test_sample,
                ),
                BarcodeUserData(
                    barcode_name="barcode02",
                    alias="alias02",
                    type=BarcodeUserData.SampleType.positive_control,
                ),
            ]

            assert actual_barcode_user_info == expected_barcode_user_info

            # Sample sheet specifies flow_cell_id
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--sample-sheet",
                        sample_sheet_csv_path(
                            "good", "start_protocol_test_with_flow_cell_id"
                        ),
                        "--sample-id",
                        "my_sample_2",
                        "--experiment-group",
                        "my_experiment_2",
                        "--basecalling",
                        "--barcoding",
                        "--barcode-kits",
                        TEST_BARCODING_KIT,
                        "--trim-barcodes",
                        "--barcodes-both-ends",
                        "--detect-mid-strand-barcodes",
                        "--min-score",
                        "5",
                        "--min-score-rear",
                        "6",
                        "--min-score-mid",
                        "7",
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 2
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.user_info.sample_id.value == "my_sample_2"
            assert protocol.user_info.protocol_group_id.value == "my_experiment_2"
            assert protocol.args == [
                "--base_calling=on",
                "--barcoding",
                "barcoding_kits=['foo-barcodes',]",
                "trim_barcodes=on",
                "require_barcodes_both_ends=on",
                "detect_mid_strand_barcodes=on",
                "min_score=5.0",
                "min_score_rear=6.0",
                "min_score_mid=7.0",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Get the sorted barcode user info
            actual_barcode_user_info = [
                el for el in protocol.user_info.barcode_user_info
            ]

            def barcode_user_info_key(el):
                return el.barcode_name, el.lamp_barcode_id

            actual_barcode_user_info = sorted(
                actual_barcode_user_info, key=barcode_user_info_key
            )

            # Make the expected values
            expected_barcode_user_info = [
                BarcodeUserData(
                    barcode_name="barcode03",
                    alias="alias03",
                    type=BarcodeUserData.SampleType.negative_control,
                ),
                BarcodeUserData(
                    barcode_name="barcode04",
                    alias="alias04",
                    type=BarcodeUserData.SampleType.no_template_control,
                ),
            ]

            assert actual_barcode_user_info == expected_barcode_user_info

            # Sample sheet specifies experiment_id; command line specifies sample_id
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--sample-sheet",
                        sample_sheet_csv_path(
                            "good", "start_protocol_test_no_sample_id"
                        ),
                        "--sample-id",
                        "my_command_line_sample",
                    ],
                )[0]
                == 0
            )

            assert len(sequencing_position.protocol_service.protocol_runs) == 3
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.user_info.sample_id.value == "my_command_line_sample"
            assert (
                protocol.user_info.protocol_group_id.value
                == "my_sample_sheet_experiment"
            )
            assert protocol.args == [
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA

            # Get the sorted barcode user info
            actual_barcode_user_info = [
                el for el in protocol.user_info.barcode_user_info
            ]
            assert actual_barcode_user_info == []

            # sample_id specified on command line conflicts with that in sample sheet
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--sample-sheet",
                        sample_sheet_csv_path(
                            "good", "start_protocol_test_with_flow_cell_id"
                        ),
                        "--sample-id",
                        "wrong_sample_id",
                        "--basecalling",
                        "--barcoding",
                        "--barcode-kits",
                        TEST_BARCODING_KIT,
                        "--trim-barcodes",
                        "--barcodes-both-ends",
                        "--detect-mid-strand-barcodes",
                        "--min-score",
                        "5",
                        "--min-score-rear",
                        "6",
                        "--min-score-mid",
                        "7",
                    ],
                )[0]
                == 1
            )

            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--sample-sheet",
                        sample_sheet_csv_path(
                            "good", "start_protocol_test_with_flow_cell_id"
                        ),
                        "--experiment-group",
                        "wrong_experiment_id",
                        "--basecalling",
                        "--barcoding",
                        "--barcode-kits",
                        TEST_BARCODING_KIT,
                        "--trim-barcodes",
                        "--barcodes-both-ends",
                        "--detect-mid-strand-barcodes",
                        "--min-score",
                        "5",
                        "--min-score-rear",
                        "6",
                        "--min-score-mid",
                        "7",
                    ],
                )[0]
                == 1
            )


def test_read_until_start_protocol():
    """Verify read until arguments work as expected."""

    with SequencingPositionTestServer() as sequencing_position:
        manager_servicer = ManagerServicer(
            [
                manager_pb2.FlowCellPosition(
                    name="MN00000",
                    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(
                        secure=sequencing_position.port
                    ),
                ),
            ]
        )
        with Server([manager_servicer]) as server:
            # Setup for experiment
            test_flow_cell_id = "foo-bar-flow-cell"
            sequencing_position.set_flow_cell_info(
                FlowCellInfo(has_flow_cell=True, flow_cell_id=test_flow_cell_id)
            )
            sequencing_position.set_protocol_list([TEST_PROTOCOL])

            # Running without filter type:
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--read-until-reference",
                        "test.fasta",
                        "--read-until-bed-file",
                        "test.bed",
                    ],
                )[0]
                != 0
            )

            # Running without reference file:
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--read-until-bed-file",
                        "test.bed",
                        "--read-until-filter",
                        "enrich",
                    ],
                )[0]
                != 0
            )

            # Incorrect filter type
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--read-until-reference",
                        "test.fasta",
                        "--read-until-bed-file",
                        "test.bed",
                        "--read-until-filter",
                        "foo",
                    ],
                )[0]
                != 0
            )

            # Read until enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position=MN00000",
                        "--read-until-reference",
                        "test.fasta",
                        "--read-until-bed-file",
                        "test.bed",
                        "--read-until-filter",
                        "deplete",
                    ],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            print(protocol.args)
            assert protocol.args == [
                "--read_until",
                "filter_type=deplete",
                "reference_files=['test.fasta',]",
                "bed_file='test.bed'",
                "--fast5=off",
                "--pod5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
            assert protocol.target_run_until_criteria == TEST_RUN_UNTIL_CRITERIA
