![.](docs/images/ONT_logo.png "Oxford Nanopore Technologies")

******************

# API Specifications for MinKNOW

## Overview

MinKNOW is software from Oxford Nanopore Technologies plc to control its single-modecule (eg: DNA or
RNA) sequencing devices. It comes embedded in GridION, PromethION and MinION Mk1C devices, and can
also be installed on user PCs to run devices such as the MinION Mk1B/Mk1D and the P2 Solo. MinKNOW
drives the sequencing hardware, analyses the data and provides the user with the results (which can
be the raw data samples from the hardware, a DNA or RNA sequence, or the answer to a biological
question).

The files and code in this repository provide a way of automating interactions with MinKNOW,
including gathering information about running or finished experiments, starting and stopping those
experiments, and even exerting more fine-grained control. Anything that can be done via MinKNOW's
user interface (and more) can be done using the APIs in this project.

This project is targetted at LIMS developers or developers of other tools that have a need to
integrate with MinKNOW. Some familiarity with Python is expected (although the APIs can be used from
other languages), as the examples are written in Python. If you are not familiar with [gRPC][grpc],
it is worth reading through some of the [gRPC documentation][grpc-docs] to get a feel for it.

[grpc]: https://grpc.io/
[grpc-docs]: https://grpc.io/docs/


******************

## Getting Started

### Dependencies

The first thing you will need is an installation of MinKNOW to communicate with. This can be
obtained from the [Oxford Nanopore Community download pages][community-download] if you want a local
installation, although the installation on a GridION, PromethION, etc will also work.

[community-download]: https://community.nanoporetech.com/downloads

Note that you will need a compatible version of MinKNOW for the version of `minknow_api` you are
using - see the FAQs below.

### Python

For the Python module and examples, you will also need Python 3.7 or later. The Python module
depends on a few other packages, such as [grpcio](https://pypi.org/project/grpcio/) and [numpy](https://pypi.org/project/numpy/), but these should be handled as part of package installation.

See [python/README.md](python/README.md) for more information about the Python module.


### Other Languages

MinKNOW's API is based on [gRPC][grpc] and can be used from any language supported by gRPC. This
includes Go, Java, Ruby, JavaScript (although see the note below about JavaScript) and many more.
The [gRPC documentation][grpc-docs] describes how to generate client libraries from the [API
descriptions](proto/minknow_api/) in this repository, and how to use those libraries. The `.proto`
files themselves contain documentation about what the various RPCs do, and a more general overview
is given below.

The Manager interface is available on port `9502` - see the FAQs for more details.
From there, APIs are available to get the ports that other services operate on (including the services
for each flow cell position).


#### JavaScript

How to use gRPC from JavaScript depends on whether you're using it from Node (in which case it works
much like any other language - see above) or from a web browser environment. For web browsers
(including Electron), you need to use the [Web][grpc-web] variant, which may also involve
connecting to a different port.

Secure connections still start at `9502` for the Manager service. When using the Manager APIs to
get ports for other services, you should use fields with `grpc_web` in the name, like `secure_grpc_web`.

[grpc-web]: https://github.com/improbable-eng/grpc-web

## Authentication

See [AUTH.md](AUTH.md) for information on authenticating with the MinKNOW API.


## API Highlights

The files in [`proto/minknow_api`](proto/minknow_api/) describe MinKNOW's APIs. Each file
describes a single *service*, which covers a specific area of MinKNOW's functionality.

There are two global services, the [manager service](proto/minknow_api/manager.proto) and
[basecaller service](proto/minknow_api/basecaller.proto). There is only one instance of each of
these services: see below for how to connect to them. All other services are provided by each flow
cell position independently. For example, if you are using a GridION X5, which has 5 flow cell
positions, there will be 5 ports (or sets of ports - secure, gRPC Web, etc), each of which
will provide *all* the other services.

### manager.proto

[manager.proto](proto/minknow_api/manager.proto) is the entry point of MinKNOW's APIs. It is always
available on a specific port `9502`.

The most important method is `flow_cell_positions`, which provides information about how to connect
to the services for each flow cell position. From there you can access all the flow cell
position-specific services.

Other methods on the manager service provide general information about the MinKNOW installation and
its high-level state, as well as port information for the [basecaller
service](proto/minknow_api/basecaller.proto) service, which can be used to basecall data from
previous experiments.

### instance.proto

[instance.proto](proto/minknow_api/instance.proto) provides general information about the flow cell
position. Of particular interest is the `get_output_directories` method, which indicates where data
files will be written to. `set_output_directories` can be used to change this.

`stream_instance_activity` may also be useful, as it provides a continuously-updated summary of the
state of the position.

This can be accessed via the ports reported by `flow_cell_positions` on the manager service.

### protocol.proto

[protocol.proto](proto/minknow_api/protocol.proto) allows starting and stopping experiment
protocols, as well as providing information about the current and previous protocol runs. Note that
information about protocol runs from before the last restart is not available via this API.

See the [`start_protocol` example](python/minknow_api/examples/start_protocol.py) for an example of how to use
this service to start a protocol.

### acquisition.proto

The main work of a protocol is acquiring data, and this is managed in
[acquisition.proto](proto/minknow_api/acquisition.proto). While most of the methods in
acquisition.proto will not be useful to most external tools, `get_acquisition_info` is helpful for
access detailed information about what was done by a protocol run reported by protocol.proto.

### device.proto

[device.proto](proto/minknow_api/device.proto) provides more detailed information about the
hardware of the flow cell position and the inserted flow cell. `get_device_info` provides some
constant information about the position, while `get_flow_cell_info` provides information about the
flow cell (a streaming version that provides updates about changes to the flow cell, such as it
being removed, is also available). It is also possible to override the flow cell identifier and
product code via this service (although this is not generally recommended).

### statistics.proto

[statistics.proto](proto/minknow_api/statistics.proto) provides statistics about current and
previous protocol runs, including duty time and temperature information. This is useful for
generating reports or tables of data describing how well an experiment has performed.


******************

Help
====

### Licence and Copyright

© 2023 Oxford Nanopore Technologies PLC.

API Specifications for MinKNOW is distributed under the Terms and Conditions of the Nanopore
Community.

### FAQs

#### What MinKNOW versions will this work with?

MinKNOW's API changes over time, to support new features and occasionally for other reasons, such as
improving security. The important version is that of *MinKNOW Core* - this version looks like 3.6.5
or 4.0.1 - rather than the date-based version of the entire MinKNOW release (which looks more like
19.12.5).

Every *minor* release of MinKNOW Core (the 4.0 in 4.0.1) has a fixed API, which is described by the
corresponding minor releases of `minknow_api`. So you should use the latest 4.0.x release of
`minknow_api` to talk to MinKNOW Core 4.0.1.

Note that while `minknow_api` does not strictly use semantic versioning, we aim to keep
backwards-incompatible changes to a minimum, and to deprecate anything we are planning to remove for
at least one minor version before we actually remove it. We also aim to only make incompatible
changes that are likely to have an impact on third-party systems when we bump the major version.

#### What port should I connect to?

Since MinKNOW Core 5.6, there are two "entry" ports, providing [manager
service](proto/minknow_api/manager.proto):

* `9501` can only be used with a gRPC secure channel. If you want to use client
  certificate authentication, you need to use this port.
* `9502` is for gRPC-Web connections, but can also be used with a gRPC secure channel. However, it
  cannot be used with client certificate authentication.

Versions prior to 5.6 only provided the `9502` port.

Ports reported by manager RPCs follow a similar pattern: there are two fields. For example, the
`basecaller_api` RPC returns a response with two fields:

* `secure` is a port that can be connected to with a gRPC secure channel, and supports client
    certificates
* `secure_grpc_web` is a port that can be connected to with a gRPC-Web secure channel (but does not
    support client certificates)

#### How do I set up a gRPC secure channel?

MinKNOW provides TLS transport security for its APIs, but uses a self-signed certificate. This means
that the client library you use has to trust this certificate.

If you are using the `minknow_api` Python package, this is all handled for you. If you are using the
gRPC client libraries directly (for example, if you are connecting from a language other than
Python), you will need to tell the library about MinKNOW's TLS certificates.

Within the MinKNOW installation, you can find the CA certificate at `conf/rpc-certs/ca.crt`. This
can be passed to most gRPC client libraries as part of creating a secure/SSL channel.

Note that this certificate is only valid for the "localhost" name - connecting to `127.0.0.1`
directly will not work, nor will connecting across the network. You can work around this by
setting the `grpc.ssl_target_name_override` channel option to `localhost`.

### Glossary

#### Acquisition

An *acquisition period* or *acquisition run* is a period in which data was being actively read from
the flow cell. A typical protocol will have two acquisition periods - a short one with minimal
analysis to calibrate the flow cell followed by a much longer one to actually gather sequence data.

#### Device

When the APIs refer to a *device*, this is the same as a *flow cell position*. Newer APIs use the
more descriptive *flow cell position*, but there are plenty of older APIs that use *device* instead.

#### Experiment

In the user interface, an *experiment name* is another name for a *protocol group ID* (see
*Protocol*). Note that what a user considers an "experiment" may not map onto a consistent concept
in MinKNOW, and the APIs generally avoid this term in favour of a more precise term like "protocol
run" or "protocol group".

#### Flow Cell

The *flow cell* is a consumable that plugs into the sequencing unit and contains the chemistry
required to sequence the sample. Often, but not always, contains some core electronics.

The *flow cell position* is the location that a flow cell can be plugged in to. It is synonymous
with *device* in the APIs.

#### Protocol

A *protocol* is a description of how to perform an experiment. This takes the form of some
configuration and a Python script. A *protocol run* is a specific execution of that protocol.

A *protocol group* is a set of protocol runs given the same name (referred to as a "protocol group
ID" in the API, and an "experiment name" in the user interface).
