# Incompatible API Changes in MinKNOW API 4.0

The 4.0 release of MinKNOW API, describing the API for MinKNOW Core 4.0, has several incompatible
changes from earlier 3.x versions, and code using the API will need to be updated to suit.

The breaking changes are documented below, but there are also some additions. Notably, the addition
of alignment support in MinKNOW has led to the addition of RPCs and message fields related to
alignment.


## Global Changes

There are two changes that affect all RPCs:

1. The package name has changed from `ont.rpc` to `minknow_api`. This will affect the namespace of
   generated C++ code, but more importantly, it changes the name of the RPCs at the network level.
   This means that code built against 4.0 (and later) versions of the MinKNOW API definitions *will
   not* work with MinKNOW Core 3, and similarly code built against MinKNOW API definitions before
   4.0 (eg: 3.6) *will not* work with MinKNOW Core 4.0 and later.
2. The directory structure has changed from having the `.proto` file contained in a `minknow/rpc`
   directory to being in a `minknow_api` directory. This means that the generated Python code is in
   a `minknow_api` module, instead of a `minknow.rpc` module. This has allowed us to release the
   `minknow_api` module as its own package on PyPI for your convenience (as the `minknow` package is
   built into MinKNOW itself, and not suitable for external distribution).

Existing code may need to replace reference to `ont.rpc`, `ont::rpc` and `minknow.rpc` with
`minknow_api`.


## Removed RPCs

The following RPCs have been removed from the MinKNOW API:

### `basecaller.proto`

* `start`: this has been renamed to `start_basecalling`.

### `manager.proto`

* `list_devices`: use `flow_cell_positions` instead.

### `protocol.proto`

* `get_sample_id` and `set_sample_id`: use the `sample_id` field of `ProtocolRunUserInfo` instead
  (this can be passed to `start_protocol` and is included in the `ProtocolRunInfo` message).

### `statistics.proto`

* `get_bias_voltages`: use `stream_bias_voltages` instead.
* `get_duty_time`: use `stream_duty_time` instead.
* `get_read_length_histogram`: use `stream_read_length_histogram` instead.
* `get_temperature`: use `stream_temperature` instead.
* `get_throughput`: use `stream_acquisition_output` instead.
* `stream_throughput`: use `stream_acquisition_output` instead.
* `stream_per_barcode_throughput`: use `stream_acquisition_output` with appropriate files and/or
  splits.
* `get_per_barcode_throughput`:  use `stream_acquisition_output` with appropriate files and/or
  splits.
* `get_encountered_barcode_names`: use `stream_encountered_acquisition_output_keys` instead.
* `stream_encountered_barcode_names`: use `stream_encountered_acquisition_output_keys` instead.
* `get_pore_speed_in_bases_boxplots`: use `stream_basecall_boxplots` instead.
* `stream_pore_speed_in_bases_boxplots`: use `stream_basecall_boxplots` instead.
* `get_qscore_boxplots`: use `stream_basecall_boxplots` instead.
* `stream_qscore_boxplots`: use `stream_basecall_boxplots` instead.


## Changed Message Types

Note that some messages have had their fields renumbered. We have not listed those here because the
package name change described above means the wire format of the RPCs is not compatible anyway.

The following messages have had their fields changed:

### `acquisition.proto`

* `AcquisitionYieldSummary`: the `basecalled_bases` field has been split into
  `basecalled_pass_bases` and `basecalled_fail_bases`. These can be summed to get the old field's
  value. The fields describing progress in writing out data have been moved to a separate
  `AcquisitionWriterSummary` message, which is available in the new `writer_summary` field of the
  `AcquisitionRunInfo` message.
* `StartRequest`: the `wait_until_processing` option has been removed. The new behaviour is the same
  as if it had been set (ie: the RPC will not return until acquisition has finished starting).

### `analysis_configuration.proto`

* Throughout the file, many fields have been changed from well-known wrapper types to basic types
  (eg: from `google.protobuf.UInt32Value` to `uint32`). Partial updates of the configuration for a
  particular piece of analysis (eg: event detection) are not supported, and this makes that clearer
  (as well as being simpler to use).
* `AnalysisConfiguration`: the `histograms` and `read_detection_alt` fields have been removed.
  `histograms` was already ignored. Running two parallel read detection setups is no longer
  supported.
* `ChannelStates`: the `name` field has been removed.
* `ChannelStates.Logic`: the `log` field has been removed.
* `EventDetection`: All previously deprecated fields (and there are many, all of which have been
  ignored for many releases) have been removed.
* `ReadClassificationParams`: the `selected_classifications` and `open_pore_classifications` fields
  are now `repeated string` instead of `google.protobuf.StringValue`. Multiple classifications
  should now be specified as separate values.
* `ReadClassificationParams.Parameters`: the `type` field has been removed.
* `WriterConfiguration`: the `read_old_single_fast5` field has been removed. This file type can no
  longer be written. Also, note that `data_set` cannot be used in any file patterns any more.
* `WriterConfiguration.BulkConfiguration`: the `basecall_summary`, `basecall_bases` and
  `basecall_events` fields have been removed. These data have not been written to the bulk file for
  many releases, even when these options were set.
* `WriterConfiguration.ReadFast5Configuration`: the `basecall_events` field has been removed. This
  data type is not produced any more, so cannot be written to files.

### `basecaller.proto`

* `RunInfo`: the `start_request` field has been renamed to `start_basecalling_request` to reflect
  that other requests are possible.
* `StartAlignmentRequest`: the `input_alignment_reference` and `minimum_coverage` fields have been
  replaced by an `alignment_configuration` field using a message from
  `analysis_configuration.proto`.
* `StartBarcodingRequest`: the `trim_barcodes` field has been replaced by a
  `barcoding_configuration` field using a message from `analysis_configuration.proto`.
* `StartRequest`: this message has been renamed to `StartBasecallingRequest`. The `barcoding_kits`
  and `trim_barcodes` options have been replaced by `barcoding_configuration` and
  `alignment_configuration` fields that uses messages from `analysis_configuration.proto`.
* `StartResponse`: this message has been renamed to `StartBasecallingResponse`.

### `data.proto`

* `GetChannelStatesResponse`, `GetSignalBytesResponse` and `GetReadStatisticsResponse` all use the
  `ReturnedChannelConfiguration` message from `device.proto` instead of `ChannelConfiguration`. This
  no longer includes the `regeneration` field (use the `unblock` field instead, which now provides
  the information you would actually expect).
* `GetExperimentYieldInfoResponse`: the `Hdf_writer_info` field has been renamed to
  `hdf_writer_info`. The `bases_called` field has been split into `bases_passed_called` and
  `bases_failed_called`. These can be summed to get the old field's value.
* `GetLiveReadsResponse`: the `action_reponses` field was renamed to
  `action_responses`. This is returned from the `get_live_reads` RPC.
* `GetSignalMinMaxRequest` has had its `seconds`, `samples` and `return_when_listening` fields
  removed. This call will always stream data until acquisition ends or it is explicitly cancelled.

### `device.proto`

* `ChannelConfiguration`: the `unblock` and `regeneration` fields have been removed, as
  `set_channel_configuration` and `set_channel_configuration_all` cannot be used to start an
  unblock. There is now a `ReturnedChannelConfiguration` message which does include `unblock` (but
  not `regeneration`) that is used by `get_channel_configuration` (as well as some RPCs in
  `data.proto`). The `unblock` field of this message should now report the unblocking state
  correctly on PromethIONs.
* `GetDeviceInfoResponse`: the `location_defined` and `location_index` fields have been removed.
  Better location information is available from the `flow_cell_positions` RPC in `manager.proto`.
* `GetDeviceInfoResponse.DeviceType`: the `PROMETHION` value now has the same value (and meaning) as
  `PROMETHION_BETA`. The `PROMETHION` name is preferred, and `PROMETHION_BETA` will be removed in
  the future.
* `GetFlowCellInfoResponse`: the `asic_id` field has been removed. Use `asic_id_str` instead.

### `instance.proto`

* `GetHostTypeResponse.HostType`: the `PROMETHION` value now has the same value (and meaning) as
  `PROMETHION_BETA`. The `PROMETHION` name is preferred, and `PROMETHION_BETA` will be removed in
  the future.

### `manager.proto`

* `ResetPositionRequest`: the `position` field has been removed; use the `positions` field instead.

### `statistics.proto`

* Most histogram data RPCs now use a `DataSelection` message to describe the selection and
  granularity of data to return, instead of `step`, `start_time` and `end_time` fields directly in
  the request message.
* All times are now in seconds, and the `TimeUnit` message has been removed.
* RPC request messages with a `run_id` field have had that field renamed to `acquisition_run_id`. It
  has the same semantics as before, but is now required.
* RPC request messages with a `wait_for_processing` options (or, equivalently, a `wait_for_starting`
  option) have had this removed. They now require an `acquisition_run_id` option, which is not
  available until the corresponding acquisition run has started, so the option to wait no longer has
  any effect.
* References to `CumulativeThroughput` in message names have been replaced with `AcquisitionOutput`.
* `StreamEncounteredCumulativeThroughputKeysRequest`: in addition to the above renaming, the
  `throughput_keys` field has been renamed to `acquisition_output_keys`.
* `CumulativeThroughputBucket`: in addition to the above renaming, the fields of this message have
  been replaced with an `AcquisitionYieldSummary` message from `acquisition.proto`.
* `StreamDutyTimeResponse`: the data are split into descriptions of buckets (`bucket_ranges`) and the
  per-channel-state data for each bucket (`channel_states`).
* Both `StreamReadLengthHistogramRequest` and `StreamReadLengthHistogramResponse`, used
  in the `stream_read_length_histogram` RPC, have changed considerably.
