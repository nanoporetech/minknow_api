![.](docs/ONT_logo.png "Oxford Nanopore Technologies")

MinKNOW LIMS Interface
======================

MinKNOW is Oxford Nanopore Technologies Device Control software embedded in MinIT, GridION, PromethION and provided for installation on user PCs to run MinION.
MinKNOW carries out several core tasks: data acquisition; real-time analysis and feedback; basecalling; data streaming; device control including selecting the run parameters; sample identification and tracking and ensuring that the platform chemistry is performing correctly to run the samples. 
With the deployment of Oxford Nanopore devices into production sequencing environments, the ability to interface with MinKNOW and pull useful metadata such as Run IDs, Flow Cell IDs, run statistics becomes more important.

Getting Started
===============

Dependencies
------------

MinKNOW uses [Google Protocol Buffers v3](https://developers.google.com/protocol-buffers/docs/proto3)
to handle serialisation in MinKNOW and its supporting applications.

MinKNOW currently uses Protobuf version 3.6.1 and gRPC 1.16.1

Protobuf can be obtained from github: https://github.com/google/protobuf/releases

Generating a python interface
-----------------------------

An example of how to generate minknow GRPC interfaces from the contents of this repository is:

```bash
mkdir -p grpc_api/
protoc --python_out=grpc_api/ minknow/rpc/*.proto
```

Navigating the code
-------------------

The API contained in this project enables a user to interact with the information stored in the minknow top bar:
![Image of minknow GUI top bar](docs/minknow_top_bar.jpg "MinKNOW top bar")

The MinKNOW gRPC API is split into separate services, intended to provide functionality for
different use cases. There are a few key areas of interest for clients:

### [Experiment Management](minknow/rpc/protocol.proto)

The protocol service contains methods to start and stop sequencing experiments.

 * See ```list_protocols``` in order to list available scripts.
 * See ```start_protocol``` for documentation on starting a sequencing experiment (and also specifying the protocol_group_id).
 * See ```set_sample_id``` for setting the sample id for the active flow cell position.

### [Acquisition](minknow/rpc/acquisition.proto)

The acquisition service provides methods to start and stop acquisition, and query yield from acquisition periods.

### [Device Query](minknow/rpc/device.proto)

The device service contains methods to interrogate the sequencing device and flow cell.

### [Instance](minknow/rpc/instance.proto)

The instance service provides information about the device - hostname, output directories etc.

### [Flow Cell Check results](bream/platform_qc_results.proto)

Bream stores the flow cell check results in the minknow [keystore](minknow/rpc/keystore.proto).

******************

### Licence and Copyright

© 2019 Oxford Nanopore Technologies Ltd.

This API is provided "as is" with limited support and under the Oxford Nanopore Product Terms and Conditions. It has been made available for users who require a greater degree of intergration into their internal systems.

Rev005