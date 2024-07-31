"""
Example script to wait for a protocol to finish, and perform user-specified actions

Example usage might be:

python ./python/minknow_api/examples/run_after_protocol.py \
    --host localhost --position X1 \
    --run-id "my_run" \
    --script-to-run "my_script.sh"

This will run ``my_script.sh`` after the run ``my_run`` has finished on position X1 of
the local machine.

"""  # noqa W605

import argparse
import logging
import os
import sys

import grpc

# minknow_api.manager supplies "Manager" a wrapper around MinKNOW's Manager gRPC API with utilities
# for querying sequencing positions + offline basecalling tools.
from minknow_api.manager import Manager


def _load_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def parse_args():
    """Build and execute a command line argument for running a script after the

    Returns:
        Parsed arguments to be used when starting a protocol.
    """

    parser = argparse.ArgumentParser(
        description="""
        Wait for a protocol to finish on a single position, and then run a user-specified script"
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
        type=int,
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

    # Sequencing position can be identified by a position name, or a flowcell ID
    position_group = parser.add_mutually_exclusive_group(required=True)
    position_group.add_argument(
        "--position",
        help="position on the machine (or MinION serial number) to run the protocol at",
    )
    position_group.add_argument(
        "--flow-cell-id",
        metavar="FLOW-CELL-ID",
        help="ID of the flow-cell on which to run the protocol. (specify this or --position)",
    )

    parser.add_argument(
        "--run-id",
        required=True,
        help="ID of the protocol run.",
    )

    parser.add_argument(
        "--script-to-run",
        help="Script to run once the protocol has finished. If no script is specified, then the final status of the protocol will be displayed before finishing.",
    )

    args = parser.parse_args()

    # Further argument checks

    if (args.client_cert_chain is None) != (args.client_key is None):
        parser.error(
            "--client-cert-chain and --client-key must either both be provided, or neither"
        )

    # Check the script exists
    if args.script_to_run and not os.path.isfile(args.script_to_run):
        print(f"The script {args.script_to_run} was not found", file=sys.stderr)
        exit(1)

    return args


def is_position_selected(position, args):
    """Find if the {position} is selected by command line arguments {args}."""

    # First check for name match:
    if args.position == position.name:
        print(f"Found position {position}")
        return True

    # If no position name match is found, see if the flowcell ID can be matched
    try:
        connected_position = position.connect()
        if args.flow_cell_id is not None:
            flow_cell_info = connected_position.device.get_flow_cell_info()
            if (
                flow_cell_info.user_specified_flow_cell_id == args.flow_cell_id
                or flow_cell_info.flow_cell_id == args.flow_cell_id
            ):
                print(f"Found flow cell {args.flow_cell_id}")
                return True
    except (grpc.RpcError, RuntimeError):
        print(f"Failed to connect to position {position.name}")

    return False


def main():
    """Entrypoint to run-after-protocol example"""
    # Parse arguments to be passed to started protocols:
    args = parse_args()

    # Specify --verbose on the command line to get extra details about the actions performed
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Construct a manager using the host + port provided:
    manager = Manager(
        host=args.host, port=args.port, developer_api_token=args.api_token
    )

    # Find on which position we are going to wait for the protocol to finish:
    positions = manager.flow_cell_positions()
    filtered_positions = list(
        filter(lambda pos: is_position_selected(pos, args), positions)
    )

    # A single position must be selected:
    if not filtered_positions:
        print(
            "No sequencing position could be found that matches the specified position name or flow-cell ID."
        )
        sys.exit(1)

    # Connect to the sequencing position:
    pos = filtered_positions[0]
    position_connection = pos.connect()

    # Obtain the interface to the protocol RPC service
    protocol_service = position_connection.protocol

    # Wait for the specified protocol to finish, and obtain details
    # about the run.
    run_info = protocol_service.wait_for_finished(run_id=args.run_id)

    # Determine the final state of the protocol run.  These states are
    # defined in the protocol RPC definition.
    if run_info.state == protocol_service._pb.PROTOCOL_COMPLETED:
        print("Protocol finished successfully")
    else:
        print(
            f"Protocol did not finish successfully, with code {protocol_service._pb.ProtocolState.Name(run_info.state)}. "
            "No further actions will be taken"
        )
        sys.exit(1)

    # If a script was specified, run it.
    if args.script_to_run:
        print(f"Running the following command: {args.script_to_run}")
        os.system(args.script_to_run)  # nosec B605


if __name__ == "__main__":
    main()
