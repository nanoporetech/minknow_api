# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from minknow_api import data_pb2 as minknow__api_dot_data__pb2


class DataServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_channel_states = channel.unary_stream(
                '/minknow_api.data.DataService/get_channel_states',
                request_serializer=minknow__api_dot_data__pb2.GetChannelStatesRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetChannelStatesResponse.FromString,
                )
        self.get_data_types = channel.unary_unary(
                '/minknow_api.data.DataService/get_data_types',
                request_serializer=minknow__api_dot_data__pb2.GetDataTypesRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetDataTypesResponse.FromString,
                )
        self.get_signal_bytes = channel.unary_stream(
                '/minknow_api.data.DataService/get_signal_bytes',
                request_serializer=minknow__api_dot_data__pb2.GetSignalBytesRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetSignalBytesResponse.FromString,
                )
        self.get_signal_min_max = channel.unary_stream(
                '/minknow_api.data.DataService/get_signal_min_max',
                request_serializer=minknow__api_dot_data__pb2.GetSignalMinMaxRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetSignalMinMaxResponse.FromString,
                )
        self.reset_channel_states = channel.unary_unary(
                '/minknow_api.data.DataService/reset_channel_states',
                request_serializer=minknow__api_dot_data__pb2.ResetChannelStatesRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.ResetChannelStatesResponse.FromString,
                )
        self.lock_channel_states = channel.unary_unary(
                '/minknow_api.data.DataService/lock_channel_states',
                request_serializer=minknow__api_dot_data__pb2.LockChannelStatesRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.LockChannelStatesResponse.FromString,
                )
        self.unlock_channel_states = channel.unary_unary(
                '/minknow_api.data.DataService/unlock_channel_states',
                request_serializer=minknow__api_dot_data__pb2.UnlockChannelStatesRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.UnlockChannelStatesResponse.FromString,
                )
        self.get_live_reads = channel.stream_stream(
                '/minknow_api.data.DataService/get_live_reads',
                request_serializer=minknow__api_dot_data__pb2.GetLiveReadsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetLiveReadsResponse.FromString,
                )
        self.record_adaptive_sampling_information = channel.unary_unary(
                '/minknow_api.data.DataService/record_adaptive_sampling_information',
                request_serializer=minknow__api_dot_data__pb2.RecordAdaptiveSamplingInformationRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.RecordAdaptiveSamplingInformationResponse.FromString,
                )
        self.get_read_statistics = channel.unary_unary(
                '/minknow_api.data.DataService/get_read_statistics',
                request_serializer=minknow__api_dot_data__pb2.GetReadStatisticsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetReadStatisticsResponse.FromString,
                )
        self.get_experiment_yield_info = channel.unary_unary(
                '/minknow_api.data.DataService/get_experiment_yield_info',
                request_serializer=minknow__api_dot_data__pb2.GetExperimentYieldInfoRequest.SerializeToString,
                response_deserializer=minknow__api_dot_data__pb2.GetExperimentYieldInfoResponse.FromString,
                )


class DataServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_channel_states(self, request, context):
        """Get the channel states for all channels from the device.

        This will return all the channel states from the moment of calling until the rpc is
        closed by the user. If the user stops acquisition, the rpc will return with the
        ABORTED status. If the user cancels the rpc, the status will be CANCELLED.

        The first messages returned will retrieve the current channel state for all channels
        On the MinION, the current state for all channels will be included in the first message.
        For PromethION, it will be split on multiple messages.

        To determine which channels have been returned, please check the channel member in the
        messages returned in the response.

        The response will be streamed, and we will provide a message as soon as there are channel
        state changes (though note that some channels could stay in the same state for a long time),
        so there is no guaranteed frequency of the messages returned. However, because a response
        message includes multiple channels, it is very likely that we have messages every few seconds.
        As in, it is likely that at least some of the channels will change every so often, therefore
        messages will be generated. For example, if 5 out of 512 channels change the state in the
        same time, there will be a message containing all 5 changes. Later on, if other channels
        change their state we will receive another message containing those and so on. Note that
        MinKNOW tries to group as many channel state changes in a single message, up to the message
        limit size, which is currently set to 32kB.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_data_types(self, request, context):
        """Get the data types of data items produced by this service.

        In order to allow clients to efficiently deal with large volumes of data in languages such as
        Python, this service can provide data as raw bytes. This call can be used to determine how to
        interpret those bytes. This can be used to construct an appropriate numpy dtype, for example.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_signal_bytes(self, request, context):
        """Get signal data from the device.

        This can be used to sample the signal being produced by the device. The signal can be
        returned as raw ADC values or as calibrated picoamp (pA) values; see ``set_calibration`` on
        the device service for the values used in this conversion.

        In addition to the signal, this can return the associated channel configuration and/or bias
        voltage information, to help analyse the data.

        If bias voltage information is requested, one bias voltage sample will be provided for each
        signal sample (on any given channel). So if you request 20 samples of signal data and also
        bias voltages, you will get 20 signal samples on each channel and also 20 bias voltage
        samples. Bias voltages are always given in millivolts, and no corrections need to be applied
        (for example, the 5x amplifier on a MinION is already accounted for).

        If channel configuration information is requested, each channel will have the starting
        channel configuration (with offset 0 to indicate it applies to the first sample on that
        channel), as well as any configuration changes that affect any of the returned samples.

        If a device settings change RPC has completed before this method is called, the data returned
        is guaranteed to have been generated by the device after those settings were applied.
        However, note that no guarantee is made about how device settings changes that overlap with
        this request will affect the returned data.

        The response will be streamed. In order to limit the size of each response message, any given
        message may include data from only a subset of the requested channels.

        Note that the data is returned as bytes fields. See the GetSignalBytesResponse documentation
        for more details about how to interpret the value. In Python code, the minknow.Device class
        provides a convenience wrapper method to convert the data into numpy arrays.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_signal_min_max(self, request, context):
        """Get summarised signal data from the device.

        This provides signal data from the device, like get_signal_bytes, but instead of all the
        data, it divides the data up into windows, and provides the minimum and maximum values for
        each window.

        This call is aimed at visualisations of data (ie: a traceviewer interface). As such, it does
        not provide most of the guarantees and options that get_signal_bytes() does. No bias voltage
        or channel configuration data is provided, it is not possible to set the number of samples
        desired up front (just cancel the call when no further data is required) and no guarantees
        are made about whether particular commands have been applied to the returned data.

        Also unlike get_signal_bytes(), the returned data is in native types, and does not require
        any further interpretation based on get_data_types(). This can be done performantly because
        of the reduced amount of data transmitted.

        The response will be streamed. In order to limit the size of each response message, any given
        message may include data from only a subset of the requested channels.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def reset_channel_states(self, request, context):
        """Call this to force re-evaluating the channel states. This will make sure the next
        channel state evaluated will be 'unclassified_following_reset'. If the analyser is behind,
        and older data will come for evaluation, it will result in changing the state to 'pending_manual_reset'.
        So typically, after a resetting the channel states, the user would see in the bulk file
        'unclassified_following_reset', 'pending_manual_reset', 'pending_manual_reset', until the relevant data
        comes through to the analyser and it will start outputting the normal channel states again.
        If the analyser is not behind, the user should ideally see just the 'unclassified_following_reset' state.

        This call is blocking - it will return from the rpc when it would have processed the
        'unclassified_following_reset' in the analyser. If the rpc takes more than 1 minute
        it will exit with the ABORTED status. This can happen if the analyser is more than 1 minute behind
        for example (in practice it shouldn't be the case). If the RPC exits with the ABORT status, it means
        the channels are to be reset in the future, but the analyser did not reach that point yet.

        Only one of these can be executed at a given time. If multiple threads call this simultaneously,
        it will execute the first request and it will exit with FAILED_PRECONDITION for the rest. If an RPC
        exited with the ABORT status, another RPC can immediately be started. The failed RPC would have not
        reset the channel states, and the user could try again. The second RPC will return as soon as the first
        reset happens, so this will not be necessarily waiting for the second acquisition index to be
        processed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def lock_channel_states(self, request, context):
        """Forces channels to be fixed on a custom channel state. The channels will not be re-evaluated until
        they are activated using unlock_channel_states.
        To create a channel state that will never be entered unless manually set using this call,
        use the "never_evaluated" criteria:
        "9": { "group": {...},
        "logic": {
        "rank": 0,
        "criteria": "never_evaluated"
        },
        "name": "custom_name_picked_by_the_user"
        }

        While the this RPC has the power of forcing a channel to any valid state other than 'unclassified',
        it is intended to be used with channel states that are designed for this functionality (i.e. that
        are never evaluated).
        Has to be called while acquiring data, fails otherwise.
        The forced channels are reset (reset = every channel back to being evaluated) every time a
        new acquisition sequence is started.

        NOTE:
        Calls to lock_channel_states and unlock_channel_states cannot be done in the same time.
        If any of these two is called while any of these is already running, the grpc will return
        with an error.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unlock_channel_states(self, request, context):
        """Re-activates channels that have been turned-off with force_channels_to_state.
        Note that 'turning off' refers to channel states only, everything else is still applied on the channel
        (e.g. mux changes, saturation, commands etc)
        No action is taken if the channel is already active.
        Has to be called while acquiring data, fails otherwise.
        NOTE:
        Calls to lock_channel_states and unlock_channel_states cannot be done in the same time.
        If any of these two is called while any of these is already running, the grpc will return
        with an error.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_live_reads(self, request_iterator, context):
        """Get live reads sent in order to control sequencing behaviour.

        This method sends current reads (reads that are currently in the sequencer) to the user along
        with live analysis data in order for real time decisions to be made.

        The method provides two streams:

        GetLiveReadsRequest stream:
        Sent by the user, provides MinKNOW with actions to take on current reads, actions
        taken are summarised and sent back to the user in the GetLiveReadsResponse stream.
        GetLiveReadsResponse stream:
        Sent to the user, contains a stream of ongoing sequencing information, sent as
        regularly as possible, with information on reads in progress, and feedback on actions
        taken on the data.

        note: This method operates on read chunks in MinKNOW, and will send at minimum, 1 read
        chunk to the user. In order to reduce latency on the method, tune the following options:

        The raw chunk size data is processed in minknow (specified in samples):
        app_conf/hyperstream.raw_data_intermediate.size
        app_conf/hyperstream.raw_meta_data_intermediate.size

        The maximum read chunk size - changing the size read chunks are processed in minknow:
        analysis_conf/read_detection.break_reads_after_seconds

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def record_adaptive_sampling_information(self, request, context):
        """Record information about adaptive-sampling for telemetry. This is optional
        and will not change how adaptive sampling works.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_read_statistics(self, request, context):
        """Collects statistics about read (chunk) lengths and signal, split by channel, channel
        configuration and read (chunk) classification.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_experiment_yield_info(self, request, context):
        """Returns various points of yield information for the ongoing experiment, such as complete
        read information and basecaller progress.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_channel_states': grpc.unary_stream_rpc_method_handler(
                    servicer.get_channel_states,
                    request_deserializer=minknow__api_dot_data__pb2.GetChannelStatesRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetChannelStatesResponse.SerializeToString,
            ),
            'get_data_types': grpc.unary_unary_rpc_method_handler(
                    servicer.get_data_types,
                    request_deserializer=minknow__api_dot_data__pb2.GetDataTypesRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetDataTypesResponse.SerializeToString,
            ),
            'get_signal_bytes': grpc.unary_stream_rpc_method_handler(
                    servicer.get_signal_bytes,
                    request_deserializer=minknow__api_dot_data__pb2.GetSignalBytesRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetSignalBytesResponse.SerializeToString,
            ),
            'get_signal_min_max': grpc.unary_stream_rpc_method_handler(
                    servicer.get_signal_min_max,
                    request_deserializer=minknow__api_dot_data__pb2.GetSignalMinMaxRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetSignalMinMaxResponse.SerializeToString,
            ),
            'reset_channel_states': grpc.unary_unary_rpc_method_handler(
                    servicer.reset_channel_states,
                    request_deserializer=minknow__api_dot_data__pb2.ResetChannelStatesRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.ResetChannelStatesResponse.SerializeToString,
            ),
            'lock_channel_states': grpc.unary_unary_rpc_method_handler(
                    servicer.lock_channel_states,
                    request_deserializer=minknow__api_dot_data__pb2.LockChannelStatesRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.LockChannelStatesResponse.SerializeToString,
            ),
            'unlock_channel_states': grpc.unary_unary_rpc_method_handler(
                    servicer.unlock_channel_states,
                    request_deserializer=minknow__api_dot_data__pb2.UnlockChannelStatesRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.UnlockChannelStatesResponse.SerializeToString,
            ),
            'get_live_reads': grpc.stream_stream_rpc_method_handler(
                    servicer.get_live_reads,
                    request_deserializer=minknow__api_dot_data__pb2.GetLiveReadsRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetLiveReadsResponse.SerializeToString,
            ),
            'record_adaptive_sampling_information': grpc.unary_unary_rpc_method_handler(
                    servicer.record_adaptive_sampling_information,
                    request_deserializer=minknow__api_dot_data__pb2.RecordAdaptiveSamplingInformationRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.RecordAdaptiveSamplingInformationResponse.SerializeToString,
            ),
            'get_read_statistics': grpc.unary_unary_rpc_method_handler(
                    servicer.get_read_statistics,
                    request_deserializer=minknow__api_dot_data__pb2.GetReadStatisticsRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetReadStatisticsResponse.SerializeToString,
            ),
            'get_experiment_yield_info': grpc.unary_unary_rpc_method_handler(
                    servicer.get_experiment_yield_info,
                    request_deserializer=minknow__api_dot_data__pb2.GetExperimentYieldInfoRequest.FromString,
                    response_serializer=minknow__api_dot_data__pb2.GetExperimentYieldInfoResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'minknow_api.data.DataService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_channel_states(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/minknow_api.data.DataService/get_channel_states',
            minknow__api_dot_data__pb2.GetChannelStatesRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetChannelStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_data_types(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/get_data_types',
            minknow__api_dot_data__pb2.GetDataTypesRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetDataTypesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_signal_bytes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/minknow_api.data.DataService/get_signal_bytes',
            minknow__api_dot_data__pb2.GetSignalBytesRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetSignalBytesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_signal_min_max(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/minknow_api.data.DataService/get_signal_min_max',
            minknow__api_dot_data__pb2.GetSignalMinMaxRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetSignalMinMaxResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def reset_channel_states(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/reset_channel_states',
            minknow__api_dot_data__pb2.ResetChannelStatesRequest.SerializeToString,
            minknow__api_dot_data__pb2.ResetChannelStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def lock_channel_states(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/lock_channel_states',
            minknow__api_dot_data__pb2.LockChannelStatesRequest.SerializeToString,
            minknow__api_dot_data__pb2.LockChannelStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def unlock_channel_states(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/unlock_channel_states',
            minknow__api_dot_data__pb2.UnlockChannelStatesRequest.SerializeToString,
            minknow__api_dot_data__pb2.UnlockChannelStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_live_reads(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/minknow_api.data.DataService/get_live_reads',
            minknow__api_dot_data__pb2.GetLiveReadsRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetLiveReadsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def record_adaptive_sampling_information(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/record_adaptive_sampling_information',
            minknow__api_dot_data__pb2.RecordAdaptiveSamplingInformationRequest.SerializeToString,
            minknow__api_dot_data__pb2.RecordAdaptiveSamplingInformationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_read_statistics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/get_read_statistics',
            minknow__api_dot_data__pb2.GetReadStatisticsRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetReadStatisticsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_experiment_yield_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.data.DataService/get_experiment_yield_info',
            minknow__api_dot_data__pb2.GetExperimentYieldInfoRequest.SerializeToString,
            minknow__api_dot_data__pb2.GetExperimentYieldInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
