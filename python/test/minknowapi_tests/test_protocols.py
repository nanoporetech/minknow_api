import minknow_api.acquisition_pb2
import minknow_api.analysis_workflows_pb2 as analysis_workflows
from minknow_api.tools import protocols, any_helpers
from minknow_api.tools.protocols import (
    BarcodingArgs,
    AlignmentArgs,
    BasecallingArgs,
    OutputArgs,
    ReadUntilArgs,
)

import pytest


def test_criteria_values():
    """Check that the CriteriaValues class generates protobuf messages as expected

    Each of the class variables in `CriteriaValues` can be `None` or not-`None`

    If the value is not-`None`, there should be a corresponding entry of the correct type in the generated protobuf
    message.

    If the value is `None`, there should not be a corresponding entry in the generated protobuf message

    Don't test the case where a class variable is set to an invalid type (e.g. setting runtime to a string) -- the
    protobuf well-known-types in the generated messages enforce this constraint.
    """

    test_params = (
        {
            "runtime": runtime,
            "estimated_bases": estimated_bases,
            "passed_basecalled_bases": passed_basecalled_bases,
            "available_pores": available_pores,
        }
        for runtime in (123, None)
        for estimated_bases in (456, None)
        for passed_basecalled_bases in (789, None)
        for available_pores in (42.125, None)
    )

    for test_param in test_params:
        criteria_values = protocols.CriteriaValues(**test_param)

        protobuf = criteria_values.as_protobuf()

        if criteria_values.runtime is not None:
            proto_any = protobuf.criteria["runtime"]
            proto_val = any_helpers.unpack_well_known_type_any(proto_any)
            # We want exact type equality checking here
            assert type(proto_val) == type(criteria_values.runtime)  # noqa: E721
            assert proto_val == criteria_values.runtime
        else:
            assert "runtime" not in protobuf.criteria

        if criteria_values.estimated_bases is not None:
            proto_any = protobuf.criteria["estimated_bases"]
            proto_val = any_helpers.unpack_well_known_type_any(proto_any)
            # We want exact type equality checking here
            assert type(proto_val) == type(  # noqa: E721
                criteria_values.estimated_bases
            )
            assert proto_val == criteria_values.estimated_bases
        else:
            assert "estimated_bases" not in protobuf.criteria

        if criteria_values.passed_basecalled_bases is not None:
            proto_any = protobuf.criteria["passed_basecalled_bases"]
            proto_val = any_helpers.unpack_well_known_type_any(proto_any)
            # We want exact type equality checking here
            assert type(proto_val) == type(  # noqa: E721
                criteria_values.passed_basecalled_bases
            )
            assert proto_val == criteria_values.passed_basecalled_bases
        else:
            assert "passed_basecalled_bases" not in protobuf.criteria

        if criteria_values.available_pores is not None:
            proto_any = protobuf.criteria["available_pores"]
            proto_val = any_helpers.unpack_well_known_type_any(proto_any)
            # We want exact type equality checking here
            assert type(proto_val) == type(  # noqa: E721
                criteria_values.available_pores
            )
            assert proto_val == criteria_values.available_pores
        else:
            assert "available_pores" not in protobuf.criteria


def test_make_protocol_arguments():
    """Check that `make_protocol_arguments` behaves as expected:

    - No arguments supplied -> no arguments output
    - Arguments supplied -> arguments exist in output
    - Basecalling arguments supplied -> correct args exist in output
    - Read_until arguments supplied -> correct args exist in output
    - Writer config arguments supplied -> correct args exist in output

    """

    # validate empty args list
    args = ["hi", "test"]
    protocol_arguments = protocols.make_protocol_arguments()
    assert set(args) not in set(protocol_arguments)

    # validate with args
    protocol_arguments = protocols.make_protocol_arguments(args=args)
    assert set(args).issubset(set(protocol_arguments))

    # validate basecalling
    barcoding = BarcodingArgs("k", "trim", "")
    alignment = AlignmentArgs("r", "bed")
    basecalling = BasecallingArgs(
        "simplex", ["modified"], "stereo", barcoding, alignment, 9.0
    )
    protocol_arguments = protocols.make_protocol_arguments(basecalling=basecalling)
    assert "--base_calling=on" in protocol_arguments
    models_index = protocol_arguments.index("--basecaller_models")
    assert (
        protocol_arguments[models_index + 1]
        == f"simplex_model='{basecalling.simplex_model}'"
    )
    modified_models = ",".join(f"'{m}'" for m in basecalling.modified_models)
    assert (
        protocol_arguments[models_index + 2] == f"modified_models=[{modified_models}]"
    )
    assert (
        protocol_arguments[models_index + 3]
        == f"stereo_model='{basecalling.stereo_model}'"
    )
    assert (
        "barcoding_kits=['" + basecalling.barcoding.kits + "',]" in protocol_arguments
    )
    assert "trim_barcodes=on" in protocol_arguments
    assert "--barcoding" in protocol_arguments
    assert (
        "reference_files=['" + basecalling.alignment.reference_files + "',]"
        in protocol_arguments
    )
    assert "bed_file='" + basecalling.alignment.bed_file + "'" in protocol_arguments
    assert "--alignment" in protocol_arguments

    # validate read until
    read_until = ReadUntilArgs("enrich", "r", "bed", "", "")
    protocol_arguments = protocols.make_protocol_arguments(read_until=read_until)
    assert "filter_type=" + read_until.filter_type in protocol_arguments
    assert (
        "reference_files=['" + read_until.reference_files + "',]" in protocol_arguments
    )
    assert "bed_file='" + read_until.bed_file + "'" in protocol_arguments
    assert "--read_until" in protocol_arguments

    # validate writer config with reads per file
    fastq = OutputArgs(1000, None)
    fast5 = OutputArgs(2000, None)
    pod5 = OutputArgs(3000, None)
    bam = OutputArgs(4000, None)
    protocol_arguments = protocols.make_protocol_arguments(
        fastq_arguments=fastq,
        fast5_arguments=fast5,
        pod5_arguments=pod5,
        bam_arguments=bam,
    )
    assert set(
        ["--fast5_data", "trace_table", "fastq", "raw", "vbz_compress"]
    ).issubset(set(protocol_arguments))
    assert "--fast5_reads_per_file=" + str(fast5.reads_per_file) in protocol_arguments
    assert "--pod5_reads_per_file=" + str(pod5.reads_per_file) in protocol_arguments
    assert set(["--fastq_data", "compress"]).issubset(set(protocol_arguments))
    assert "--fastq_reads_per_file=" + str(fastq.reads_per_file) in protocol_arguments
    assert "--bam=on" in protocol_arguments
    assert "--bam_reads_per_file=" + str(bam.reads_per_file) in protocol_arguments

    # validate writer config with batch duration
    fastq = OutputArgs(None, 3600)
    fast5 = OutputArgs(None, 3600)
    pod5 = OutputArgs(None, 3600)
    bam = OutputArgs(None, 3600)
    protocol_arguments = protocols.make_protocol_arguments(
        fastq_arguments=fastq,
        fast5_arguments=fast5,
        pod5_arguments=pod5,
        bam_arguments=bam,
    )
    assert set(
        ["--fast5_data", "trace_table", "fastq", "raw", "vbz_compress"]
    ).issubset(set(protocol_arguments))
    assert "--fast5_batch_duration=" + str(fast5.batch_duration) in protocol_arguments
    assert "--pod5_batch_duration=" + str(pod5.batch_duration) in protocol_arguments
    assert set(["--fastq_data", "compress"]).issubset(set(protocol_arguments))
    assert "--fastq_batch_duration=" + str(fastq.batch_duration) in protocol_arguments
    assert "--bam=on" in protocol_arguments
    assert "--bam_batch_duration=" + str(bam.batch_duration) in protocol_arguments


def test_make_target_run_until_criteria():
    """Check that `make_target_run_until_criteria` behaves as expected:

    - No arguments supplied -> empty message returned
    - One argument supplied -> correct corresponding protobuf message returned
    - Two arguments supplied -> throws

    """
    # Not supplying any criteria
    expected = minknow_api.acquisition_pb2.TargetRunUntilCriteria()
    actual = protocols.make_target_run_until_criteria()
    assert actual == expected

    # Only supplying `stop_criteria`
    criteria_values = protocols.CriteriaValues(runtime=123, estimated_bases=456)

    expected = minknow_api.acquisition_pb2.TargetRunUntilCriteria()
    expected.stop_criteria.criteria["runtime"].CopyFrom(
        any_helpers.make_uint64_any(123)
    )
    expected.stop_criteria.criteria["estimated_bases"].CopyFrom(
        any_helpers.make_uint64_any(456)
    )

    actual = protocols.make_target_run_until_criteria(stop_criteria=criteria_values)
    assert actual == expected

    # Only supplying `experiment_duration`
    experiment_duration_hours = 13.2
    runtime_seconds = int(experiment_duration_hours * 60 * 60)

    expected = minknow_api.acquisition_pb2.TargetRunUntilCriteria()
    expected.stop_criteria.criteria["runtime"].CopyFrom(
        any_helpers.make_uint64_any(runtime_seconds)
    )

    actual = protocols.make_target_run_until_criteria(
        experiment_duration=experiment_duration_hours
    )

    assert actual == expected

    # Supplying both

    with pytest.raises(ValueError):
        protocols.make_target_run_until_criteria(
            stop_criteria=protocols.CriteriaValues(runtime=123),
            experiment_duration=123.0,
        )


class DeviceServiceMock:
    class FlowCellInfo:
        def __init__(self):
            self.has_adapter = True

    def __init__(self):
        self.flow_cell_info = self.FlowCellInfo()

    def get_flow_cell_info(self):
        return self.flow_cell_info


class ProtocolServiceMock:
    class Result:
        def __init__(self):
            self.run_id = "run id test"

    def __init__(self):
        self.result = self.Result()

    def start_protocol(self, **kwargs):
        self.start_protocol_args = kwargs
        return self.result


class DeviceConnectionMock:
    def __init__(self):
        self.device = DeviceServiceMock()
        self.protocol = ProtocolServiceMock()


def test_start_protocol():
    device_connection = DeviceConnectionMock()

    # Test with AnalysisWorkflowRequest data

    workflow_params = analysis_workflows.AnalysisWorkflowRequest()
    workflow_params.workflow_id = "workflow_id"
    workflow_params.parameters = "parameters"

    run_id = protocols.start_protocol(
        device_connection,
        identifier="",
        sample_id="",
        experiment_group="",
        barcode_info=None,
        analysis_workflow_request=workflow_params,
    )

    start_protocol_args = device_connection.protocol.start_protocol_args
    assert run_id == device_connection.protocol.result.run_id
    assert start_protocol_args["analysis_workflow_request"] == workflow_params

    # Test with empty AnalysisWorkflowRequest data

    workflow_params = analysis_workflows.AnalysisWorkflowRequest()

    run_id = protocols.start_protocol(
        device_connection,
        identifier="",
        sample_id="",
        experiment_group="",
        barcode_info=None,
        analysis_workflow_request=workflow_params,
    )

    start_protocol_args = device_connection.protocol.start_protocol_args
    assert run_id == device_connection.protocol.result.run_id
    assert start_protocol_args["analysis_workflow_request"] == workflow_params
