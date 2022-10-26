![.](docs/images/ONT_logo.png "Oxford Nanopore Technologies")

******************

# API Specifications for MinKNOW

### Overview

MinKNOW is Oxford Nanopore Technologies Device Control software embedded in MinION-mk1C, GridION,
PromethION and provided for installation on user PCs to run MinIONs. It carries out several core
tasks: data acquisition, real-time analysis and feedback, basecalling, data streaming, device
control (including selecting the run parameters), sample identification and tracking, and ensuring
that the platform chemistry is performing correctly to run the samples.

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

# Getting Started

### Dependencies

The first thing you will need is an installation of MinKNOW to communicate with. This can be
obtained from the [Oxford Nanopore Community download pages][community-download] if you want a local
installation, although the installation on a GridION, PromethION, Mk1C, etc will also work.

[community-download]: https://community.nanoporetech.com/downloads

Note that you will need a compatible version of MinKNOW for the version of `minknow_api` you are
using - see the FAQs below.

For the Python module and examples, you will also need Python 3.5 or later, with the following
Python packages installed:

* [grpcio](https://pypi.org/project/grpcio/)
* [numpy](https://pypi.org/project/numpy/)
* [packaging](https://pypi.org/project/packaging/)
* [protobuf](https://pypi.org/project/protobuf/)


### Python

The `minknow_api` Python package provides a client library for the MinKNOW APIs. The recommended way
to get it is from PyPI using pip, but it can also be built from source (see [BUILD.md](BUILD.md)).

```bash
# Install minknow_api
> pip install minknow_api

# Verify API is installed correctly (from a checkout of this repository):
> python ./python/minknow_api/examples/list_sequencing_positions.py --host localhost

# Possible output if running minknow locally:
#   Available sequencing positions on localhost:9502:
#   MN12345: running
#     secure: 8000
```

The package contains plenty of documentation in its docstrings, although for an overview of the
MinKNOW APIs themselves you may prefer to read the [API description files](proto/minknow_api/) -
see below for further discussion of these files. There are also [examples](python/minknow_api/examples/) (like
the `list_sequencing_positions.py` script in the above instructions) that show how to perform some
common tasks.

### Other Languages

MinKNOW's API is based on [gRPC][grpc] and can be used from any language supported by gRPC. This
includes Go, Java, Ruby, JavaScript (although see the note below about JavaScript) and many more.
The [gRPC documentation][grpc-docs] describes how to generate client libraries from the [API
descriptions](proto/minknow_api/) in this repository, and how to use those libraries. The `.proto`
files themselves contain documentation about what the various RPCs do, and a more general overview
is given below.

The Manager interface is available on port  `9502` - see the FAQs for more details.
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


### API Highlights

The files in [`proto/minknow_api`](proto/minknow_api/) describe MinKNOW's APIs. Each file
describes a single *service*, which covers a specific area of MinKNOW's functionality.

There are two global services, the [manager service](proto/minknow_api/manager.proto) and
[basecaller service](proto/minknow_api/basecaller.proto). There is only one instance of each of
these services: see below for how to connect to them. All other services are provided by each flow
cell position independently. For example, if you are using a GridION X5, which has 5 flow cell
positions, there will be 5 ports (or sets of ports - secure, gRPC Web, etc), each of which
will provide *all* the other services.

### Authentication

See [API Tokens](API_TOKENS.md) for information on authenticating with the MinKNOW API.

#### manager.proto

[manager.proto](proto/minknow_api/manager.proto) is the entry point of MinKNOW's APIs. It is always
available on a specific port `9502`.

The most important method is `flow_cell_positions`, which provides information about how to connect
to the services for each flow cell position. From there you can access all the flow cell
position-specific services.

Other methods on the manager service provide general information about the MinKNOW installation and
its high-level state, as well as port information for the [basecaller
service](proto/minknow_api/basecaller.proto) service, which can be used to basecall data from
previous experiments.

#### instance.proto

[instance.proto](proto/minknow_api/instance.proto) provides general information about the flow cell
position. Of particular interest is the `get_output_directories` method, which indicates where data
files will be written to. `set_output_directories` can be used to change this.

`stream_instance_activity` may also be useful, as it provides a continuously-updated summary of the
state of the position.

This can be accessed via the ports reported by `flow_cell_positions` on the manager service.

#### protocol.proto

[protocol.proto](proto/minknow_api/protocol.proto) allows starting and stopping experiment
protocols, as well as providing information about the current and previous protocol runs. Note that
information about protocol runs from before the last restart is not available via this API.

See the [`start_protocol` example](python/minknow_api/examples/start_protocol.py) for an example of how to use
this service to start a protocol.

#### acquisition.proto

The main work of a protocol is acquiring data, and this is managed in
[acquisition.proto](proto/minknow_api/acquisition.proto). While most of the methods in
acquisition.proto will not be useful to most external tools, `get_acquisition_info` is helpful for
access detailed information about what was done by a protocol run reported by protocol.proto.

#### device.proto

[device.proto](proto/minknow_api/device.proto) provides more detailed information about the
hardware of the flow cell position and the inserted flow cell. `get_device_info` provides some
constant information about the position, while `get_flow_cell_info` provides information about the
flow cell (a streaming version that provides updates about changes to the flow cell, such as it
being removed, is also available). It is also possible to override the flow cell identifier and
product code via this service (although this is not generally recommended).

#### statistics.proto

[statistics.proto](proto/minknow_api/statistics.proto) provides statistics about current and
previous protocol runs, including duty time and temperature information. This is useful for
generating reports or tables of data describing how well an experiment has performed.


******************

Help
====

### Licence and Copyright

© 2021 Oxford Nanopore Technologies PLC.

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

We aim to keep API backward-compatibility within a *major* release (the 4 in 4.0.1) of MinKNOW Core.
This means that if you write code that talks to MinKNOW Core 4.2, say, using `minknow_api` 4.2.1, it
should work with MinKNOW 4.3, 4.4, etc (without even updating `minknow_api`), but it *won't* work
with MinKNOW Core 3.6 or 5.0. There is also no guarantee it will work with MinKNOW Core 4.0 or 4.1
(depending on which specific APIs you have used).

#### What port should I connect to?

There is one standard port that MinKNOW exposes, which provides the [manager
service](proto/minknow_api/manager.proto):

* `9502` can be used with a gRPC or gRPC-Web "secure channel"

gRPC-Web is only used for browser-based clients; all other client should use the normal gRPC ports.

Ports reported by manager RPCs follow a similar pattern: there are two fields. For example, the
`basecaller_api` RPC returns a response with two fields:

* `secure` is a port that can be connected to with a gRPC secure channel
* `secure_grpc_web` is a port that can be connected to with a gRPC-Web secure channel

It may be that the `secure` and `secure_grpc_web` fields contain the same port number, but this is
not guaranteed and should not be relied on.

#### How do I connect to a "secure" port?

MinKNOW installations use a self-signed certificate for their secure ports. This means that the
client library you use has to trust this certificate.

If you are using the `minknow_api` Python package, this is all handled for you. If you are using
`minknow_api.manager.Manager`, secure connections are used by default. This can be overridden with
the `use_tls` argument when creating this class. `minknow_api.Connection` can also be passed a
`use_tls` argument.

If you are using the gRPC client libraries directly (for example, if you are connecting from a
language other than Python), you will need to tell the library about MinKNOW's TLS certificates.

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


### Troubleshooting

#### Bad metadata key

If you see the following error when connecting to the **local** machine:

```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAUTHENTICATED
        details = "Bad metadata key"
```

you can try setting the `MINKNOW_API_USE_LOCAL_TOKEN` environment variable to `1`. Note that you
will need to have MinKNOW's local guest mode enabled for this to work (it is enabled by default, but
the setting can be changed via Mooneye).

#### Invalid local auth token

If you see the following error when connecting to a **remote** machine:

```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAUTHENTICATED
        details = "Invalid local auth token"
```

you can try setting the `MINKNOW_API_USE_LOCAL_TOKEN` environment variable to `0`.

#### MissingMinknowSSlCertError

If you get a `MissingMinknowSSlCertError` exception, try setting the `MINKNOW_TRUSTED_CA`
environment variable. This should be the path to the `conf/rpc-certs/ca.crt` file found in a MinKNOW
installation. You should use a copy of the file from the same version of MinKNOW as the one you are
attempting to connect to.
