Examples
========

Developer API Tokens
--------------------

When using remote execution (not running the example on the sequencer itself), some of the examples in this directory require
an API token, which can be generated using the MinKNOW UI. This token will authenticate access to the sequencer remotely,
and is specific to each sequencer used.

The examples in this directory accept an `--api-token` argument and pass this to the required API classes, when the example
requires a token.

See [developer api tokens](../../../API_TOKENS.md) for further info.


[list_sequencing_positions](list_sequencing_positions.py)
-----------------------------------------------------------

An example showing how to communicate with the minknow manager and query information about connected sequencing devices.

Example usage:

```
> python list_sequencing_positions.py

# Possible output if running minknow locally:
#   Available sequencing positions on localhost:9502:
#   MN00001: running
#     secure: 8000

```


[start_protocol](start_protocol.py)
-------------------------------------

An example command line tool to start a protocol.

Example usage:

```
> python list_sequencing_positions.py

> python ./python/minknow_api/examples/start_protocol.py \
>     --api-token ${MY_DEVELOPER_API_TOKEN} \
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