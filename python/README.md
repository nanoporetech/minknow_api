# Python API client for MinKNOW

This package provides a Python client to access the [MinKNOW APIs][minknow_api]. You will need a
compatible version of MinKNOW already installed to make use of this project.

To check for compatibility, look at the version of *MinKNOW Core*. The first two components of the
MinKNOW Core version should match the first two components of the `minknow_api` version. For
example, `minknow_api` 5.4.0 is compatible with any 5.4.x version of MinKNOW Core (which is part of
the 22.12 release of MinKNOW).

See the [main README in the git repository][readme] for more information about the MinKNOW API.

[minknow_api]: https://github.com/nanoporetech/minknow_api
[readme]: https://github.com/nanoporetech/minknow_api/blob/master/README.md

## Using

The recommended way to get it is from PyPI using pip, but it can also be built from source (see
`BUILD.md` in the top level of the git repository).

```bash
# Install minknow_api
> pip install minknow_api

# Verify API is installed correctly:
> python -m minknow_api.examples.list_sequencing_positions --host localhost

# Possible output if running MinKNOW locally:
#   Available sequencing positions on localhost:9502:
#   MN12345: running
#     secure: 8000
```

The package contains plenty of documentation in its docstrings, although for an overview of the
MinKNOW APIs themselves you may prefer to read the [API description files][api_files] - see below
for further discussion of these files. There are also [examples][examples] in the
`minknow_api.examples` submodule that show how to perform some common tasks.

[api_files]: https://github.com/nanoporetech/minknow_api/tree/master/proto/minknow_api
[examples]: https://github.com/nanoporetech/minknow_api/tree/master/python/minknow_api/examples


## Licence and Copyright

© 2023 Oxford Nanopore Technologies PLC.

API Specifications for MinKNOW is distributed under the Terms and Conditions of the Nanopore
Community.


## Troubleshooting

### Bad metadata key

If you see the following error when connecting to the **local** machine:

```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAUTHENTICATED
        details = "Bad metadata key"
```

you can try setting the `MINKNOW_API_USE_LOCAL_TOKEN` environment variable to `1`. Note that you
will need to have MinKNOW's local guest mode enabled for this to work (it is enabled by default, but
the setting can be changed via Mooneye).

### Invalid local auth token

If you see the following error when connecting to a **remote** machine:

```
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAUTHENTICATED
        details = "Invalid local auth token"
```

you can try setting the `MINKNOW_API_USE_LOCAL_TOKEN` environment variable to `0`.

### MissingMinknowSSlCertError

If you get a `MissingMinknowSSlCertError` exception, try setting the `MINKNOW_TRUSTED_CA`
environment variable. This should be the path to the `<data_dir>/rpc-certs/minknow/ca.crt` file,
where `<data_dir>` maps to `C:\\data` on Windows and `/data` on Ubuntu and MacOS platforms.
You should use a copy of the file from the same version of MinKNOW as the one you are
attempting to connect to.
