import logging
from pathlib import Path
import subprocess
import sys

from minknow_api import manager_pb2, protocol_pb2

from test_minknow_server import (
    FlowCellInfo,
    ManagerTestServer,
    PositionInfo,
    SequencingPositionTestServer,
)

example_root = Path(__file__).parent.parent.parent / "examples"

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
        [sys.executable, str(start_protocol_source), "--port", str(port), "--verbose"]
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
                    secure=0, insecure=sequencing_position.port
                ),
            ),
        ]

        with ManagerTestServer(positions=test_positions) as server:

            # Missing kit argument
            assert run_start_protocol_example(server.port, [])[0] == 2
            # Missing position/flow cell argument
            assert (
                run_start_protocol_example(server.port, ["--kit", TEST_KIT_NAME,])[0]
                == 1
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
            assert len(sequencing_position.protocol_service.started_protocols) == 1
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
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
            assert len(sequencing_position.protocol_service.started_protocols) == 2
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
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
                    secure=0, insecure=sequencing_position.port
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
            assert len(sequencing_position.protocol_service.started_protocols) == 1
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == "my-sample-id"
            assert protocol.user_info.protocol_group_id.value == "my-experiment-group"
            assert protocol.args == [
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
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
                    secure=0, insecure=sequencing_position.port
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
            assert len(sequencing_position.protocol_service.started_protocols) == 1
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
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
            assert len(sequencing_position.protocol_service.started_protocols) == 2
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--guppy_filename=%s" % TEST_BASECLL_MODEL_OTHER,
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
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
                    secure=0, insecure=sequencing_position.port
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

            assert len(sequencing_position.protocol_service.started_protocols) == 1
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.args == [
                "--base_calling=on",
                "--barcoding",
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=off",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
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

            assert len(sequencing_position.protocol_service.started_protocols) == 2
            protocol = sequencing_position.protocol_service.started_protocols[-1]
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
                "--mux-scan-period=1.5",
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
                    secure=0, insecure=sequencing_position.port
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

            assert len(sequencing_position.protocol_service.started_protocols) == 1
            protocol = sequencing_position.protocol_service.started_protocols[-1]
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
                "--mux-scan-period=1.5",
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

            assert len(sequencing_position.protocol_service.started_protocols) == 2
            protocol = sequencing_position.protocol_service.started_protocols[-1]
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
                "--mux-scan-period=1.5",
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
                    secure=0, insecure=sequencing_position.port
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
            assert len(sequencing_position.protocol_service.started_protocols) == 1
            protocol = sequencing_position.protocol_service.started_protocols[-1]
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
                "--mux-scan-period=1.5",
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
            assert len(sequencing_position.protocol_service.started_protocols) == 2
            protocol = sequencing_position.protocol_service.started_protocols[-1]
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
                "--mux-scan-period=1.5",
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
            assert len(sequencing_position.protocol_service.started_protocols) == 3
            protocol = sequencing_position.protocol_service.started_protocols[-1]
            assert protocol.identifier == TEST_PROTOCOL_IDENTIFIER
            assert protocol.user_info.sample_id.value == ""
            assert protocol.user_info.protocol_group_id.value == ""
            assert protocol.args == [
                "--experiment_time=72",
                "--fast5=off",
                "--fastq=off",
                "--bam=on",
                "--active_channel_selection=on",
                "--mux-scan-period=1.5",
            ]
