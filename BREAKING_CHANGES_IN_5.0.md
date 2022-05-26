# Incompatible API Changes in MinKNOW API 5.0

The 5.0 release of MinKNOW API, describing the API for MinKNOW Core 5.0, has several incompatible
changes from earlier 4.x versions, and code using the API will need to be updated to suit.

The breaking changes are documented below.  There also some changes to the API that do not
break compatibility with older versions, such as the addition of new RPC's; these are not 
documented here.


## Removed RPCs

No RPCs have been removed from the MinKNOW API since MinKNOW Core 4.0.


## Changed Message Types

Note that some messages have had their fields renumbered.  The wire format of these messages will
not be compatible with earlier 4.x versions.

Some messages have had fields renamed, but using the same number as in 4.x.  These messages will 
be wire compatible with 4.x, although the interpretation of these fields may have changed.  Code
which uses these renamed fields will not be compatible.

The following messages have had their fields changed:

### `analysis_configuration.proto`

* `ReportConfiguration.ReportConfiguration`: The `markdown_report_file_pattern` field has been 
  renumbered to 8.  Field number 2 is now `json_report_file_pattern`
  
### `instance.proto`

* `GetVersionInfoResponse`: The `protocols` field has been renamed to `bream`, and the 
  `configuration` field renamed to `protocol_configuration`, to more accurately reflect
  the contents of the packages these fields relate to.
 
### `keystore.proto`

* `StoreRequest`: When using the `lifetime` field to store a value in the manager, the only valid
  values are `UNTIL_INSTANCE_END` and `PERSIST_ACROSS_RESTARTS`.  Using any other value will cause
  the call to fail with `INVALID_ARGUMENT` 

### `manager.proto`

* `FlowCellPosition.RpcPorts`: The fields `insecure` and `insecure_grpc_web` have been removed, 
  as it is no longer possible to use the gRPC protocols without TLS.

### `statistics.proto`

* `AcquisitionOutputBucket` has been renamed to `AcquisitionOutputSnapshot`, as this message 
  really reflects a snapshot of data at a given time point.  The field `bucket` has been renamed
  to `seconds`, as it indicates the time point.  
* `StreamAcquisitionOutputResponse`: The submessage `FilteredBuckets` has been
  renamed to `FilteredSnapshots`.  The `buckets` field in both messages has been renamed
  to `snapshots`.
* `WriterOutputBucket` has been renamed to `WriterOutputSnapshot`, as this message 
  really reflects a snapshot of data at a given time point.  The field `bucket` has been renamed
  to `seconds`, as it indicates the time point. 
* `StreamWriterOutputResponse`: The `buckets` field has been renamed to `snapshots`.
