"""
Example script to start a protocol

Example usage might be:

python ./python/examples/start_protocol.py \
    --host localhost --position X1 \                        # Select which host + position will run a script
    --sample-id "my_sample" --experiment-group "my_group" \ # Set sample id + experiment group
    --experiment-duration 24 \                              # Set the run time of the experiment
    --kit SQK-LSK109 \                                      # Specify which kit is being run
    --basecalling \                                         # Enable basecalling
    --fastq --bam                                           # Choose fastq + bam output options

"""

import argparse
import logging
import sys

# minknow_api.manager supplies "Manager" a wrapper around MinKNOW's Manager gRPC API with utilities
# for querying sequencing positions + offline basecalling tools.
from minknow_api.manager import Manager

# We need `find_protocol` to search for the required protocol given a kit + product code.
from minknow_api.tools import protocols


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
        "--port", help="Port to connect to on host (defaults to standard MinKNOW port)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    parser.add_argument("--sample-id", help="sample ID to set")
    parser.add_argument(
        "--experiment-group",
        "--group-id",
        help="experiment group (aka protocol group ID) to set",
    )
    parser.add_argument(
        "--position",
        help="position on the machine (or MinION serial number) to run the protocol at",
    )
    parser.add_argument(
        "--flow-cell-id",
        metavar="FLOW-CELL-ID",
        help="ID of the flow-cell on which to run the protocol. (specify this or --position)",
    )

    parser.add_argument(
        "--kit",
        required=True,
        help="Sequencing kit used with the flow-cell, eg: SQK-LSK108",
    )
    parser.add_argument(
        "--product-code",
        help="Override the product-code stored on the flow-cell and previously user-specified"
        "product-codes",
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
        "--barcoding", action="store_true", help="protocol uses barcoding",
    )
    parser.add_argument(
        "--barcode-kits",
        nargs="+",
        help="bar-coding expansion kits used in the experiment",
    )
    parser.add_argument(
        "--trim-barcodes", action="store_true", help="enable bar-code trimming",
    )
    parser.add_argument(
        "--barcodes-both-ends",
        action="store_true",
        help="bar-code filtering (both ends of a strand must have a matching barcode)",
    )

    parser.add_argument(
        "--detect-mid-strand-barcodes",
        action="store_true",
        help="bar-code filtering for bar-codes in the middle of a strand",
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="read selection based on bar-code accuracy",
    )

    parser.add_argument(
        "--min-score-rear",
        type=float,
        default=0.0,
        help="read selection based on bar-code accuracy",
    )

    parser.add_argument(
        "--min-score-mid",
        type=float,
        default=0.0,
        help="read selection based on bar-code accuracy",
    )

    # ALIGNMENT ARGUMENTS
    parser.add_argument(
        "--alignment-reference",
        help="Specify alignment reference to send to basecaller for live alignment.",
    )
    parser.add_argument(
        "--bed-file", help="Specify bed file to send to basecaller.",
    )

    # Output arguments
    parser.add_argument(
        "--fastq",
        action="store_true",
        help="enables FastQ file output, defaulting to 4000 reads per file",
    )

    parser.add_argument(
        "--fastq-reads-per-file",
        type=int,
        default=4000,
        help="set the number of reads combined into one FastQ file.",
    )

    parser.add_argument(
        "--fast5",
        action="store_true",
        help="enables Fast5 file output, defaulting to 4000 reads per file, this will store raw, "
        "fastq and trace-table data",
    )

    parser.add_argument(
        "--fast5-reads-per-file",
        type=int,
        default=4000,
        help="set the number of reads combined into one Fast5 file.",
    )

    parser.add_argument(
        "--bam",
        action="store_true",
        help="enables BAM file output, defaulting to 4000 reads per file",
    )

    parser.add_argument(
        "--bam-reads-per-file",
        type=int,
        default=4000,
        help="set the number of reads combined into one BAM file.",
    )

    # Experiment
    parser.add_argument(
        "--experiment-duration",
        type=float,
        default=72,
        help="time spent sequencing (in hours)",
    )

    parser.add_argument(
        "--no-active-channel-selection",
        action="store_true",
        help="allow dynamic selection of channels to select pores for sequencing, "
        "ignored for Flongle flow-cells",
    )

    parser.add_argument(
        "--mux-scan-period",
        type=float,
        default=1.5,
        help="number of hours before a mux scan takes place, enables active-channel-selection, "
        "ignored for Flongle flow-cells",
    )
    parser.add_argument(
        "extra_args",
        metavar="ARGS",
        nargs="*",
        help="Additional arguments passed verbatim to the protocol script",
    )
    args = parser.parse_args()

    # Further argument checks
    if args.bed_file and not args.alignment_reference:
        print("Unable to specify `--bed-file` without `--alignment-reference`.")
        sys.exit(1)

    if (args.barcoding or args.barcode_kits) and not (
        args.basecalling or args.basecall_config
    ):
        print(
            "Unable to specify `--barcoding` or `--barcode-kits` without `--basecalling`."
        )
        sys.exit(1)

    if args.alignment_reference and not (args.basecalling or args.basecall_config):
        print("Unable to specify `--alignment-reference` without `--basecalling`.")
        sys.exit(1)

    if not (args.fast5 or args.fastq):
        print("No output (fast5 or fastq) specified")

    return args


def is_position_selected(position, args):
    """Find if the {position} is selected by command line arguments {args}."""

    # First check for name match:
    if args.position == position.name:
        return True

    # Then verify if the flow cell matches:
    connected_position = position.connect()
    if args.flow_cell_id is not None:
        flow_cell_info = connected_position.device.get_flow_cell_info()
        if (
            flow_cell_info.user_specified_flow_cell_id == args.flow_cell_id
            or flow_cell_info.flow_cell_id == args.flow_cell_id
        ):
            return True

    return False


def main():
    """Entrypoint to start protocol example"""
    # Parse arguments to be passed to started protocols:
    args = parse_args()

    # Specify --verbose on the command line to get extra details about
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Construct a manager using the host + port provided:
    manager = Manager(host=args.host, port=args.port, use_tls=False)

    # Find which positions we are going to start protocol on:
    positions = manager.flow_cell_positions()
    filtered_positions = list(
        filter(lambda pos: is_position_selected(pos, args), positions)
    )

    # At least one position needs to be selected:
    if not filtered_positions:
        print(
            "No positions selected for protocol - specify `--position` or `--flow-cell-id`"
        )
        sys.exit(1)

    protocol_identifiers = {}
    for pos in filtered_positions:
        # Connect to the sequencing position:
        position_connection = pos.connect()

        # Check if a flowcell is available for sequencing
        flow_cell_info = position_connection.device.get_flow_cell_info()
        if not flow_cell_info.has_flow_cell:
            print("No flow cell present in position %s" % pos)
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
            basecalling=args.basecalling,
            basecall_config=args.basecall_config,
            barcoding=args.barcoding,
            barcoding_kits=args.barcode_kits,
        )

        if not protocol_info:
            print("Failed to find protocol for position %s" % (pos.name))
            print("Requested protocol:")
            print("  product-code: %s" % args.product_code)
            print("  kit: %s" % args.kit)
            print("  basecalling: %s" % args.basecalling)
            print("  basecall_config: %s" % args.basecall_config)
            print("  barcode-kits: %s" % args.barcode_kits)
            print("  barcoding: %s" % args.barcoding)
            sys.exit(1)

        # Store the identifier for later:
        protocol_identifiers[pos.name] = protocol_info.identifier

    # Start protocol on the requested postitions:
    print("Starting protocol on %s positions" % len(filtered_positions))
    for pos in filtered_positions:

        # Connect to the sequencing position:
        position_connection = pos.connect()

        # Find the protocol identifier for the required protocol:
        protocol_identifier = protocol_identifiers[pos.name]

        # Now select which arguments to pass to start protocol:
        print("Starting protocol %s on position %s" % (protocol_identifier, pos.name))

        # Set up user specified product code if requested:
        if args.product_code:
            position_connection.device.set_user_specified_product_code(
                code=args.product_code
            )

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
                    args.detect_mid_strand_barcodes,
                    args.min_score,
                    args.min_score_rear,
                    args.min_score_mid,
                )

            if args.alignment_reference:
                alignment_args = protocols.AlignmentArgs(
                    reference_files=[args.alignment_reference], bed_file=args.bed_file,
                )

            basecalling_args = protocols.BasecallingArgs(
                config=args.basecall_config,
                barcoding=barcoding_args,
                alignment=alignment_args,
            )

        def build_output_arguments(args, name):
            if not getattr(args, name):
                return None
            return protocols.OutputArgs(
                reads_per_file=getattr(args, "%s_reads_per_file" % name)
            )

        fastq_arguments = build_output_arguments(args, "fastq")
        fast5_arguments = build_output_arguments(args, "fast5")
        bam_arguments = build_output_arguments(args, "bam")

        # Now start the protocol:
        run_id = protocols.start_protocol(
            position_connection,
            protocol_identifier,
            sample_id=args.sample_id,
            experiment_group=args.experiment_group,
            basecalling=basecalling_args,
            fastq_arguments=fastq_arguments,
            fast5_arguments=fast5_arguments,
            bam_arguments=bam_arguments,
            disable_active_channel_selection=args.no_active_channel_selection,
            mux_scan_period=args.mux_scan_period,
            args=args.extra_args,  # Any extra args passed.
        )

        print("Started protocol %s" % run_id)


if __name__ == "__main__":
    main()
