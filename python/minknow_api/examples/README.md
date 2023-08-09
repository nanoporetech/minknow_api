Examples
========

Authentication
--------------

When using remote execution (not running the example on the sequencer itself), some of the examples
in this directory require authentication. The recommended approach is to use client certificates.
See the `create_client_certificates.py` section below.

You can also use API tokens, which can be generated using the MinKNOW UI and passed to the example
scripts using the `--api-token` argument. However, this is deprecated in favour of using client
certificates.

See [AUTH.md][auth] for further info.

[auth]: https://github.com/nanoporetech/minknow_api/blob/master/AUTH.md


[create_client_certificates](create_client_certificates.py)
-----------------------------------------------------------

Client certificates are the recommended way of authenticating with MinKNOW's APIs. This
script will generate some suitable certificates, although your organisation may have an
existing mechanism for generating certificates that you wish to use.

Running this script requires the `cryptography` package to be installed, which is not a
dependency of `minknow_api` (as it is only used by this script).

```bash
pip install cryptography
python create_client_certificates.py my_client --no-key-pass
```

This will generate a self-signed certificate (valid for a year) that identifies its
subject as "my_client". You will get two files in the current directory:

- `my_client_cert.pem`, which should be copied into the `conf/rpc-client-certs/`
  directory in the MinKNOW installation
- `my_client_key.pem` which should be kept secret

You can pass the certificate and key to the other examples using the arguments
`--client-cert-chain=my_client_cert.pem` and `--client-key=my_client_key.pem`, or you
can set the environment variables

```
MINKNOW_API_CLIENT_CERTIFICATE_CHAIN="$PWD/my_client_cert.pem"
MINKNOW_API_CLIENT_KEY="$PWD/my_client_key.pem"
```


[list_sequencing_positions](list_sequencing_positions.py)
---------------------------------------------------------

An example showing how to communicate with the minknow manager and query information about connected sequencing devices.

Example usage:

```bash
python list_sequencing_positions.py

# Possible output (if running minknow locally):
#   Available sequencing positions on localhost:
#   MN00001: running
#     secure: 8000

```


[start_protocol](start_protocol.py)
-----------------------------------

An example command line tool to start a protocol.

Example usage:

```bash
python list_sequencing_positions.py

python ./python/minknow_api/examples/start_protocol.py \
    --host localhost --position 1A \                        # Select which host + position will run a script
    --sample-id "my_sample" --experiment-group "my_group" \ # Set sample id + experiment group
    --experiment-duration 24 \                              # Set the run time of the experiment (hours)
    --kit SQK-LSK109 \                                      # Specify which kit is being run
    --basecalling \                                         # Enable basecalling
    --fastq --bam                                           # Choose fastq + bam output options

# Possible output (if running minknow locally):
#   Starting protocol on 1 positions
#   Starting protocol sequencing/sequencing_PRO002_DNA:FLO-PRO002:SQK-LSK109 on position 6C
#   Started protocol 07ec1bc5-9e39-4bff-ad73-447e2dc480c1

```

[manage_simulated_devices](manage_simulated_devices.py)
-------------------------------------------------------
An example command line app to manage simulated devices in MinKNOW.

N.B addition of the P2 solo simulated position requires MinKNOW Core 5.4 or later.

Example usage:

```bash
# Add a simulated device
python manage_simulated_devices.py
# Possible output (if running minknow locally):
#   Connected simulated positions on MinKNOW at localhost:
#       MS00000: MINION
#       1A: PROMETHION
#       MS00003: MINION

# Add a simulated device by name
python manage_simulated_devices.py --add MS00002
# Possible output (if running minknow locally):
#   Added simulated device MS00002

# Add multiple devices by name
python manage_simulated_devices.py --add MS00002 MS00004 MS00009
# Possible output (if running minknow locally):
#   Added simulated device MS00002.
#   Added simulated device MS00004.
#   Added simulated device MS00009.

# List simulated devices
python manage_simulated_devices.py --list
# Possible output (if running minknow locally):
#   Connected simulated positions on MinKNOW at localhost:
#       MS00000: MINION
#       MS00001: PROMETHION
#       MS00002: MINION
#       MS00003: MINION

# Remove simulated devices
# Remove MS00002
python manage_simulated_devices.py --remove MS00002

# Remove Multiple devices
python manage_simulated_devices.py --remove MS00002 MS00004

# Remove all simulated devices (Not compatible with --remove)
python manage_simulated_devices.py --remove-all

# Add a simulated PromethION device
python manage_simulated_devices.py --prom --add

# Add multiple simulated PromethION devices
python manage_simulated_devices.py --prom --add 1A 2B

# Add a simulated P2 position
python manage_simulated_devices.py --p2 --add P2S_000000-A

# Add multiple simulated P2 positions
python manage_simulated_devices.py --p2 --add P2S_000000-A P2S_000000-B 

```
