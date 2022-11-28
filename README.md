# MinKNOW API Rust Client

*This is currently an early implementation and should not be used in production settings. This is NOT an official ONT project.*

A rust implementation of the minknow_api client for interacting with MinKNOW. More information on MinKNOW and minknow_api client, see [the minknow_api python client repository](https://github.com/nanoporetech/minknow_api).

## Contributing

Prequisites:

* Rust
* Cargo
* [MinKNOW](https://community.nanoporetech.com/docs/prepare/library_prep_protocols/Guppy-protocol/v/gpb_2003_v1_revan_14dec2018/guppy-for-macos) >=22.10.7 installed and running locally

End to end tests associated with the `minknow-api-rust` client currently interact directly with a running minknow instance to create simulated devices. The following setup must be performed prior to running tests:

1. Create a developer API token by opening the MinKNOW desktop application and navigating to 'Host Settings' -> 'API Access Tokens'.
1. An environment variable must reference this token, run `export MINKNOW_API_TEST_TOKEN={created_token}`
1. An environment variable must reference the self-signed certificate provided with the MinKNOW installation (for example, on MacOS run `export MIKNOW_TRUSTED_CA="/Applications/MinKNOW.app/Contents/Resources/conf/rpc-certs/ca.crt"`)

Once above prerequisites tests can be run with `cargo test --tests`.
