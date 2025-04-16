"""Tools for interacting with protocols in minknow"""

import collections
import dataclasses
from pathlib import Path
import logging
from typing import Optional, List, Sequence, Tuple

import grpc

from .. import Connection
from minknow_api import protocol_pb2, run_until_pb2, acquisition_pb2
from minknow_api.manager_pb2 import FindBasecallConfigurationsResponse
from minknow_api.protocol_pb2 import BarcodeUserData
from minknow_api.analysis_workflows_pb2 import AnalysisWorkflowRequest
from minknow_api.tools.any_helpers import make_float_any, make_uint64_any

LOGGER = logging.getLogger(__name__)


def find_default_simplex_model(
    device_connection: Connection,
    kit: str,
    sample_rate: int,
    available_basecall_configs: List[
        FindBasecallConfigurationsResponse.BasecallConfiguration
    ],
) -> Tuple[
    FindBasecallConfigurationsResponse.BasecallConfiguration,
    FindBasecallConfigurationsResponse.SimplexModel,
]:
    default_variant = "HAC".casefold()

    flow_cell_info = device_connection.device.get_flow_cell_info()
    flow_cell_product_code = (
        flow_cell_info.user_specified_product_code or flow_cell_info.product_code
    )

    for config in available_basecall_configs:
        if (
            kit in config.kits
            and flow_cell_product_code in config.flowcells
            and sample_rate == config.sampling_rate
        ):
            for simplex in config.simplex_models:
                if simplex.variant.casefold() == default_variant:
                    return config, simplex

    raise RuntimeError(
        f"No simplex model available for kit: {kit}, sample_rate: {sample_rate}. Searched {len(available_basecall_configs)} configs"
    )


def find_simplex_model(
    available_basecall_configs: List[
        FindBasecallConfigurationsResponse.BasecallConfiguration
    ],
    simplex_model_name: str,
) -> Tuple[FindBasecallConfigurationsResponse.SimplexModel]:

    searched_configs = set()
    for config in available_basecall_configs:
        for simplex in config.simplex_models:
            searched_configs.add(simplex.name)
            if simplex.name == simplex_model_name:
                return simplex

    raise RuntimeError(
        f"No simplex model called '{simplex_model_name}' found. Searched: {', '.join(searched_configs)} configs"
    )


def find_protocol(
    device_connection: Connection,
    product_code: str,
    kit: str,
    config_name: Optional[str],
    barcoding: bool = False,
    barcoding_kits: Optional[List[str]] = None,
    force_reload: bool = False,
    experiment_type: str = "sequencing",
) -> Optional[str]:
    """Find a protocol identifier.

    This will fetch a list of protocols from the device-instance, then search through the protocols
    for one that supports the flow-cell type (product code) and all the specified options. It
    returns the first protocol it finds that matches.

    Args:
        device_connection (:obj:`Connection`):  As returned by minknow.manager.FlowCellPosition().connect().
        product_code (:obj:`str`):              The flow-cell type, as in flow_cell_info.product_code.
        kit (:obj:`str`):                       The kit to be sequenced. eg: "SQK-LSK108".
        config_name (:obj:`str`):               Optional name of a config to select.
        barcoding (bool):                       True if barcoding is required.
        barcoding_kits (:obj:`list`):           Barcoding kits that the protocol should support. If specified,
                                                barcoding is assumed to be True.
        force_reload (bool):                    If true will force reloading the protocols from their descriptions,
                                                this will take a few seconds.
        experiment_type(:obj:`str`):            Type of experiment to be run.

    Returns:
        The first protocol to match or None.
    """

    try:
        response = device_connection.protocol.list_protocols(force_reload=force_reload)
    except grpc.RpcError as exception:
        raise Exception(
            "Could not get a list of protocols ({})".format(exception.details())
        )

    if not response.protocols:
        raise Exception("List of protocols is empty")

    for protocol in response.protocols:
        # we need the tags, if we don't have them move ont next protocol
        if not protocol.tag_extraction_result.success:
            LOGGER.debug("Ignoring protocol with tag extraction failure")
            continue

        # the tags provide a way to filter the experiments
        tags = protocol.tags

        # ...with the correct name...
        if config_name is not None and protocol.name != config_name:
            LOGGER.debug(
                "Protocol is not named correctly %s, not %s",
                protocol.name,
                config_name,
            )
            continue

        # want a sequencing experiment...
        if experiment_type and tags["experiment type"].string_value != experiment_type:
            LOGGER.debug(
                "Ignoring experiment with incorrect type: %s vs %s",
                tags["experiment type"].string_value,
                experiment_type,
            )
            continue

        # ...for the correct flow-cell type...
        if tags["flow cell"].string_value != product_code:
            LOGGER.debug(
                "Protocol is for product %s, not %s",
                tags["flow cell"].string_value,
                product_code,
            )
            continue

        # ...with matching kit
        if tags["kit"].string_value != kit:
            LOGGER.debug(
                "Protocol supports kit %s, not %s", tags["kit"].string_value, kit
            )
            continue

        # if bar-coding is required, the protocol should support it and all
        # the bar-coding kits in use
        if tags["barcoding"].bool_value != barcoding:
            if barcoding:
                LOGGER.debug("Protocol does not support barcoding")
                continue
            else:
                LOGGER.debug("Protocol requires barcoding")

        supported_kits = tags["barcoding kits"].array_value
        # workaround for the set of barcoding kits being returned as a string rather
        # that array of strings
        if supported_kits and len(supported_kits[0]) == 1:
            supported_kits = (
                tags["barcoding kits"].array_value[1:-1].replace('"', "").split(",")
            )
        if tags["barcoding"].bool_value:
            supported_kits.append(tags["kit"].string_value)
        if barcoding_kits and not set(barcoding_kits).issubset(supported_kits):
            LOGGER.debug(
                "barcoding kits specified %s not amongst those supported %s",
                barcoding_kits,
                supported_kits,
            )
            continue

        # we have a match, (ignore the rest)
        return protocol
    return None


BarcodingArgs = collections.namedtuple(
    "BarcodingArgs",
    [
        "kits",
        "trim_barcodes",
        "barcodes_both_ends",
    ],
)
AlignmentArgs = collections.namedtuple("AlignmentArgs", ["reference_files", "bed_file"])
BasecallingArgs = collections.namedtuple(
    "BasecallingArgs",
    [
        "simplex_model",
        "modified_models",
        "stereo_model",
        "barcoding",
        "alignment",
        "min_qscore",
    ],
)
OutputArgs = collections.namedtuple("OutputArgs", ["reads_per_file", "batch_duration"])


@dataclasses.dataclass
class CriteriaValues:
    """
    Python representation of a `minknow_api.run_until.CriteriaValues` message

    See the `Standard Run-Until Criteria` in `run_until.proto` for further descriptions of the fields
    """

    # Runtime, in seconds
    runtime: Optional[int] = None
    # Estimated bases, in bases
    estimated_bases: Optional[int] = None
    # Passed basecalled bases, in seconds
    passed_basecalled_bases: Optional[int] = None
    # Available pores
    available_pores: Optional[float] = None

    def as_protobuf(self):
        criteria_dict = {}
        if self.runtime is not None:
            criteria_dict["runtime"] = make_uint64_any(self.runtime)
        if self.estimated_bases is not None:
            criteria_dict["estimated_bases"] = make_uint64_any(self.estimated_bases)
        if self.passed_basecalled_bases is not None:
            criteria_dict["passed_basecalled_bases"] = make_uint64_any(
                self.passed_basecalled_bases
            )
        if self.available_pores is not None:
            criteria_dict["available_pores"] = make_float_any(self.available_pores)

        return run_until_pb2.CriteriaValues(criteria=criteria_dict)


ReadUntilArgs = collections.namedtuple(
    "ReadUntilArgs",
    [
        # "enrich", or "deplete"
        "filter_type",
        # List of reference files to pass to guppy for read until (only one file supported at the moment).
        "reference_files",
        # Bed file to pass to guppy for read until
        "bed_file",
        # First channel for read until to operate on.
        "first_channel",
        # Last channel for read until to operate on.
        "last_channel",
    ],
)


def make_protocol_arguments(
    basecalling: BasecallingArgs = None,
    read_until: ReadUntilArgs = None,
    fastq_arguments: OutputArgs = None,
    fast5_arguments: OutputArgs = None,
    pod5_arguments: OutputArgs = None,
    bam_arguments: OutputArgs = None,
    disable_active_channel_selection: bool = False,
    mux_scan_period: float = 1.5,
    simulation_path: Optional[Path] = None,
    args: Optional[List[str]] = None,
    is_flongle: bool = False,
) -> List[str]:
    """Build arguments to be used when starting a protocol.

    This will assemble the arguments passed to this script into arguments to pass to the protocol.

    Args:
        basecalling(:obj:`BasecallingArgs`):    Arguments to control basecalling.
        read_until(:obj:`ReadUntilArgs):        Arguments to control read until.
        fastq_arguments(:obj:`OutputArgs`):     Control fastq file generation.
        fast5_arguments(:obj:`OutputArgs`):     Control fast5 file generation.
        pod5_arguments(:obj:`OutputArgs`):      Control pod5 file generation.
        bam_arguments(:obj:`OutputArgs`):       Control bam file generation.
        disable_active_channel_selection(bool): Disable active channel selection
        mux_scan_period(float):                 Period of time between mux scans in hours.
        simulation_path(:obj:`Path`):           An optional fast5 bulk path to use for simulated playback.
        args(:obj:`list`):                      Extra arguments to pass to protocol.
        is_flongle(bool):                       Specify if the flow cell to be sequenced on is a flongle.

    Returns:
        A list of strings to be passed as arguments to start_protocol.
    """

    def on_off(value: bool):
        if value:
            return "on"
        else:
            return "off"

    protocol_args = []

    if basecalling:
        protocol_args.append("--base_calling=on")

        models_args = []

        models_args.append(f"simplex_model='{basecalling.simplex_model}'")
        if basecalling.modified_models:
            modified_models = ",".join(f"'{m}'" for m in basecalling.modified_models)
            models_args.append(f"modified_models=[{modified_models}]")
        if basecalling.stereo_model:
            models_args.append(f"stereo_model='{basecalling.stereo_model}'")

        protocol_args.append("--basecaller_models")
        protocol_args.extend(models_args)

        protocol_args.extend(
            ["--read_filtering", f"min_qscore={basecalling.min_qscore}"]
        )

        if basecalling.barcoding:
            barcoding_args = []
            if basecalling.barcoding.kits:
                # list of barcoding kits converted to quoted, comma separated array elements
                # eg: barcoding_kits=['a','b','c']
                barcoding_args.append(
                    "barcoding_kits=['" + "','".join(basecalling.barcoding.kits) + "',]"
                )

            if basecalling.barcoding.trim_barcodes:
                # trim_barcodes=on/off
                barcoding_args.append(
                    "trim_barcodes=" + on_off(basecalling.barcoding.trim_barcodes)
                )

            if basecalling.barcoding.barcodes_both_ends:
                # require_barcodes_both_ends=on/off
                barcoding_args.append(
                    "require_barcodes_both_ends="
                    + on_off(basecalling.barcoding.barcodes_both_ends)
                )

            protocol_args.extend(["--barcoding"] + barcoding_args)

        if basecalling.alignment:
            alignment_args = []
            if basecalling.alignment.reference_files:
                alignment_args.append(
                    "reference_files=['"
                    + "','".join(basecalling.alignment.reference_files)
                    + "',]"
                )
            if basecalling.alignment.bed_file:
                alignment_args.append(
                    "bed_file='{}'".format(basecalling.alignment.bed_file)
                )
            protocol_args.extend(["--alignment"] + alignment_args)

    if read_until:
        read_until_args = []
        if read_until.filter_type:
            read_until_args.append("filter_type={}".format(read_until.filter_type))

        if read_until.reference_files:
            read_until_args.append(
                "reference_files=['" + "','".join(read_until.reference_files) + "',]"
            )

        if read_until.bed_file:
            read_until_args.append("bed_file='{}'".format(read_until.bed_file))

        if read_until.first_channel:
            read_until_args.append("first_channel={}".format(read_until.first_channel))

        if read_until.last_channel:
            read_until_args.append("last_channel={}".format(read_until.last_channel))

        protocol_args.extend(["--read_until"] + read_until_args)

    protocol_args.append("--fast5=" + on_off(fast5_arguments))
    if fast5_arguments:
        protocol_args.extend(
            ["--fast5_data", "trace_table", "fastq", "raw", "vbz_compress"]
        )
        if fast5_arguments.reads_per_file is not None:
            protocol_args.append(
                "--fast5_reads_per_file={}".format(fast5_arguments.reads_per_file)
            )
        if fast5_arguments.batch_duration is not None:
            protocol_args.append(
                "--fast5_batch_duration={}".format(fast5_arguments.batch_duration)
            )

    protocol_args.append("--pod5=" + on_off(pod5_arguments))
    if pod5_arguments:
        if pod5_arguments.reads_per_file is not None:
            protocol_args.append(
                "--pod5_reads_per_file={}".format(pod5_arguments.reads_per_file)
            )
        if pod5_arguments.batch_duration is not None:
            protocol_args.append(
                "--pod5_batch_duration={}".format(pod5_arguments.batch_duration)
            )

    protocol_args.append("--fastq=" + on_off(fastq_arguments))
    if fastq_arguments:
        protocol_args.extend(["--fastq_data", "compress"])
        if fastq_arguments.reads_per_file is not None:
            protocol_args.append(
                "--fastq_reads_per_file={}".format(fastq_arguments.reads_per_file)
            )
        if fastq_arguments.batch_duration is not None:
            protocol_args.append(
                "--fastq_batch_duration={}".format(fastq_arguments.batch_duration)
            )

    protocol_args.append("--bam=" + on_off(bam_arguments))
    if bam_arguments:
        if bam_arguments.reads_per_file is not None:
            protocol_args.append(
                "--bam_reads_per_file={}".format(bam_arguments.reads_per_file)
            )
        if bam_arguments.batch_duration is not None:
            protocol_args.append(
                "--bam_batch_duration={}".format(bam_arguments.batch_duration)
            )

    if not is_flongle:
        protocol_args.append(
            "--active_channel_selection=" + on_off(not disable_active_channel_selection)
        )
        if not disable_active_channel_selection:
            protocol_args.append("--mux_scan_period={}".format(mux_scan_period))

    if simulation_path:
        if not simulation_path.exists():
            raise Exception(
                f"Non-existent path '{simulation_path}' passed for simulation."
            )
        protocol_args.extend(["--simulation", str(simulation_path)])

    if args:
        protocol_args.extend(args)

    return protocol_args


def make_target_run_until_criteria(
    stop_criteria: Optional[CriteriaValues] = None,
    experiment_duration: Optional[float] = None,
) -> acquisition_pb2.TargetRunUntilCriteria:
    """Make an `acquisition.TargetRunUntilCriteria` message based on the supplied parameters

    If `stop_criteria` is supplied, then the `stop_criteria` in the returned message are set to match the supplied
    criteria.  Otherwise, if `experiment_duration` is supplied, then the "runtime" stop criterion in the returned
    message is set to match the supplied `experiment_duration`.

    If no arguments are supplied, the returned message will be empty.  If both arguments are supplied, a `ValueError`
    is raised, since only one or the other argument may be supplied

    Args:
        stop_criteria(:obj:`CriteriaValues`):   Stop criteria to set.
        experiment_duration(float):             Length of the experiment in hours.

    Returns:
        An `acquisition.TargetRunUntilCriteria` message with the specified criteria
    """

    if stop_criteria and experiment_duration:
        raise ValueError(
            "Can specify `stop_criteria` or `experiment_duration` but not both"
        )

    if experiment_duration:
        # Case of having both is handled above
        # The assert below corresponds to the comment above, and is NOT a run-time check
        assert not stop_criteria  # nosec B101

        # `experiment_duration` is in hours
        # `runtime` is in seconds
        stop_criteria = CriteriaValues(runtime=int(experiment_duration * 60 * 60))

    if stop_criteria:
        return acquisition_pb2.TargetRunUntilCriteria(
            stop_criteria=stop_criteria.as_protobuf()
        )
    else:
        # Empty target criteria
        return acquisition_pb2.TargetRunUntilCriteria()


def start_protocol(
    device_connection: Connection,
    identifier: str,
    sample_id: str,
    experiment_group: str,
    barcode_info: Optional[Sequence[BarcodeUserData]],
    stop_criteria: Optional[CriteriaValues] = None,
    experiment_duration: Optional[float] = None,
    analysis_workflow_request: Optional[AnalysisWorkflowRequest] = None,
    *args,
    **kwargs,
) -> str:
    """Start a protocol on the passed {device_connection}.

    Args:
        device_connection(:obj:`Connection`):   The device connection to start a protocol on.
        identifier(str):                        Protocol identifier to be started.
        sample_id(str):                         Sample id of protocol to start.
        experiment_group(str):                  Experiment group of protocol to start.
        barcode_info(Sequence[:obj:`BarcodeUserData`]):
                Barcode user data (sample type and alias)
        analysis_workflow_request: Optional[AnalysisWorkflowRequest]:
                Analysis workflow request message
        stop_criteria(::obj::`TargetCriteria`): When to stop the acquisition
        experiment_duration(float):             Length of the experiment in hours.
        *args: Additional arguments forwarded to {make_protocol_arguments}
        **kwargs: Additional arguments forwarded to {make_protocol_arguments}

    Returns:
        The protocol_run_id of the started protocol.

    Notes:
        Only one of `stop_criteria` and `experiment_duration` may be specified
    """

    flow_cell_info = device_connection.device.get_flow_cell_info()

    protocol_arguments = make_protocol_arguments(
        *args, is_flongle=flow_cell_info.has_adapter, **kwargs
    )
    LOGGER.debug("Built protocol arguments: %s", " ".join(protocol_arguments))

    user_info = protocol_pb2.ProtocolRunUserInfo()
    if sample_id:
        user_info.sample_id.value = sample_id
    if experiment_group:
        user_info.protocol_group_id.value = experiment_group
    if barcode_info:
        user_info.barcode_user_info.extend(barcode_info)

    # Run until criteria
    target_run_until_criteria = make_target_run_until_criteria(
        stop_criteria=stop_criteria,
        experiment_duration=experiment_duration,
    )

    # Only pass analysis_workflow_request to start_protocol() if the user explicitly supplied it
    additional_params = {}
    if analysis_workflow_request is not None:
        additional_params["analysis_workflow_request"] = analysis_workflow_request

    result = device_connection.protocol.start_protocol(
        identifier=identifier,
        args=protocol_arguments,
        user_info=user_info,
        target_run_until_criteria=target_run_until_criteria,
        **additional_params,
    )

    return result.run_id
