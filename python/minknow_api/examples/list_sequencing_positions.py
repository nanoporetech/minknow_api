import argparse

# minknow_api.manager supplies "Manager" a wrapper around MinKNOW's Manager gRPC API with utilities for
# querying sequencing positions + offline basecalling tools.
from minknow_api.manager import Manager


def main():
    """Main entrypoint for list_sequencing_devices example"""
    parser = argparse.ArgumentParser(
        description="List sequencing positions connected to a host."
    )
    parser.add_argument(
        "--host", default="localhost", help="Specify which host to connect to."
    )
    parser.add_argument(
        "--port", default=None, help="Specify which porer to connect to."
    )

    args = parser.parse_args()

    # Construct a manager using the host + port provided.
    manager = Manager(host=args.host, port=args.port)

    # Find a list of currently available sequencing positions.
    positions = manager.flow_cell_positions()

    # Print out available positions.
    print("Available sequencing positions on %s:%s:" % (args.host, args.port))
    for pos in positions:
        print("%s: %s" % (pos.name, pos.state))

        if pos.running:
            print("  secure: %s" % pos.description.rpc_ports.secure)

            # User could call {pos.connect()} here to connect to the running MinKNOW instance.


if __name__ == "__main__":
    main()
