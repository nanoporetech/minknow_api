""" Add, remove and list simulated devices.

This can be run with the Python environment shipped with minknow-core, or any python environment with the minknow_api installed in it.
"""

import argparse
import sys
import time

from grpc import RpcError

import minknow_api
from minknow_api.manager import Manager


def _load_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def parse_arguments():
    """Parse command-line options"""
    parser = argparse.ArgumentParser(
        description="""Dynamically create and destroy simulated devices.
        Running the script with no arguments will add a sensibly chosen flowcell type with a sensible default name.
        It is also possible to list or remove simulated devices, using --list or --remove.

        Example usage:
        python manage_simulated_devices.py

        python manage_simulated_devices.py --add

        """
    )

    parser.add_argument(
        "--host",
        default="localhost",
        help="IP address of the machine running MinKNOW (defaults to localhost)",
    )
    parser.add_argument(
        "--port",
        help="Override the port to connect to MinKNOW",
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

    device_group = parser.add_mutually_exclusive_group()
    device_group.add_argument(
        "--prom",
        "-p",
        action="store_true",
        help="Add a simulated PromethION flow cell. If adding a simulated PromethION flow cell and providing a name, please ensure the name follows the LN naming convention, where L is an uppercase letter and N is a single digit number.",
    )
    device_group.add_argument(
        "--p2",
        action="store_true",
        help='Add a simulated P2 flow cell. If adding a simulated P2 flow cell and providing a name, please use either "P2S_" followed by five digits, and then "-A" or "-B" eg: "P2S_000000-A" or "P2S_000000-B".',
    )

    action_group = parser.add_mutually_exclusive_group()

    action_group.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List simulated devices present in MinKNOW.",
    )
    action_group.add_argument(
        "--add",
        "-a",
        nargs="*",
        default=None,
        help='Add specified simulated devices to MinKnow. BY default this device is a MinION, but this can be changed using the "--prom " or "--p2" flags. Optionally specify device names, which should be passed as a space separated list, for example `--add MS00000 MS00001`.\n Names must be in certain formats for each type created - MSXXXXX for MinION and LN for PromethION, where L is an uppercase letter and N is a single digit number eg: "1A". For P2, please use either "P2S_" followed by five digits, and then "-A" or "-B" eg: "P2S_000000-A" or "P2S_000000-B".',
    )
    action_group.add_argument(
        "--remove",
        "-r",
        nargs="*",
        default=None,
        help="Remove one or more dynamically created simulated device. Example usage:\n `--remove MS00000`. \nWill not error if device doesn't exist.",
    )
    action_group.add_argument(
        "--remove-all",
        action="store_true",
        help="Remove all simulated devices on the specified MinKNOW instance. Incompatible with --remove.",
    )

    args = parser.parse_args()

    if (args.client_cert_chain is None) != (args.client_key is None):
        parser.error(
            "--client-cert-chain and --client-key must either both be provided, or neither"
        )

    return args


def gen_prom_name():
    letters = ("A", "B", "C", "D", "E", "F", "G", "H")
    numbers = (1, 2, 3, 4, 5, 6)
    for n in numbers:
        for letter in letters:
            yield n, letter


def create_devices(manager, device_names, pattern, device_type):
    """Create a simulated device"""

    def get_unique_name(name_pattern, device_type):
        """Find the first device name with the specified pattern that doesn't already exist"""
        simulated_positions_names = [
            pos.name for pos in manager.flow_cell_positions() if pos.is_simulated
        ]
        # Promethion
        if (
            device_type
            == minknow_api.manager_pb2.SimulatedDeviceType.SIMULATED_PROMETHION
        ):
            for n, letter in gen_prom_name():
                name = name_pattern.format(n, letter)
                if name not in simulated_positions_names:
                    yield name
        # P2
        if device_type == minknow_api.manager_pb2.SimulatedDeviceType.SIMULATED_P2:
            for letter in ("A", "B"):
                name = pattern.format(letter)
                if name not in simulated_positions_names:
                    yield name
        # Anything else (MinION)
        for i in range(1000):
            name = name_pattern.format(i)
            if name not in simulated_positions_names:
                yield name

    # No device names were provided
    device_names = [None] if not device_names else device_names
    gen_unique_names = get_unique_name(pattern, device_type)
    for device_name in device_names:
        if device_name is None:
            device_name = next(gen_unique_names)
        try:
            manager.add_simulated_device(
                name=device_name,
                type=device_type,
            )
            print(f"Added simulated device {device_name}.")
        except RpcError as e:
            print(f"Error adding simulated device {device_name}", file=sys.stderr)
            print(repr(e.details()), file=sys.stderr)


def main():
    """Based on program arguments, list, add, and remove simulated devices as required."""
    args = parse_arguments()

    if (args.prom or args.p2) and args.add is None:
        print(
            "You have specified a device type but not passed --add. Listing available devices..."
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
    except Exception as e:
        print(
            f"Unable to connect to MinKNOW at {args.host}{args.port or ''} - {repr(e)}",
            file=sys.stderr,
        )
        exit(1)

    if args.add is not None:
        if args.prom:
            pattern = "{}{}"
            device_type = (
                minknow_api.manager_pb2.SimulatedDeviceType.SIMULATED_PROMETHION
            )
        elif args.p2:
            pattern = "PS2_000000-{}"
            try:
                device_type = minknow_api.manager_pb2.SimulatedDeviceType.SIMULATED_P2
            except AttributeError:
                print(
                    repr(
                        NotImplementedError(
                            f"Unfortunately the addition of a simulated P2 is not supported on this version of the minknow_api: {minknow_api.__version__}"
                        )
                    )
                )
                sys.exit(1)
                # patterns  and  tests
        else:
            device_type = minknow_api.manager_pb2.SimulatedDeviceType.SIMULATED_MINION
            pattern = "MS{:05}"
        create_devices(
            manager=manager,
            device_names=args.add,
            pattern=pattern,
            device_type=device_type,
        )
        sys.exit(0)

    elif isinstance(args.remove, list):
        for device_name in args.remove:
            if device_name is not None:
                # remove the named device
                manager.remove_simulated_device(name=device_name)
                print(f"Removed device {device_name}.")
            else:
                print(
                    "Please provide a device name to remove.\n\n"
                    "For example:\n\tpython manage_simulated_devices.py --remove MS00000.\n\n"
                    "Simulated device names can be viewed using the --list command.",
                    file=sys.stderr,
                )
                sys.exit(1)
        sys.exit(0)

    elif args.remove_all:
        print("Removing all simulated devices.")
        for position in manager.flow_cell_positions():
            if position.is_simulated:
                manager.remove_simulated_device(name=position.name)
                time.sleep(0.05)
                print(f"Removed device {position.name}.")
        print("Finished removing devices.")
        sys.exit(0)

    positions = [pos for pos in manager.flow_cell_positions() if pos.is_simulated]
    print(f"Connected simulated positions on MinKNOW at {args.host}:")
    for position in positions:
        print(
            f"\t{position.name}: {position.device_type}{' (integrated)' if position.is_integrated else ''}"
        )
    sys.exit(0)


if __name__ == "__main__":
    main()
