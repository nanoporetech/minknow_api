"""
Example script to start a protocol

Example usage might be:

python ./python/minknow_api/examples/start_protocol.py \
    --host localhost --position X1 \
    --sample-id "my_sample" --experiment-group "my_group" \
    --experiment-duration 24 \
    --kit SQK-LSK109 \
    --basecalling \
    --fastq --bam

This will start a protocol on position X1 of the local machine, with the sample ID set
to "my_sample" and the run placed in the experiment group "my_group". It will be set to
run for 24 hours. It will assume the sample was prepared using the SQK-LSK109 kit.
Basecalling will be enabled, producing FASTQ and BAM output files.

"""  # noqa W605

import argparse
import logging
from pathlib import Path
import sys
import json

# minknow_api.manager supplies "Manager" a wrapper around MinKNOW's Manager gRPC API with utilities
# for querying sequencing positions + offline basecalling tools.
from enum import Enum
from typing import Sequence

from minknow_api.examples.load_sample_sheet import (
    ParsedSampleSheetEntry,
    SampleSheetParseError,
    load_sample_sheet_csv,
)
from minknow_api.manager import Manager
from minknow_api.protocol_pb2 import AnalysisWorkflowRequest

# We need `find_protocol` to search for the required protocol given a kit + product code.
from minknow_api.tools import protocols


def _load_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def parse_args():
    """Build and execute a command line argument for starting a protocol.

    Returns:
        Parsed arguments to be used when starting a protocol.
    """

    parser = argparse.ArgumentParser(
        description="""
        Run a sequencing protocol in a running MinKNOW instance.
        """
    )

    parser.add_argument(
        "--host",
        default="localhost",
        help="IP address of the machine running MinKNOW (defaults to localhost)",
    )
    parser.add_argument(
        "--port",
        help="Port to connect to on host (defaults to standard MinKNOW port based on tls setting)",
    )
    parser.add_argument(
        "--api-token",
        default=None,
        help="Specify an API token to use, should be returned from the sequencer as a developer API token.",
    )
    parser.add_argument(
        "--client-cert-chain",
        type=_load_file,
        default=None,
        help="Path to a PEM-encoded X.509 certificate chain for client authentication.",
    )
    parser.add_argument(
        "--client-key",
        type=_load_file,
        default=None,
        help="Path to a PEM-encoded private key for client certificate authentication.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    parser.add_argument("--sample-id", help="sample ID to set")
    parser.add_argument(
        "--experiment-group",
        "--group-id",
        help="experiment group (aka protocol group ID) to set",
    )

    position_args = parser.add_mutually_exclusive_group(required=True)
    position_args.add_argument(
        "--position",
        help="position on the machine (or MinION serial number) to run the protocol at. "
        "(specify this or --flow-cell-id or --sample-sheet)",
    )
    position_args.add_argument(
        "--flow-cell-id",
        metavar="FLOW-CELL-ID",
        help="ID of the flow-cell on which to run the protocol. "
        "(specify this or --position or --sample-sheet)",
    )

    parser.add_argument(
        "--kit",
        required=True,
        help="Sequencing kit used with the flow-cell, eg: SQK-LSK108",
    )
    parser.add_argument(
        "--product-code",
        help="Override the product-code stored on the flow-cell and previously user-specified "
        "product-codes",
    )
    parser.add_argument(
        "--config-name",
        help="Script name hint, if using custom configs when sequencing.",
    )

    # SAMPLE SHEET
    position_args.add_argument(
        "--sample-sheet",
        help="Filename of CSV sample sheet. "
        "(specify this or --position or --flow-cell-id)",
    )

    # BASECALL ARGUMENTS
    parser.add_argument(
        "--basecalling",
        action="store_true",
        help="enable base-calling using the default base-calling model",
    )

    parser.add_argument(
        "--basecall-config",
        help="specify the base-calling config and enable base-calling",
    )

    # BARCODING ARGUMENTS
    parser.add_argument(
        "--barcoding",
        action="store_true",
        help="protocol uses barcoding",
    )
    parser.add_argument(
        "--barcode-kits",
        nargs="+",
        help="bar-coding expansion kits used in the experiment",
    )
    parser.add_argument(
        "--trim-barcodes",
        action="store_true",
        help="enable bar-code trimming",
    )
    parser.add_argument(
        "--barcodes-both-ends",
        action="store_true",
        help="bar-code filtering (both ends of a strand must have a matching barcode)",
    )

    # ALIGNMENT ARGUMENTS
    parser.add_argument(
        "--alignment-reference",
        help="Specify alignment reference to send to basecaller for live alignment.",
    )
    parser.add_argument(
        "--bed-file",
        help="Specify bed file to send to basecaller.",
    )

    # Output arguments
    parser.add_argument(
        "--fastq",
        action="store_true",
        help="enables FastQ file output.",
    )

    parser.add_argument(
        "--fastq-reads-per-file",
        type=int,
        help="set the number of reads combined into one FastQ file.",
    )

    parser.add_argument(
        "--fastq-batch-duration",
        type=int,
        help="Duration (in seconds) of a single fastq file batch; if set to 0, time-based batching is disabled",
    )

    parser.add_argument(
        "--fast5",
        action="store_true",
        help="enables Fast5 file output, this will store raw, fastq and trace-table data.",
    )

    parser.add_argument(
        "--fast5-reads-per-file",
        type=int,
        help="set the number of reads combined into one Fast5 file.",
    )

    parser.add_argument(
        "--fast5-batch-duration",
        type=int,
        help="Duration (in seconds) of a single fast5 file batch; if set to 0, time-based batching is disabled",
    )

    parser.add_argument(
        "--pod5",
        action="store_true",
        help="enables Pod5 file output, this will store raw data.",
    )

    parser.add_argument(
        "--pod5-reads-per-file",
        type=int,
        help="set the number of reads combined into one Pod5 file.",
    )

    parser.add_argument(
        "--pod5-batch-duration",
        type=int,
        help="Duration (in seconds) of a single pod5 file batch; if set to 0, time-based batching is disabled",
    )

    parser.add_argument(
        "--bam",
        action="store_true",
        help="enables BAM file output.",
    )

    parser.add_argument(
        "--bam-reads-per-file",
        type=int,
        help="set the number of reads combined into one bam file.",
    )

    parser.add_argument(
        "--bam-batch-duration",
        type=int,
        help="Duration (in seconds) of a single bam file batch; if set to 0, time-based batching is disabled",
    )

    # Read until
    parser.add_argument(
        "--read-until-reference",
        type=str,
        help="Reference file to use in read until",
    )

    parser.add_argument(
        "--read-until-bed-file",
        type=str,
        help="Bed file to use in read until",
    )

    parser.add_argument(
        "--read-until-filter",
        type=str,
        choices=["deplete", "enrich"],
        help="Filter type to use in read until",
    )

    # Experiment
    parser.add_argument(
        "--experiment-duration",
        type=float,
        default=72,
        help="time spent sequencing (in hours)",
    )

    parser.add_argument(
        "--mux-scan-period",
        type=float,
        default=1.5,
        help="number of hours before a mux scan takes place, enables active-channel-selection, "
        "ignored for Flongle flow-cells",
    )

    parser.add_argument(
        "--simulation",
        type=Path,
        help="Bulk file to use for play back",
    )

    # Can either use a JSON file or a JSON string for workflow arguments
    workflow_args = parser.add_mutually_exclusive_group()
    workflow_args.add_argument(
        "--workflow_json_file",
        type=Path,
        help="Input JSON file to use for analysis workflow request",
    )
    workflow_args.add_argument(
        "--workflow_json_string",
        type=str,
        help="Input JSON string to use for analysis workflow request",
    )

    parser.add_argument(
        "extra_args",
        metavar="ARGS",
        nargs="*",
        help="Additional arguments passed verbatim to the protocol script",
    )

    args = parser.parse_args()

    # Read until must have a reference and a filter type, if enabled:
    if (
        args.read_until_filter is not None
        or args.read_until_reference is not None
        or args.read_until_bed_file is not None
    ):
        if args.read_until_filter is None:
            parser.error(
                "Unable to specify read until arguments without a filter type."
            )

        if args.read_until_reference is None:
            parser.error(
                "Unable to specify read until arguments without a reference type."
            )

    if args.bed_file and not args.alignment_reference:
        parser.error("Unable to specify `--bed-file` without `--alignment-reference`.")

    if (args.barcoding or args.barcode_kits) and not (
        args.basecalling or args.basecall_config
    ):
        parser.error(
            "Unable to specify `--barcoding` or `--barcode-kits` without `--basecalling`."
        )

    if args.alignment_reference and not (args.basecalling or args.basecall_config):
        parser.error(
            "Unable to specify `--alignment-reference` without `--basecalling`."
        )

    if not (args.fast5 or args.pod5 or args.bam or args.fastq):
        print("No output (fast5, pod5, bam or fastq) specified")
        # not fatal, just warning the user

    if (args.client_cert_chain is None) != (args.client_key is None):
        parser.error(
            "--client-cert-chain and --client-key must either both be provided, or neither"
        )

    return args


class PositionKeyType(Enum):
    PositionId = 1
    FlowCellId = 2


class ExperimentSpec(object):
    def __init__(self, entry: ParsedSampleSheetEntry):
        self.entry = entry
        self.position = None
        self.protocol_id = ""


ExperimentSpecs = Sequence[ExperimentSpec]


# Add sample sheet entry info to experiment_specs
def add_sample_sheet_entries(experiment_specs: ExperimentSpecs, args):
    if args.sample_sheet:
        if args.position:
            raise ValueError(
                "has position and sample_sheet, but these are mutually exclusive"
            )
        if args.flow_cell_id:
            raise ValueError(
                "has flow_cell_id and sample_sheet, but these are mutually exclusive"
            )
        try:
            sample_sheet = load_sample_sheet_csv(args.sample_sheet)
        except SampleSheetParseError as e:
            print("Error loading sample sheet CSV: {}".format(e))
            sys.exit(1)
        except FileNotFoundError:
            print("Sample sheet file not found: {}".format(args.sample_sheet))
            sys.exit(1)

        for entry in sample_sheet:

            # Fix up the `sample_id` and `experiment_id` with values supplied on the command line
            # (provided they don't clash with sample sheet values)
            if args.sample_id:
                if entry.sample_id and args.sample_id != entry.sample_id:
                    print(
                        "`--sample-id` specified on command line does not match `sample_id` specified in sample sheet"
                    )
                    sys.exit(1)
                else:
                    sample_id = args.sample_id
            else:
                sample_id = entry.sample_id

            if args.experiment_group:
                if entry.experiment_id and args.experiment_group != entry.experiment_id:
                    print(
                        "`--experiment-group` specified on command line does not match `experiment_id` specified in sample sheet"
                    )
                    sys.exit(1)
                else:
                    experiment_id = args.experiment_group
            else:
                experiment_id = entry.experiment_id

            # Check that we have exactly one of `position_id` and `flow_cell_id`
            if entry.position_id and entry.flow_cell_id:
                raise ValueError(
                    "There is not exactly one of position_id and flow_cell_id"
                )

            # Add the entry to the specs
            experiment_specs.append(
                ExperimentSpec(
                    entry=ParsedSampleSheetEntry(
                        flow_cell_id=entry.flow_cell_id,
                        position_id=entry.position_id,
                        sample_id=sample_id,
                        experiment_id=experiment_id,
                        barcode_info=entry.barcode_info,
                    )
                )
            )

    elif args.position:
        if args.sample_sheet:
            raise ValueError(
                "has sample_sheet and position, but these are mutually exclusive"
            )
        if args.flow_cell_id:
            raise ValueError(
                "has flow_cell_id and position, but these are mutually exclusive"
            )

        experiment_specs.append(
            ExperimentSpec(
                entry=ParsedSampleSheetEntry(
                    flow_cell_id=None,
                    position_id=args.position,
                    sample_id=args.sample_id,
                    experiment_id=args.experiment_group,
                    barcode_info=None,
                )
            )
        )

    elif args.flow_cell_id:
        if args.sample_sheet:
            raise ValueError(
                "has sample_sheet and flow_cell_id, but these are mutually exclusive"
            )
        if args.position:
            raise ValueError(
                "has position and flow_cell_id, but these are mutually exclusive"
            )
        experiment_specs.append(
            ExperimentSpec(
                entry=ParsedSampleSheetEntry(
                    flow_cell_id=args.flow_cell_id,
                    position_id=None,
                    sample_id=args.sample_id,
                    experiment_id=args.experiment_group,
                    barcode_info=None,
                )
            )
        )
    else:
        print(
            "No sample position specified; specify either `--position`, `--flow-cell-id` or `--sample-sheet`"
        )
        sys.exit(1)


# Determine whether to look up positions by position name or by flow_cell_id
def determine_position_key_type(experiment_specs: ExperimentSpecs) -> PositionKeyType:
    if all(spec.entry.position_id for spec in experiment_specs):
        if any(spec.entry.flow_cell_id for spec in experiment_specs):
            raise ValueError(
                "flow_cell_id in experiment_specs despite look-up by position_id"
            )
        return PositionKeyType.PositionId
    elif all(spec.entry.flow_cell_id for spec in experiment_specs):
        if any(spec.entry.position_id for spec in experiment_specs):
            raise ValueError(
                "position_id in experiment_specs despite look-up by flow_cell_id"
            )
        return PositionKeyType.FlowCellId
    else:
        # Could not determine what to look up by
        # This should not occur
        raise ValueError("Neither position_id nor flow_cell_id in experiment_specs")


# Check if any spec has requested to be started on the supplied position
# If it has, then store that position in the spec for later use
def add_position_to_specs(
    experiment_specs: ExperimentSpecs, position, position_key_type
):
    # Look up by position_id or by flow_cell_id

    if position_key_type is PositionKeyType.PositionId:
        matches = [
            spec for spec in experiment_specs if spec.entry.position_id == position.name
        ]
    elif position_key_type is PositionKeyType.FlowCellId:
        # Get the flow cell info for the position
        position_connection = position.connect()
        flow_cell_info = position_connection.device.get_flow_cell_info()
        if not flow_cell_info:
            # No flow cell in the position; cannot look up by flow_cell_id
            return
        matches = [
            spec
            for spec in experiment_specs
            if (spec.entry.flow_cell_id == flow_cell_info.flow_cell_id)
            or (spec.entry.flow_cell_id == flow_cell_info.user_specified_flow_cell_id)
        ]
    else:
        # Should not happen - only two options for PositionKeyType
        raise ValueError("PositionKeyType is neither PositionID nor FlowCellId")

    if not matches:
        # No requests to start any experiments on this position
        return

    if len(matches) > 1:
        # Too many matches; error
        # May occur if the user_specified_flow_cell_id for one flow cell matches the flow_cell_id for another flow cell
        print("Trying to start multiple experiments on the same flow cell")
        sys.exit(1)

    # Add the current position to the matched entries
    matches[0].position = position


# Add position info to the experiment_specs
def add_position_info(experiment_specs, manager):
    position_key_type = determine_position_key_type(experiment_specs)
    positions = manager.flow_cell_positions()
    for position in positions:
        add_position_to_specs(experiment_specs, position, position_key_type)

    # Check that we added a position to all experiment specs
    # Fail with an error if we couldn't find any positions
    if not all(spec.position for spec in experiment_specs):
        print("Could not find all specified positions:")
        print(
            "\n".join(
                "\t{}".format(spec.entry.position_id or spec.entry.flow_cell_id)
                for spec in experiment_specs
                if not spec.position
            )
        )
        sys.exit(1)


# Determine which protocol to run for each experiment, and add its ID to experiment_specs
def add_protocol_ids(experiment_specs, args):
    for spec in experiment_specs:
        # Connect to the sequencing position:
        position_connection = spec.position.connect()

        # Check if a flowcell is available for sequencing
        flow_cell_info = position_connection.device.get_flow_cell_info()
        if not flow_cell_info.has_flow_cell:
            print("No flow cell present in position {}".format(spec.position))
            sys.exit(1)

        # Select product code:
        if args.product_code:
            product_code = args.product_code
        else:
            product_code = flow_cell_info.user_specified_product_code
            if not product_code:
                product_code = flow_cell_info.product_code

        # Find the protocol identifier for the required protocol:
        protocol_info = protocols.find_protocol(
            position_connection,
            product_code=product_code,
            kit=args.kit,
            config_name=args.config_name,
            basecalling=args.basecalling,
            basecall_config=args.basecall_config,
            barcoding=args.barcoding,
            barcoding_kits=args.barcode_kits,
        )

        if not protocol_info:
            print("Failed to find protocol for position %s" % (spec.position))
            print("Requested protocol:")
            print("  product-code: %s" % args.product_code)
            print("  kit: %s" % args.kit)
            print("  basecalling: %s" % args.basecalling)
            print("  basecall_config: %s" % args.basecall_config)
            print("  barcode-kits: %s" % args.barcode_kits)
            print("  barcoding: %s" % args.barcoding)
            print("  config-name: %s" % args.config_name)
            sys.exit(1)

        # Store the identifier for later:
        spec.protocol_id = protocol_info.identifier


def main():
    """Entrypoint to start protocol example"""
    # Parse arguments to be passed to started protocols:
    args = parse_args()

    def _make_request(request_body):
        req = json.loads(request_body)

        # check request_body is valid
        if "workflow_id" not in req or "parameters" not in req:
            raise ValueError("Request body does not contain valid data.")

        # convert string to protobuf
        workflow_params = AnalysisWorkflowRequest()
        workflow_params.proxy_request.api = "/workflow_instances/start"
        workflow_params.proxy_request.request_body = request_body
        return workflow_params

    # parse json analysis workflow data from input file
    analysis_workflow_request = None
    if args.workflow_json_file:
        request_body = args.workflow_json_file.read_text()
        analysis_workflow_request = _make_request(request_body)

    # parse json analysis workflow data from input string
    if args.workflow_json_string:
        analysis_workflow_request = _make_request(args.workflow_json_string)

    # Specify --verbose on the command line to get extra details about the actions performed
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Construct a manager using the host + port provided:
    manager = Manager(
        host=args.host,
        port=args.port,
        developer_api_token=args.api_token,
        client_certificate_chain=args.client_cert_chain,
        client_private_key=args.client_key,
    )

    experiment_specs = []
    add_sample_sheet_entries(experiment_specs, args)
    add_position_info(experiment_specs, manager)
    add_protocol_ids(experiment_specs, args)

    # Build arguments for starting protocol:
    basecalling_args = None
    if args.basecalling or args.basecall_config:
        barcoding_args = None
        alignment_args = None
        if args.barcode_kits or args.barcoding:
            barcoding_args = protocols.BarcodingArgs(
                args.barcode_kits,
                args.trim_barcodes,
                args.barcodes_both_ends,
            )

        if args.alignment_reference:
            alignment_args = protocols.AlignmentArgs(
                reference_files=[args.alignment_reference],
                bed_file=args.bed_file,
            )

        basecalling_args = protocols.BasecallingArgs(
            config=args.basecall_config,
            barcoding=barcoding_args,
            alignment=alignment_args,
        )

    read_until_args = None
    if args.read_until_filter:
        read_until_args = protocols.ReadUntilArgs(
            filter_type=args.read_until_filter,
            reference_files=[args.read_until_reference],
            bed_file=args.read_until_bed_file,
            first_channel=None,  # These default to all channels.
            last_channel=None,
        )

    def build_output_arguments(args, name):
        if not getattr(args, name):
            return None
        return protocols.OutputArgs(
            reads_per_file=getattr(args, "%s_reads_per_file" % name, None),
            batch_duration=getattr(args, "%s_batch_duration" % name, None),
        )

    fastq_arguments = build_output_arguments(args, "fastq")
    fast5_arguments = build_output_arguments(args, "fast5")
    pod5_arguments = build_output_arguments(args, "pod5")
    bam_arguments = build_output_arguments(args, "bam")

    # Now start the protocol(s):
    print("Starting protocol on %s positions" % len(experiment_specs))
    for spec in experiment_specs:
        position_connection = spec.position.connect()

        # Set up user specified product code if requested:
        if args.product_code:
            position_connection.device.set_user_specified_product_code(
                code=args.product_code
            )

        # Generate stop criteria for use by Run Until
        # The `runtime` is in seconds, while the `experiment_duration` is in hours
        stop_criteria = protocols.CriteriaValues(
            runtime=int(args.experiment_duration * 60 * 60)
        )

        run_id = protocols.start_protocol(
            position_connection,
            identifier=spec.protocol_id,
            sample_id=spec.entry.sample_id,
            experiment_group=spec.entry.experiment_id,
            barcode_info=spec.entry.barcode_info,
            basecalling=basecalling_args,
            read_until=read_until_args,
            fastq_arguments=fastq_arguments,
            fast5_arguments=fast5_arguments,
            pod5_arguments=pod5_arguments,
            bam_arguments=bam_arguments,
            analysis_workflow_request=analysis_workflow_request,
            disable_active_channel_selection=False,
            mux_scan_period=args.mux_scan_period,
            stop_criteria=stop_criteria,
            simulation_path=args.simulation,
            args=args.extra_args,  # Any extra args passed.
        )

        flow_cell_info = position_connection.device.get_flow_cell_info()

        print("Started protocol:")
        print("    run_id={}".format(run_id))
        print("    position={}".format(spec.position.name))
        print("    flow_cell_id={}".format(flow_cell_info.flow_cell_id))
        print(
            "    user_specified_flow_cell_id={}".format(
                flow_cell_info.user_specified_flow_cell_id
            )
        )


if __name__ == "__main__":
    main()
