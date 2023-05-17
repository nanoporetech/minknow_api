# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from minknow_api import acquisition_pb2 as minknow__api_dot_acquisition__pb2


class AcquisitionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.start = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/start',
                request_serializer=minknow__api_dot_acquisition__pb2.StartRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.StartResponse.FromString,
                )
        self.stop = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/stop',
                request_serializer=minknow__api_dot_acquisition__pb2.StopRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.StopResponse.FromString,
                )
        self.watch_for_status_change = channel.stream_stream(
                '/minknow_api.acquisition.AcquisitionService/watch_for_status_change',
                request_serializer=minknow__api_dot_acquisition__pb2.WatchForStatusChangeRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.WatchForStatusChangeResponse.FromString,
                )
        self.watch_current_acquisition_run = channel.unary_stream(
                '/minknow_api.acquisition.AcquisitionService/watch_current_acquisition_run',
                request_serializer=minknow__api_dot_acquisition__pb2.WatchCurrentAcquisitionRunRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.FromString,
                )
        self.current_status = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/current_status',
                request_serializer=minknow__api_dot_acquisition__pb2.CurrentStatusRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.CurrentStatusResponse.FromString,
                )
        self.get_progress = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/get_progress',
                request_serializer=minknow__api_dot_acquisition__pb2.GetProgressRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.GetProgressResponse.FromString,
                )
        self.get_acquisition_info = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/get_acquisition_info',
                request_serializer=minknow__api_dot_acquisition__pb2.GetAcquisitionRunInfoRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.FromString,
                )
        self.list_acquisition_runs = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/list_acquisition_runs',
                request_serializer=minknow__api_dot_acquisition__pb2.ListAcquisitionRunsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.ListAcquisitionRunsResponse.FromString,
                )
        self.get_current_acquisition_run = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/get_current_acquisition_run',
                request_serializer=minknow__api_dot_acquisition__pb2.GetCurrentAcquisitionRunRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.FromString,
                )
        self.set_signal_reader = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/set_signal_reader',
                request_serializer=minknow__api_dot_acquisition__pb2.SetSignalReaderRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.SetSignalReaderResponse.FromString,
                )
        self.set_bream_info = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/set_bream_info',
                request_serializer=minknow__api_dot_acquisition__pb2.SetBreamInfoRequest.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.SetBreamInfoResponse.FromString,
                )
        self.append_mux_scan_result = channel.unary_unary(
                '/minknow_api.acquisition.AcquisitionService/append_mux_scan_result',
                request_serializer=minknow__api_dot_acquisition__pb2.MuxScanResult.SerializeToString,
                response_deserializer=minknow__api_dot_acquisition__pb2.AppendMuxScanResultResponse.FromString,
                )


class AcquisitionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def start(self, request, context):
        """Starts reading data from the device

        Some setup calls will need to be made before starting data acquisition: particularly setting the analysis configuration,
        calibration, read writer and bulk writer config and some device calls such as setting the sampling frequency

        If acquisition is already running (even in the FINISHING state), this call will fail.

        On MinIONs and GridIONs, this will enable the ASIC power supply if it is not already enabled.
        See StopRequest.keep_power_on for more details about the implications of this.

        The rpc will return once `current_status` is "PROCESSING" or an error occurs and acquisition fails to start.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stop(self, request, context):
        """Stops data acquisition.

        Can specify a stop mode that handles what is done with the data when data acquisition is stopped. Refer to the enum
        description for documentation on what each mode does.

        Be aware that this command will return as soon as Minknow enters the FINISHING state and not the READY state.
        So if starting a new experiment then you will have to wait for the READY state separately
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def watch_for_status_change(self, request_iterator, context):
        """Watches for status changes within MinKNOW. Status states are defined from MinknowStatus enum.
        This is a bi-directional stream where the incoming response stream will return every time the status has changed
        and the request stream is used to stop the watcher. Refer to http://www.grpc.io/docs/tutorials/basic/python.html
        to see how bi-directional streaming works in grpc, but essentially when calling this function the user will have
        to pass in a generator that will eventually yield a WatchForStatusChangeRequest(stop=True) to the cpp side.
        A wrapper class for this is provided in the Python code.

        The function will first return with the current status that MinKNOW is in. Every response thereafter will be a
        change from one status to another.

        The ERROR_STATUS state includes errors during transition between states. If that happens, MinKNOW will
        try to revert to the READY state. It is up to the user to determine if they wish to try to wait for MinKNOW to
        correct itself or to try some other course of action
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def watch_current_acquisition_run(self, request, context):
        """Returns current acquisition run info and streams any changes to the current acquisition

        This call can be made even if acquisition is not running. In this case, the next streamed
        response will be the start of a new acquisition and you will receive updates for that acquisition
        until it finishes.

        If an acquisition finishes this stream will still continue to run and you will be notified when a new acquisition starts.

        Note if you begin this stream before any acquisition is started in minknow the state is `ACQUISITION_COMPLETED`.

        Since 1.13
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def current_status(self, request, context):
        """Check the current status of MinKNOW.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_progress(self, request, context):
        """Information on how much data has been acquired, processed and written.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_acquisition_info(self, request, context):
        """Gets information about an acquisition run, run within this instance on MinKNOW.

        If no run ID is provided, information about the most recently started acquisition run is
        provided.

        Since 1.11
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list_acquisition_runs(self, request, context):
        """Gets information about all previous acquisitions.

        Since 1.11
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_current_acquisition_run(self, request, context):
        """Returns the name and run id of the currently running acquisition.

        Will fail with FAILED_PRECONDITION if there is no acquisition running

        Since 1.11
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_signal_reader(self, request, context):
        """Specify the signal reader to use

        Since 3.6
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_bream_info(self, request, context):
        """Set the bream information for the current acquisition.

        This should only be called by the protocol. It will only affect the last acquisition that was
        started in the current protocol.

        If no protocol is running, or no acquisition has been started during the current protocol, a
        FAILED_PRECONDITION error will be returned.

        Since 5.0
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def append_mux_scan_result(self, request, context):
        """Add a mux scan result to the bream information for the current acquisition.

        This should only be called by the protocol. It will only affect the last acquisition that was
        started in the current protocol.

        If no protocol is running, or no acquisition has been started during the current protocol, a
        FAILED_PRECONDITION error will be returned.

        Since 5.0
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AcquisitionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'start': grpc.unary_unary_rpc_method_handler(
                    servicer.start,
                    request_deserializer=minknow__api_dot_acquisition__pb2.StartRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.StartResponse.SerializeToString,
            ),
            'stop': grpc.unary_unary_rpc_method_handler(
                    servicer.stop,
                    request_deserializer=minknow__api_dot_acquisition__pb2.StopRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.StopResponse.SerializeToString,
            ),
            'watch_for_status_change': grpc.stream_stream_rpc_method_handler(
                    servicer.watch_for_status_change,
                    request_deserializer=minknow__api_dot_acquisition__pb2.WatchForStatusChangeRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.WatchForStatusChangeResponse.SerializeToString,
            ),
            'watch_current_acquisition_run': grpc.unary_stream_rpc_method_handler(
                    servicer.watch_current_acquisition_run,
                    request_deserializer=minknow__api_dot_acquisition__pb2.WatchCurrentAcquisitionRunRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.SerializeToString,
            ),
            'current_status': grpc.unary_unary_rpc_method_handler(
                    servicer.current_status,
                    request_deserializer=minknow__api_dot_acquisition__pb2.CurrentStatusRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.CurrentStatusResponse.SerializeToString,
            ),
            'get_progress': grpc.unary_unary_rpc_method_handler(
                    servicer.get_progress,
                    request_deserializer=minknow__api_dot_acquisition__pb2.GetProgressRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.GetProgressResponse.SerializeToString,
            ),
            'get_acquisition_info': grpc.unary_unary_rpc_method_handler(
                    servicer.get_acquisition_info,
                    request_deserializer=minknow__api_dot_acquisition__pb2.GetAcquisitionRunInfoRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.SerializeToString,
            ),
            'list_acquisition_runs': grpc.unary_unary_rpc_method_handler(
                    servicer.list_acquisition_runs,
                    request_deserializer=minknow__api_dot_acquisition__pb2.ListAcquisitionRunsRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.ListAcquisitionRunsResponse.SerializeToString,
            ),
            'get_current_acquisition_run': grpc.unary_unary_rpc_method_handler(
                    servicer.get_current_acquisition_run,
                    request_deserializer=minknow__api_dot_acquisition__pb2.GetCurrentAcquisitionRunRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.SerializeToString,
            ),
            'set_signal_reader': grpc.unary_unary_rpc_method_handler(
                    servicer.set_signal_reader,
                    request_deserializer=minknow__api_dot_acquisition__pb2.SetSignalReaderRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.SetSignalReaderResponse.SerializeToString,
            ),
            'set_bream_info': grpc.unary_unary_rpc_method_handler(
                    servicer.set_bream_info,
                    request_deserializer=minknow__api_dot_acquisition__pb2.SetBreamInfoRequest.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.SetBreamInfoResponse.SerializeToString,
            ),
            'append_mux_scan_result': grpc.unary_unary_rpc_method_handler(
                    servicer.append_mux_scan_result,
                    request_deserializer=minknow__api_dot_acquisition__pb2.MuxScanResult.FromString,
                    response_serializer=minknow__api_dot_acquisition__pb2.AppendMuxScanResultResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'minknow_api.acquisition.AcquisitionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AcquisitionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def start(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/start',
            minknow__api_dot_acquisition__pb2.StartRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.StartResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/stop',
            minknow__api_dot_acquisition__pb2.StopRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.StopResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def watch_for_status_change(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/minknow_api.acquisition.AcquisitionService/watch_for_status_change',
            minknow__api_dot_acquisition__pb2.WatchForStatusChangeRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.WatchForStatusChangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def watch_current_acquisition_run(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/minknow_api.acquisition.AcquisitionService/watch_current_acquisition_run',
            minknow__api_dot_acquisition__pb2.WatchCurrentAcquisitionRunRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def current_status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/current_status',
            minknow__api_dot_acquisition__pb2.CurrentStatusRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.CurrentStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_progress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/get_progress',
            minknow__api_dot_acquisition__pb2.GetProgressRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.GetProgressResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_acquisition_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/get_acquisition_info',
            minknow__api_dot_acquisition__pb2.GetAcquisitionRunInfoRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list_acquisition_runs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/list_acquisition_runs',
            minknow__api_dot_acquisition__pb2.ListAcquisitionRunsRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.ListAcquisitionRunsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_current_acquisition_run(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/get_current_acquisition_run',
            minknow__api_dot_acquisition__pb2.GetCurrentAcquisitionRunRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.AcquisitionRunInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_signal_reader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/set_signal_reader',
            minknow__api_dot_acquisition__pb2.SetSignalReaderRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.SetSignalReaderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_bream_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/set_bream_info',
            minknow__api_dot_acquisition__pb2.SetBreamInfoRequest.SerializeToString,
            minknow__api_dot_acquisition__pb2.SetBreamInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def append_mux_scan_result(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.acquisition.AcquisitionService/append_mux_scan_result',
            minknow__api_dot_acquisition__pb2.MuxScanResult.SerializeToString,
            minknow__api_dot_acquisition__pb2.AppendMuxScanResultResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)