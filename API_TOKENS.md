Types of API Token
==================

MinKNOW generally expects connections to be authenticated, and the MinKNOW API sometimes expects the user to supply an API token
in order to authenticate.

Local Tokens
------------

When the MinKNOW API is used on the sequencer itself, API access is granted using a token stored on disk. This allows any local process
to talk to minknow without needing to provide an API key.


Developer API Tokens
--------------------

When using remote execution (not running the example on the sequencer itself), API users must supply an API token generated using the MinKNOW UI.

This token will authenticate access to the sequencer remotely, and is specific to each sequencer used.

A developer API token can be supplied to the API using an argument to the `Manager` class, and is then passed to all child connections:

```python
# Construct a manager using the host + port provided:
manager = Manager(host=args.host, port=args.port, developer_api_token=os.env["MY_DEVELOPER_API_TOKEN"])
```

### Generating an API token

A user can generate an API token when logged into the sequencer, from the Host Settings section. API tokens must be generated using the UI, from a user
logged in using nanopore credentials, this allows events to be audited back to their originating user.

Note that a token will only be returned once, when you first generate it. After that, you will not be able to get it via the UI, so make sure you
store it safely (you can always generate another token, however).
