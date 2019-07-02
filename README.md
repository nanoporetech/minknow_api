# Introduction
MinKNOW is Oxford Nanopore Technologies Device Control software embedded in MinIT, GridION, PromethION and provided for installation on user PCs to run MinION.
MinKNOW carries out several core tasks: data acquisition; real-time analysis and feedback; basecalling; data streaming; device control including selecting the run parameters; sample identification and tracking and ensuring that the platform chemistry is performing correctly to run the samples. 
With the deployment of Oxford Nanopore devices into production sequencing environements, the ability to interface with MinKNOW and pull useful metadata such as Run IDs, Flow Cell IDs, run statistics becomes more important.

This API is provided "as is" with limited support and under the Oxford Nanopore Product Terms and Conditions and the Developer Licence Agreement. It has been made available for users who require a greater degree of intergration into their internal systems.


# MinKNOW Protobuf Repository

Contents:
 * [minknow](minknow/rpc/) - MinKNOW gRPC API broken into service descriptions.
 * [protocol return info](protocol_return_info.proto) - Messages the GUI expects to receive from special protocol scripts.
 * [protocol ui](protocol_ui.proto) - Used to communicate UI between GUI and bream scripts.
 * [daemon](daemon.proto) - [deprecated] Interface details for the minknow instance manager.
 * [raw data sampler](raw_data_sampler.proto) - [deprecated] Raw data from MinKNOW for the trace viewer.
 * [google](google/) - External google protobuf tools.

Navigating the gRPC API
-----------------------

The MinKNOW gRPC API is split into separate services, intended to provide functionality for
different use cases. There are a few key areas of interest for clients:

The API useful for LIMS integration is described in [LIMS API](LIMS_README.md).


### [Data Acquisition](minknow/rpc/acquisition.proto)

The acquisition service has methods used to start and stop sequencing on the device

 * See ```start``` for documentation on starting an experiment.
 * See ```get_current_acquisition_run``` for querying current acquisition state.

### [Read Until](minknow/rpc/data.proto)

The data service contains the low level apis used to obtain live experiment data, see ```get_live_reads```
for documentation on the low level read until api.