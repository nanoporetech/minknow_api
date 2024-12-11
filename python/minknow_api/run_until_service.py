### THIS FILE IS AUTOGENERATED. DO NOT EDIT THIS FILE DIRECTLY ###
import minknow_api
from minknow_api.run_until_pb2_grpc import *
import minknow_api.run_until_pb2 as run_until_pb2
from minknow_api.run_until_pb2 import *
from minknow_api._support import MessageWrapper, ArgumentError
import time
import logging
import sys

__all__ = [
    "RunUntilService",
    "CriteriaValues",
    "WriteTargetCriteriaRequest",
    "WriteTargetCriteriaResponse",
    "StreamTargetCriteriaRequest",
    "StreamTargetCriteriaResponse",
    "EstimatedTimeRemainingUpdate",
    "ActionUpdate",
    "ScriptUpdate",
    "ErrorUpdate",
    "Update",
    "WriteUpdatesRequest",
    "WriteUpdatesResponse",
    "StreamUpdatesRequest",
    "StreamUpdatesResponse",
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


class RunUntilService(object):
    """Overview
    ========

    This service allows a user to set certain criteria (Target Run-Until Criteria), which indicate
    the conditions under which the experiment should be stopped or paused.  For example, the user
    can specify that the experiment should be stopped after a certain time has elapsed, or paused
    when the number of available pores drops below a certain level.  This functionality is referred
    to as "Run-Until", since it allows the user to specify that an experiment should "run until"
    some condition has been fulfilled.

    The Target Run-Until Criteria are the conditions that are used to determine whether an
    experiment should be stopped or paused.  There is a "standard" set of Run-Until Criteria, which
    can always be used.  Additional Run-Until Criteria may also be supported by custom Run-Until
    Scripts (see below).

    This service also provides updates about the Run-Until status.  These include updates about
    the experiment's progress towards the Run-Until Criteria, as well as updates about the estimated
    time remaining, and Run-Until actions (i.e. starting/stopping the experiment).

    Finally, this service provides an API for Run-Until Scripts.  A Run-Until Script is responsible
    for actually implementing the Run-Until functionality.  The Run-Until Script reads the Target
    Run-Until Criteria that are set by the user.  It then monitors the experiment's progress, and
    pauses or stops the experiment when the Run-Until Criteria have been fulfilled.  There is a
    "standard" ONT-provided run-until script, which supports the "standard" Run-Until Criteria.
    Custom Run-Until Scripts can be implemented which extend the "standard" Run-Until Script to
    provide support for additional criteria.

    Usage -- Users
    ==============

    Overview
    --------

    The user sets the initial target Run-Until Criteria when the protocol is started, supplying them
    in the parameters passed to `start_protocol()` or `begin_protocol()`.

    The user may update these criteria as the experiment progresses by calling
    `write_target_criteria()` with the new criteria.

    The user can also obtain updates from the Run-Until Script by calling
    `stream_updates()`.  The Run-Until Script may send "estimated time remaining"
    information, or messages relating to the Run-Until status.

    If a criterion is specified in `write_target_criteria()` that is not recognised by the
    Run-Until Script, then the Run-Until Script will ignore that criterion.  It will also
    report that it has encountered an unrecognised criterion through `stream_updates()`.


    Standard Run-Until Criteria
    ---------------------------

    The Standard Run-Until Criteria are described below.  These criteria are always available for
    use.

    `runtime` (uint64)
         Acquisition runtime, in seconds
         Criterion is met if the runtime is greater than or equal to the specified value.

    `available_pores` (float)
         Pores marked available, following a mux scan.
         Criterion is met if the percentage of available pores is less than the specified value.
         An update will be supplied after each mux scan that is performed.

    `estimated_bases` (uint64)
         Estimated bases generated during the experiment.
         Criterion is met if the number of estimated bases is greater than or equal to the specified
         value.

    `passed_basecalled_bases` (uint64)
         Basecalled bases which pass filtering (following basecalling)
         Criterion will never be met if basecalling is not enabled.
         Updates will not be supplied if basecalling is not enabled.
         Criterion is met if the number of basecalled bases which pass filtering is greater than or
         equal to the specified value.


    Additional Run-Until Criteria
    -----------------------------

    Custom Run-Until Scripts may support additional criteria (beyond the Standard Run-Until Criteria
    described above).  The list of these criteria, and their meaning, will be supplied in the
    documentation for the custom run-until script.


    Usage -- Run-Until Scripts
    ==========================

    Overview
    --------

    The Run-Until Script is started as a custom script.

    The script obtains the Run-Until Criteria from MinKNOW using `stream_target_criteria()`.  Any
    updates to the Run-Until Criteria are also transmitted through this call.  If any of the
    criteria specified are not support by the script, the script reports an error via
    `write_updates()`.

    Finally, the Run-Until Script can perform actions and send updates to the user using the
    `write_updates()` interface.  Actions include pausing, resuming and stopping the
    acquisition.  Updates include estimated time remaining.

    Update History
    ==============

    MinKNOW stores an "merged" history of updates that are received on the `write_updates()`
    interface.  The history is calculated as MinKNOW receives updates on the `write_updates()`
    stream as follows:

     - When the protocol starts, an empty message is added to the history
     - When an update is received on the `write_updates()` interface, the values of the
       `estimated_time_remaining_update` and `current_progress_update` fields are updated, by
       "merging" the corresponding fields of the last message in the history.  "Merging" here means
       copying keys/values which appear in the "previous" message, but which don't have
       corresponding keys in the newly received message.
     - Once the values in the update have been updated, the "merged" message is then added to the
       history:
         - If the previous message in the history has no fields set, besides the
           `estimated_time_remaining_update` and/or `current_progress_update` fields, then the
           previous message in the history is overwritten with the "merged" message
         - Otherwise, the "merged" message is appended to the history.

     After updating the history, the final entry in the history is sent to any open
     `stream_updates()` streams.  The `idx` in the `StreamUpdatesResponse` message is set equal to
     the index of the entry in the history.  This means that the `stream_updates()` stream will
     likely contain repeated `idx` values -- this will happen when the previous message in the
     history is overwritten by the "merged" message.  The `time` in the `StreamUpdatesResponse`
     message is set equal to the time at which the entry in the history was last updated."""
    def __init__(self, channel):
        self._stub = RunUntilServiceStub(channel)
        self._pb = run_until_pb2
    def write_target_criteria(self, _message=None, _timeout=None, **kwargs):
        """Write target run-until criteria

        Updates to these criteria are forwarded to `stream_target_criteria()`.  When an update is
        made, all existing criteria are replaced with those specified in the
        WriteTargetCriteriaRequest

        

        Args:
            _message (minknow_api.run_until_pb2.WriteTargetCriteriaRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
            acquisition_run_id (str): The acquisition to set the Run-Until Criteria for
            pause_criteria (minknow_api.run_until_pb2.CriteriaValues, optional): 
            stop_criteria (minknow_api.run_until_pb2.CriteriaValues, optional): 

        Returns:
            minknow_api.run_until_pb2.WriteTargetCriteriaResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.write_target_criteria,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.run_until.RunUntilService")

        unused_args = set(kwargs.keys())

        _message = WriteTargetCriteriaRequest()

        if "acquisition_run_id" in kwargs:
            unused_args.remove("acquisition_run_id")
            _message.acquisition_run_id = kwargs['acquisition_run_id']
        else:
            raise ArgumentError("write_target_criteria requires a 'acquisition_run_id' argument")

        if "pause_criteria" in kwargs:
            unused_args.remove("pause_criteria")
            _message.pause_criteria.CopyFrom(kwargs['pause_criteria'])

        if "stop_criteria" in kwargs:
            unused_args.remove("stop_criteria")
            _message.stop_criteria.CopyFrom(kwargs['stop_criteria'])

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to write_target_criteria: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.write_target_criteria,
                              _message, _timeout,
                              [],
                              "minknow_api.run_until.RunUntilService")
    def stream_target_criteria(self, _message=None, _timeout=None, **kwargs):
        """Obtain the current target run-until criteria, and listen for changes in the target
        run-until criteria

        When an update is received, it specifies the new target criteria, which should replace all
        existing criteria.

        

        Args:
            _message (minknow_api.run_until_pb2.StreamTargetCriteriaRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
                Note that this is the time until the call ends, not the time between returned
                messages.
            acquisition_run_id (str): The acquisition to obtain the Run-Until Criteria for

        Returns:
            iter of minknow_api.run_until_pb2.StreamTargetCriteriaResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.stream_target_criteria,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.run_until.RunUntilService")

        unused_args = set(kwargs.keys())

        _message = StreamTargetCriteriaRequest()

        if "acquisition_run_id" in kwargs:
            unused_args.remove("acquisition_run_id")
            _message.acquisition_run_id = kwargs['acquisition_run_id']
        else:
            raise ArgumentError("stream_target_criteria requires a 'acquisition_run_id' argument")

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to stream_target_criteria: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.stream_target_criteria,
                              _message, _timeout,
                              [],
                              "minknow_api.run_until.RunUntilService")
    def write_updates(self, _message=None, _timeout=None, **kwargs):
        """Send an update about the current Run-Until state

        The Run-Until Script can use this to provide information about the expected time remaining
        (as well as other information) to users of the Run-Until functionality

        Updates written here are forwarded on to `stream_updates()`

        

        Args:
            _message (minknow_api.run_until_pb2.WriteUpdatesRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
            acquisition_run_id (str): The acquisition this Run-Until update applies to
            update (minknow_api.run_until_pb2.Update, optional): 

        Returns:
            minknow_api.run_until_pb2.WriteUpdatesResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.write_updates,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.run_until.RunUntilService")

        unused_args = set(kwargs.keys())

        _message = WriteUpdatesRequest()

        if "acquisition_run_id" in kwargs:
            unused_args.remove("acquisition_run_id")
            _message.acquisition_run_id = kwargs['acquisition_run_id']
        else:
            raise ArgumentError("write_updates requires a 'acquisition_run_id' argument")

        if "update" in kwargs:
            unused_args.remove("update")
            _message.update.CopyFrom(kwargs['update'])

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to write_updates: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.write_updates,
                              _message, _timeout,
                              [],
                              "minknow_api.run_until.RunUntilService")
    def stream_updates(self, _message=None, _timeout=None, **kwargs):
        """Obtain updates about the current Run-Until state

        The user can use this to obtain information about the expected time remaining (as well as
        other information) from the Run-Until Script.

        Updates are sent following writes to `write_updates()`

        

        Args:
            _message (minknow_api.run_until_pb2.StreamUpdatesRequest, optional): The message to send.
                This can be passed instead of the keyword arguments.
            _timeout (float, optional): The call will be cancelled after this number of seconds
                if it has not been completed.
                Note that this is the time until the call ends, not the time between returned
                messages.
            acquisition_run_id (str): The acquisition to stream Run-Until updates for
            start_idx (int, optional): The index of the first update to send.

                If an index is set that is greater than the current greatest update index, no past updates
                will be sent, but any future updates will be sent.  This may mean that you receive updates
                with an `idx` smaller than `start_idx`.

                In order to receive only updates that are sent after the call to `stream_updates()`, and no
                historic updates, set `start_idx` to `int64_max`.

                Setting `start_idx` to a negative number will be treated as an offset from the end of the
                updates history. A `start_idx` of `-1` will cause the last update to be sent, and any future
                updates to be streamed.  The negative value is clamped such that a "large" negative number
                will be equivalent to setting a `start_idx` of `0`.

                By default, `start_idx` is `0`, which means that all updates from the first update onwards
                will be sent.

        Returns:
            iter of minknow_api.run_until_pb2.StreamUpdatesResponse

        Note that the returned messages are actually wrapped in a type that collapses
        submessages for fields marked with ``[rpc_unwrap]``.
        """
        if _message is not None:
            if isinstance(_message, MessageWrapper):
                _message = _message._message
            return run_with_retry(self._stub.stream_updates,
                                  _message, _timeout,
                                  [],
                                  "minknow_api.run_until.RunUntilService")

        unused_args = set(kwargs.keys())

        _message = StreamUpdatesRequest()

        if "acquisition_run_id" in kwargs:
            unused_args.remove("acquisition_run_id")
            _message.acquisition_run_id = kwargs['acquisition_run_id']
        else:
            raise ArgumentError("stream_updates requires a 'acquisition_run_id' argument")

        if "start_idx" in kwargs:
            unused_args.remove("start_idx")
            _message.start_idx = kwargs['start_idx']

        if len(unused_args) > 0:
            raise ArgumentError("Unexpected keyword arguments to stream_updates: '{}'".format(", ".join(unused_args)))

        return run_with_retry(self._stub.stream_updates,
                              _message, _timeout,
                              [],
                              "minknow_api.run_until.RunUntilService")
