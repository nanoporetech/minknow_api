### THIS FILE IS AUTOGENERATED. DO NOT EDIT THIS FILE DIRECTLY ###
import minknow_api
from minknow_api.hardware_check_pb2_grpc import *
import minknow_api.hardware_check_pb2 as hardware_check_pb2
from minknow_api.hardware_check_pb2 import *
from minknow_api._support import MessageWrapper, ArgumentError
import time
import logging
import sys

__all__ = [
    "HardwareCheckService",
    "StartHardwareCheckRequest",
    "StartHardwareCheckResponse",
    "StopHardwareCheckRequest",
    "StopHardwareCheckResponse",
    "PositionCheckResult",
    "HardwareCheckScriptData",
    "UpdateHardwareCheckResultsRequest",
    "UpdateHardwareCheckResultsResponse",
    "StreamHardwareCheckResultsRequest",
    "HardwareCheckResult",
    "StreamHardwareCheckResultsResponse",
    "GenerateHardwareCheckReportRequest",
    "GenerateHardwareCheckReportResponse",
    "HardwareCheckState",
    "HARDWARE_CHECK_RUNNING",
    "HARDWARE_CHECK_COMPLETED",
    "HARDWARE_CHECK_STOPPED",
    "HARDWARE_CHECK_FINISHED_WITH_ERROR_COULD_NOT_OBTAIN_EXIT_CODE",
    "HARDWARE_CHECK_FINISHED_WITH_ERROR_PYTHON_EXECUTOR_DID_NOT_START",
    "HARDWARE_CHECK_FINISHED_WITH_ERROR_SCRIPT_ERROR_CODE",
    "HARDWARE_CHECK_FINISHED_WITH_ERROR_LINGERING_RUN",
]

def run_with_retry(method, message, timeout, unwraps, full_name):
    retry_count = 20
    error = None
    for i in range(retry_count):
        try:
            result = MessageWrapper(method(message, timeout=timeout), unwraps=unwraps)
            return result
        except grpc.RpcError as e:
            # Retrying unidentified grpc errors to keep clients from crashing
            retryable_error = (e.code() == grpc.StatusCode.UNKNOWN and "Stream removed" in e.details() or \
                                (e.code() == grpc.StatusCode.INTERNAL and "RST_STREAM" in e.details()))
            if retryable_error:
                logging.info('Bypassed ({}: {}) error for grpc: {}. Attempt {}.'.format(e.code(), e.details(), full_name, i))
            else:
                raise
            error = e
        time.sleep(1)
    raise error


class HardwareCheckService(object):
    def __init__(self, channel):
        self._stub = HardwareCheckServiceStub(channel)
        self._pb = hardware_check_pb2
    def start_hardware_check(self, _message=None, _timeout=None, **kwargs):
        """Starts a hardware check against the device and any given positions.

        This RPC is idempotent. It may change the state of the system, but if the requested
        change has already happened, it will not fail because of this, make any additional
        changes or return a different value.

        Args:
            _message (minknow_api.hardware_check_pb2.StartHardwareCheckRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
            position_ids (str, optional): A list of position IDs to start a hardware check on
                e.g. `['X1', X2', 'X5']`.

        Returns:
            minknow_api.hardware_check_pb2.StartHardwareCheckResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.start_hardware_check,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.hardware_check.HardwareCheckService")

        unused_args = set(kwargs.keys())

        _message = StartHardwareCheckRequest()

        if "position_ids" in kwargs:
            unused_args.remove("position_ids")
            _message.position_ids.extend(kwargs['position_ids'])

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to start_hardware_check: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.start_hardware_check,
                              _message, _timeout,
                              [],
                              "minknow_api.hardware_check.HardwareCheckService")
    def stop_hardware_check(self, _message=None, _timeout=None, **kwargs):
        """Stops a hardware check against the device.

        This RPC is idempotent. It may change the state of the system, but if the requested
        change has already happened, it will not fail because of this, make any additional
        changes or return a different value.

        Args:
            _message (minknow_api.hardware_check_pb2.StopHardwareCheckRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
            hardware_check_id (str, optional): The unique ID for a hardware check.

        Returns:
            minknow_api.hardware_check_pb2.StopHardwareCheckResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.stop_hardware_check,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.hardware_check.HardwareCheckService")

        unused_args = set(kwargs.keys())

        _message = StopHardwareCheckRequest()

        if "hardware_check_id" in kwargs:
            unused_args.remove("hardware_check_id")
            _message.hardware_check_id = kwargs['hardware_check_id']

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to stop_hardware_check: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.stop_hardware_check,
                              _message, _timeout,
                              [],
                              "minknow_api.hardware_check.HardwareCheckService")
    def update_hardware_check_results(self, _message=None, _timeout=None, **kwargs):
        """Sets the latest hardware check result within Core, with the information from the hardware check script.

        This RPC is idempotent. It may change the state of the system, but if the requested
        change has already happened, it will not fail because of this, make any additional
        changes or return a different value.

        Args:
            _message (minknow_api.hardware_check_pb2.UpdateHardwareCheckResultsRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
            hardware_check_id (str, optional): The unique ID for a hardware check.
            hardware_check_script_data (minknow_api.hardware_check_pb2.HardwareCheckScriptData, optional): The data from the hardware check script

        Returns:
            minknow_api.hardware_check_pb2.UpdateHardwareCheckResultsResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.update_hardware_check_results,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.hardware_check.HardwareCheckService")

        unused_args = set(kwargs.keys())

        _message = UpdateHardwareCheckResultsRequest()

        if "hardware_check_id" in kwargs:
            unused_args.remove("hardware_check_id")
            _message.hardware_check_id = kwargs['hardware_check_id']

        if "hardware_check_script_data" in kwargs:
            unused_args.remove("hardware_check_script_data")
            _message.hardware_check_script_data.CopyFrom(kwargs['hardware_check_script_data'])

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to update_hardware_check_results: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.update_hardware_check_results,
                              _message, _timeout,
                              [],
                              "minknow_api.hardware_check.HardwareCheckService")
    def stream_hardware_check_results(self, _message=None, _timeout=None, **kwargs):
        """Lists all hardware checks

        Stream remains open whilst subscribed and any additionally started hardware checks are added to the list.

        This RPC has no side effects. Calling it will have no effect on the state of the
        system. It is safe to call repeatedly, or to retry on failure, although there is no
        guarantee it will return the same information each time.

        Args:
            _message (minknow_api.hardware_check_pb2.StreamHardwareCheckResultsRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
                Note that this is the time until the call ends, not the time between returned
                messages.
            hardware_check_id (str, optional): Filter the response by a specific hardware check ID.

                If this is empty, then:
                     - HardwareCheckResults for existing hardware checks will be streamed immediately
                         - Up to `count` newest hardware check results will be returned
                     - The stream will remain open
                     - Any subsequent hardware check updates will also be streamed, including those for
                       any hardware checks that are started after the `stream_hardware_check_results()`
                       call was made.

                Otherwise, if this is non-empty, then:
                     - The HardwareCheckResult for the corresponding hardware check will be returned
                     - If that hardware check is still in progress, then the stream will remain open and
                       any updates for that hardware check will be returned.
                     - The stream will be closed if/when the specified hardware check finishes
                         - This will be immediately after returning the first response if the hardware
                           check was already finished when the call was made
                     - If the specified `hardware_check_id` doesn't correspond to a valid hardware check,
                       an INVALID_ARGUMENT status will be returned.
            count (int, optional): The maximum number of records to return initially

                Since HardwareCheckResults are returned newest-to-oldest, this provides a way to get
                information only for the newest hardware checks

                (Note that subsequent updates will also be streamed, and so more than `count` responses may
                be returned on the stream)

                If `count` is `0` (the default) then all matching records will be returned

        Returns:
            iter of minknow_api.hardware_check_pb2.StreamHardwareCheckResultsResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.stream_hardware_check_results,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.hardware_check.HardwareCheckService")

        unused_args = set(kwargs.keys())

        _message = StreamHardwareCheckResultsRequest()

        if "hardware_check_id" in kwargs:
            unused_args.remove("hardware_check_id")
            _message.hardware_check_id = kwargs['hardware_check_id']

        if "count" in kwargs:
            unused_args.remove("count")
            _message.count = kwargs['count']

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to stream_hardware_check_results: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.stream_hardware_check_results,
                              _message, _timeout,
                              [],
                              "minknow_api.hardware_check.HardwareCheckService")
    def generate_hardware_check_report(self, _message=None, _timeout=None, **kwargs):
        """Generate a hardware check result report from a given hardware check ID.

        This RPC is idempotent. It may change the state of the system, but if the requested
        change has already happened, it will not fail because of this, make any additional
        changes or return a different value.

        Args:
            _message (minknow_api.hardware_check_pb2.GenerateHardwareCheckReportRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
                Note that this is the time until the call ends, not the time between returned
                messages.
            hardware_check_id (str, optional): The ID of the hardware check to generate a report for.

        Returns:
            iter of minknow_api.hardware_check_pb2.GenerateHardwareCheckReportResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.generate_hardware_check_report,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.hardware_check.HardwareCheckService")

        unused_args = set(kwargs.keys())

        _message = GenerateHardwareCheckReportRequest()

        if "hardware_check_id" in kwargs:
            unused_args.remove("hardware_check_id")
            _message.hardware_check_id = kwargs['hardware_check_id']

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to generate_hardware_check_report: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.generate_hardware_check_report,
                              _message, _timeout,
                              [],
                              "minknow_api.hardware_check.HardwareCheckService")
