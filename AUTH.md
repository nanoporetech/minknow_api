Authentication
==============

Unless you have enabled guest mode for MinKNOW, you will need to authenticate in order
to use the APIs. By default, guest mode is enabled for local connections but not remote
ones - however, MinKNOW can only tell a connection is local by its use of the "local
auth token" (see below)!

The recommended approach for authentication is to use client certificates.


Client certificates
-------------------

gRPC has built-in support for authentication via client TLS certificates, and MinKNOW
Core and `minknow_api` versions from 5.6 onwards enable this support.

The certificates must obey the following requirements:

- They must be X.509 certificates, encoded in PEM format.
- They must be valid for "digital signature" key usage (or not have the key usage
  extension).
- They must be valid for "client auth" extended key usage (or not have the extended key
  usage extension).
- There must be a chain of trust from a certificate in the `conf/rpc-client-certs`
  directory in the MinkNOW installation to the certificate used for client
  authentication.

The `minknow_api.examples.create_client_certificates` example script can be used to
generate certificates satisfying the first two requirements.

After placing either the certificate itself or another certificate that has signed it (a
Certificate Authority) into `conf/rpc-client-certs`, you should restart MinKNOW so that
it picks up the new certificate.

When using the `minknow_api` Python module, you can tell it what client certificate to
use by setting the following environment variables:

- `MINKNOW_API_CLIENT_CERTIFICATE_CHAIN` should be the path to the (PEM-encoded) client
  certificate *chain* to use. This means that if you are using a CA, the file needs to
  contain both the client certificate and the CA certificate.
- `MINKNOW_API_CLIENT_KEY` should be the path to the private key associated with the
  client certificate. This key should not be encrypted with a password.

`minknow_api.manager.Manager()` can accept the certificate and key as arguments instead
of using the environment variables.


Local token
-----------

When implementing "local guest access" (where local connections don't need to
authenticate but remote connections do), MinKNOW needs to be able to distinguish remote
connections and local connections. Due to the constraints of gRPC and gRPC-Web, MinKNOW
cannot directly tell whether a connection originated on the local machine or not.

Instead, local clients are expected to read a token from a file on disk and provide it
with connections they make to MinKNOW. This is only necessary if other authentication
methods are not used.

The `minknow_api` Python package handles this for you. If you are not using this
package, see the the `manager.local_authentication_token_path()` RPC documentation for
how to obtain this token.


Developer API Tokens
--------------------

Developer API tokens are DEPRECATED in favour of using client TLS certificates.

MinKNOW also supports creating "developer API tokens" to provide access to MinKNOW on a
particularly computer or sequencing device. This is less flexible than client
certificates, particularly when you are managing several sequencing devices - client
certificates let you easily use the same authentication details for all the MinKNOW
installations by just dropping a file into the installation of each one, whereas
developer API tokens are always specific to one MinKNOW installation.

A user can generate an API token when logged into the sequencer, from the Host Settings
section. API tokens must be generated using the UI, from a user logged in using nanopore
credentials. This allows events to be audited back to their originating user.

Note that a token will only be returned once, when you first generate it. After that,
you will not be able to get it via the UI, so make sure you store it safely (you can
always generate another token, however).

The token can then be supplied to the API using an argument to the `Manager` class. It
is passed to all child connections.

```python
manager = Manager(host="localhost", developer_api_token="the-token-copied-from-the-ui")
```
