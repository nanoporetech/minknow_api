Examples
========

[list_sequencing_positions](list_sequencing_positions.py)
-----------------------------------------------------------

An example showing how to communicate with the minknow manager and query information about connected sequencing devices.

Example usage:

```
> python list_sequencing_positions.py

# Possible output if running minknow locally:
#   Available sequencing positions on localhost:9501:
#   MN00001: running
#     secure: 8000
#     insecure: 8001

```

[start_protocol](start_protocol.py)
-------------------------------------

An example command line tool to start a protocol.

Example usage:

```
> python list_sequencing_positions.py

> python ./python/examples/start_protocol.py \
>     --host localhost --position 1A \                        # Select which host + position will run a script
>     --sample-id "my_sample" --experiment-group "my_group" \ # Set sample id + experiment group
>     --experiment-duration 24 \                              # Set the run time of the experiment (hours)
>     --kit SQK-LSK109 \                                      # Specify which kit is being run
>     --basecalling \                                         # Enable basecalling
>     --fastq --bam                                           # Choose fastq + bam output options

# Possible output if running minknow locally:
#
# Starting protocol on 1 positions
# Starting protocol sequencing/sequencing_PRO002_DNA:FLO-PRO002:SQK-LSK109 on position 6C
# Started protocol 07ec1bc5-9e39-4bff-ad73-447e2dc480c1

```