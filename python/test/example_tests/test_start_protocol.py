import logging
from pathlib import Path
import subprocess
import sys

from minknow_api import manager_pb2, protocol_pb2
from minknow_api.protocol_pb2 import BarcodeUserData

from test_minknow_server import (
    FlowCellInfo,
    ManagerTestServer,
    PositionInfo,
    SequencingPositionTestServer,
)

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


def run_start_protocol_example(port, args):
    p = subprocess.run(
        [sys.executable, str(start_protocol_source), "--port", str(port), "--verbose",]
        + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if p.returncode:
        print(p.stdout.decode("utf-8"))
    return p.returncode, p.stdout


def test_basic_start_protocol():
    """Verify basic arguments are passed correctly for starting protocols."""

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

            # Missing kit argument
            assert run_start_protocol_example(server.port, [])[0] == 2

            # Missing position/flow cell/sample sheet argument
            assert (
                run_start_protocol_example(server.port, ["--kit", TEST_KIT_NAME,])[0]
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
                    ["--kit", TEST_KIT_NAME, "--position", position_info.position_name],
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
                    ["--kit", TEST_KIT_NAME, "--position", position_info.position_name],
                )[0]
                == 1
            )

            # Protocols available
            sequencing_position.set_protocol_list([TEST_PROTOCOL])

            # Position argument supplied should work...
            assert (
                run_start_protocol_example(
                    server.port,
                    ["--kit", TEST_KIT_NAME, "--position", position_info.position_name],
                )[0]
                == 0
            )
            assert len(sequencing_position.protocol_service.protocol_runs) == 1
            protocol = sequencing_position.protocol_service.protocol_runs[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]


def test_naming_start_protocol():
    """Verify naming experiments works as expected."""

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
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]


def test_basecalling_start_protocol():
    """Verify basecalling arguments work as expected."""

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
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

            # Basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]


def test_barcoding_start_protocol():
    """Verify basecalling barcoding arguments work as expected."""

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
                        "--position",
                        position_info.position_name,
                        "--barcoding",
                    ],
                )[0]
                == 1
            )

            # Barcoding with basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

            # Barcoding with all options
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]


def test_alignment_start_protocol():
    """Verify basecalling alignment arguments work as expected."""

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
                        "--position",
                        position_info.position_name,
                        "--alignment-reference",
                        alignment_ref,
                    ],
                )[0]
                == 1
            )
            # Alignment not enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
                        "--bed-file",
                        bed_file,
                    ],
                )[0]
                == 1
            )

            # Alignment with basecalling enabled
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

            # Alignment with bed file
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]


def test_output_start_protocol():
    """Verify output options work as expected."""

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
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=on",
                "--fastq_data",
                "compress",
                "--fastq_reads_per_file=5000",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

            # Fast5
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=on",
                "--fast5_data",
                "trace_table",
                "fastq",
                "raw",
                "vbz_compress",
                "--fast5_reads_per_file=501",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

            # BAM
            assert (
                run_start_protocol_example(
                    server.port,
                    [
                        "--kit",
                        TEST_KIT_NAME,
                        "--position",
                        position_info.position_name,
                        "--bam",
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=on",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]


def sample_sheet_csv_path(*args):
    return str(
        Path(__file__).parent.joinpath("sample_sheets", *args).with_suffix(".csv")
    )


def test_sample_sheet_start_protocol():
    """Verify that the `--sample-sheet` argument works as expected."""
    """Verify basecalling barcoding arguments work as expected."""

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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]

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
                        "--position",
                        position_info.position_name,
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
                        "--position",
                        position_info.position_name,
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
                        "--position",
                        position_info.position_name,
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
                        "--position",
                        position_info.position_name,
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
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux_scan_period=1.5",
            ]
