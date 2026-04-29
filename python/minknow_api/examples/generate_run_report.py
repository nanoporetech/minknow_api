"""
Example script to export run report JSON information
"""

import argparse
import sys

import grpc
from minknow_api.manager import Manager


def _load_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_data(dest, data):
    # Write to either stdout or a file if a filename is specified.
    if dest:
        try:
            with open(dest, "wt") as f:
                f.write(data)

        except IOError as e:
            print(f'Unable to open "{dest}" for writing: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        # Write to stdout
        print(data)


def main():
    # Define the command-line arguments.  The parser module will extract the user's values and place them in
    # variables named after the options.
    parser = argparse.ArgumentParser(
        description="""
        Export run report JSON information.
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
        help="Specify an API token to use, should be returned from the sequencer as a developer API token. This can only be left unset if there is a local token available.",
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
        default=None,
        help="Restrict results to those ran on a position on the machine (or MinION serial number)",
    )
    parser.add_argument(
        "--protocol",
        required=True,
        help="Extract information for a specific protocol run-id (eg. 04462a44-eed3-4550-af0d-bc9683352583 returned from protocol.list_protocol_runs)",
    )
    parser.add_argument(
        "-j",
        "--json",
        default=False,
        action="store_true",
        help="Output the run report json source data, instead of html",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Send output to a file instead of stdout.",
    )
    args = parser.parse_args()

    if (args.client_cert_chain is None) != (args.client_key is None):
        parser.error(
            "--client-cert-chain and --client-key must either both be provided, or neither"
        )

    # Try and connect to the minknow-core manager passing the host, port and developer-api token.  If the Python code
    # can't connect it will throw, catch the exception and exit with an error message.
    try:
        manager = Manager(
            host=args.host,
            port=args.port,
            developer_api_token=args.api_token,
            client_certificate_chain=args.client_cert_chain,
            client_private_key=args.client_key,
        )
    except Exception:
        port = f":{args.port}" if args.port else ""
        print(f"Unable to connect to MinKNOW at {args.host}{port}", file=sys.stderr)
        exit(1)

    # Get the sequencing positions. Convert the iterable object returned into a list enabling iteratating over the
    # contents multiple times.
    reported_positions = list(manager.flow_cell_positions())
    if not reported_positions:
        print("No sequencing positions reported", file=sys.stderr)
        exit(1)

    # If a position has been specified on the command-line, filter out all the positions which don't contain the
    # specified text in their name.
    if args.position:
        # Do the filtering
        positions = [pos for pos in reported_positions if args.position in pos.name]
        if not positions:
            print("No positions in the list :", file=sys.stderr)
            for pos in reported_positions:
                print(f"    {pos.name}", file=sys.stderr)
            print(
                f"matched your required position name {args.position}", file=sys.stderr
            )
            exit(1)
    else:
        positions = reported_positions

    found_protocol = False
    # loop through all the positions that matched the filter
    for pos in positions:
        # Connect to the position and get a list of all the protocols run on that position, these are provided as
        # Run-IDs.
        connection = pos.connect()
        list_runs_response = connection.protocol.list_protocol_runs()

        matching_protocol_run_ids = [
            run_id
            for run_id in list_runs_response.run_ids
            if run_id.lower().startswith(args.protocol.lower())
        ]

        if not matching_protocol_run_ids:
            # Not found on this position, try the next one
            continue

        if len(matching_protocol_run_ids) > 1:
            print(
                "Multiple protocols matched the protocol id '%s' on position '%s', please be more specific"
                % (args.protocol, pos.name),
                file=sys.stderr,
            )
            sys.exit(1)

        found_protocol = True
        matching_protocol_run_id = matching_protocol_run_ids[0]

        try:
            if not args.json:
                stream = connection.protocol.generate_run_report(
                    protocol_run_id=matching_protocol_run_id,
                    include_input_data=False,
                )

                report_data = "".join(msg.report_data for msg in stream)
                write_data(args.output, report_data)

            else:
                stream = connection.protocol.generate_run_report(
                    protocol_run_id=matching_protocol_run_id,
                    include_input_data=True,
                )

                json_report_data = "".join(msg.input_data for msg in stream)
                write_data(args.output, json_report_data)
        except grpc.RpcError as e:
            print(
                "Failed to generate run_report for protocol '%s': %s"
                % (args.protocol, e),
                file=sys.stderr,
            )

        # Found the protocol and written the data -- all done
        break

    if not found_protocol:
        print("Failed to find protocol '%s'" % args.protocol, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
