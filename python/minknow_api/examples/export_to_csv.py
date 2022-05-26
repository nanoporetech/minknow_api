"""
Example script to export a number of fields for all experiments that match some search criteria to a CSV file.
"""

import argparse
import csv
import minknow_api
import sys
from minknow_api.manager import Manager


def main():
    # Define the command-line arguments.  The parser module will extract the user's values and place them in
    # variables named after the options.
    parser = argparse.ArgumentParser(
        description="""
        Export experiment information in CSV format.
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
        "--position",
        default=None,
        help="Restrict results to those ran on a position on the machine (or MinION serial number)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Send output to a file instead of stdout.",
    )
    args = parser.parse_args()

    # Try and connect to the minknow-core manager passing the host, port and developer-api token.  If the Python code
    # can't connect it will throw, catch the exception and exit with an error message.
    try:
        manager = Manager(
            host=args.host, port=args.port, developer_api_token=args.api_token
        )
    except:
        port = f":{args.port}" if args.port else ""
        print(f"Unable to connect to MinKNOW at {args.host}{port}", file=sys.stderr)
        exit(1)

    # Get the sequencing positions. Convert the iterable object returned into a list enabling iteratating over the
    # contents multiple times.
    reported_positions = list(manager.flow_cell_positions())
    if not reported_positions:
        printf("No sequencing positions reported", file=sys.stderr)
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

    experiments = []
    # loop through all the positions that matched the filter
    for pos in positions:
        # Connect to the position and get a list of all the protocols run on that position, these are provided as
        # Run-IDs.
        connection = pos.connect()
        list_runs_response = connection.protocol.list_protocol_runs()

        # loop through the Run-IDs fetching information about the experiment
        for run_id in list_runs_response.run_ids:
            # The majority of the information needed comes from the protocol-run-info.  The information returned also
            # provides a key for fetching further information about experiments from other services.
            try:
                proto_run_info = connection.protocol.get_run_info(run_id=run_id)
            except:
                print(
                    f"Warning : Couldn't find information about the experiment with run-id {run_id}",
                    file=sys.stderr,
                )
                continue

            # Only return info about protocols that have completed as identified by having an end-time
            if not proto_run_info.end_time.IsInitialized():
                print(
                    f"Warning : Ignoring experiment {run_id} it has not finished.",
                    file=sys.stderr,
                )
                continue

            experiment_information = {}

            experiment_information["Experiment ID"] = proto_run_info.protocol_id
            experiment_information[
                "Flow-Cell ID"
            ] = proto_run_info.flow_cell.flow_cell_id
            experiment_information["Sample ID"] = proto_run_info.user_info.sample_id

            end_time = proto_run_info.end_time.ToDatetime()
            start_time = proto_run_info.start_time.ToDatetime()
            experiment_information["Run Time"] = end_time - start_time

            # Information about reads and quantity of data is provided by the acquisition service.  The information is
            # indexed on the acquisition_run_id, there is a list of all these for the acquisition periods involved in
            # this experiment.  Get these, find the information we're interested in and sum the results across all the
            # acquisitions.
            bytes_written = 0
            number_of_reads = 0
            for acq_run_id in proto_run_info.acquisition_run_ids:
                try:
                    acq_run_info = connection.acquisition.get_acquisition_info(
                        run_id=acq_run_id
                    )
                except:
                    print(
                        f"Warning: Couldn't find acquisition info for run-id {acq_run_id}",
                        file=sys.stderr,
                    )
                    continue
                number_of_reads += acq_run_info.yield_summary.read_count
                bytes_written += acq_run_info.writer_summary.bytes_to_write_completed
            experiment_information["Data Quantity (Bytes)"] = bytes_written
            experiment_information["Reads"] = number_of_reads

            experiment_information["File Path"] = proto_run_info.output_path
            experiment_information["Run ID"] = run_id

            experiments.append(experiment_information)

    # If there were no runs found, then exit without creating a file.
    if len(experiments) == 0:
        exit(0)

    # Export collected information as CSV in either stdout or a file if a filename is specified.
    if args.output:
        csv_file = open(args.output, "w")
        if csv_file is None:
            print(f'Unable to open "{args.output}" for writing.', file=sys.stderr)
            sys.exit(1)
    else:
        csv_file = sys.stdout

    # Python makes CSV output easy with the csv library, tell it what the fields are, it will handle all the comma
    # stuff.  Get the fields from the first experiment, exiting earlier when if there was no data means should work.
    csv_writer = csv.DictWriter(csv_file, fieldnames=experiments[0].keys())
    csv_writer.writeheader()
    for experiment in experiments:
        csv_writer.writerow(experiment)


if __name__ == "__main__":
    main()
