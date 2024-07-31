"""
Example script to extract protocol yield

Example usage might be (to dump the statistics for the most recent protocol):

```
> python ./python/minknow_api/examples/extract_run_statistics.py --host localhost --position X1
```

This script generates a set of files in the current dir summarising acquisition output for the most recent protocol run on X1.

"""

import argparse
import logging
import sys
from pathlib import Path

import grpc

import minknow_api.statistics_pb2

# minknow_api.manager supplies "Manager" a wrapper around MinKNOW's Manager gRPC API with utilities
# for querying sequencing positions + offline basecalling tools.
from minknow_api.manager import Manager


def dump_statistics_for_acquisition(connection, acquisition_run_id, output_dir):
    """Extract any acquisition output information about `acquisition_run_id`, and write a report into `output_dir`."""

    def do_title(title_str, title_char):
        """Format a markdown title for `title_str`"""
        return title_str + "\n" + title_char * len(title_str) + "\n\n"

    def format_filter_group(filter_group):
        """Find a descriptive string for `filter_group`."""
        return "barcode: %s, alignment_reference: %s" % (
            filter_group.barcode_name,
            filter_group.alignment_reference,
        )

    # Invoke the API to get a stream of acquisition output results:
    #
    # Request snapshots each hour, and ensure data is split on
    # alignment reference and barcode name.
    stream = connection.statistics.stream_acquisition_output(
        acquisition_run_id=acquisition_run_id,
        data_selection=minknow_api.statistics_pb2.DataSelection(step=60 * 60),
        split=minknow_api.statistics_pb2.AcquisitionOutputSplit(
            alignment_reference=True,
            barcode_name=True,
        ),
    )

    report = do_title("Acquisition report", "=")

    # Now iterate the stream and summarise each bucket as markdown
    for filter_groups in stream:
        for filter_group in filter_groups.snapshots:
            # Find a title for this filter group:
            report += do_title(
                "Output snapshots for "
                + " and ".join(
                    format_filter_group(grp) for grp in filter_group.filtering
                ),
                "-",
            )

            report += (
                "\t".join(
                    [
                        "Timestamp(s)",
                        "Passed Called reads",
                        "Failed Reads",
                        "Basecalled samples",
                    ]
                )
                + "\n"
            )
            # Generate per snapshot summaries (one per line):
            #
            # See `acquisition.AcquisitionYieldSummary` in acquisition.proto for other fields that could be queried here.
            for snapshot in filter_group.snapshots:
                cells = [
                    snapshot.seconds,  # timestamp(s)
                    snapshot.yield_summary.basecalled_pass_read_count,  # Passed Called reads
                    snapshot.yield_summary.basecalled_fail_read_count,  # Failed reads
                    snapshot.yield_summary.basecalled_samples,  # Total samples passed through the basecaller
                ]

                report += "\t".join(str(c) for c in cells) + "\n"

            report += "\n"

    with open(
        str(output_dir / ("acquisition_output_%s.md" % acquisition_run_id)), "w"
    ) as file:
        file.write(report)


def _load_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def main():
    """Entrypoint to extract run statistics example"""
    # Parse arguments to be passed to started protocols:
    parser = argparse.ArgumentParser(
        description="""
        Collect statistics from an existing protocol.
        """
    )

    parser.add_argument(
        "--host",
        default="localhost",
        help="IP address of the machine running MinKNOW (defaults to localhost)",
    )
    parser.add_argument(
        "--port",
        help="Port to connect to on host (defaults to standard MinKNOW port)",
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
    parser.add_argument(
        "--position",
        help="position on the machine (or MinION serial number) to run the protocol at",
        required=True,
    )
    parser.add_argument(
        "--protocol",
        help="Extract information for a specific protocol run-id (eg. 04462a44-eed3-4550-af0d-bc9683352583 returned form protocol.list_protocol_runs). Defaults to last run protocol.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./"),
        help="Directory to write extracted info to. Defaults to current directory.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if (args.client_cert_chain is None) != (args.client_key is None):
        parser.error(
            "--client-cert-chain and --client-key must either both be provided, or neither"
        )

    # Specify --verbose on the command line to get extra details about
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

    # Find which positions we are going to start protocol on:
    positions = list(manager.flow_cell_positions())
    filtered_positions = list(filter(lambda pos: pos.name == args.position, positions))

    # Find the position we were asked to interrogate:
    if not filtered_positions:
        print(
            "Failed to find position %s in available positions '%s'"
            % (args.position, ", ".join([p.name for p in positions]))
        )
        exit(1)

    # Connect to the grpc port for the position:
    connection = filtered_positions[0].connect()

    # Find the protoocol id we are going to query (or the most recent if not specified):
    protocol_id = args.protocol
    if not protocol_id:
        protocols = connection.protocol.list_protocol_runs()
        if not protocols.run_ids:
            print(
                "%s has no protocols available to extract statistics" % args.position,
                file=sys.stderr,
            )
            sys.exit(1)
        protocol_id = protocols.run_ids[-1]

    # Find the correct acquisition run to query:
    try:
        run_info = connection.protocol.get_run_info(run_id=protocol_id)
    except grpc.RpcError:
        print("Failed to get protocol info for id '%s'" % protocol_id, file=sys.stderr)
        sys.exit(1)

    if not run_info.acquisition_run_ids:
        print("No acquisition info for protocol id '%s'" % protocol_id, file=sys.stderr)
        sys.exit(1)

    interesting_acquisition_id = run_info.acquisition_run_ids[-1]

    # Last acquisition period will contain any sequencing.
    #
    # The first acquisition may be a calibration (if required), then the sequencing run is next.
    dump_statistics_for_acquisition(
        connection, interesting_acquisition_id, args.output_dir
    )


if __name__ == "__main__":
    main()
