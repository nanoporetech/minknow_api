# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/run_until.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from minknow_api import rpc_options_pb2 as minknow__api_dot_rpc__options__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bminknow_api/run_until.proto\x12\x15minknow_api.run_until\x1a\x1dminknow_api/rpc_options.proto\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x9e\x01\n\x0e\x43riteriaValues\x12\x45\n\x08\x63riteria\x18\x01 \x03(\x0b\x32\x33.minknow_api.run_until.CriteriaValues.CriteriaEntry\x1a\x45\n\rCriteriaEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x38\x01\"\x1c\n\x1aGetStandardCriteriaRequest\"V\n\x1bGetStandardCriteriaResponse\x12\x37\n\x08\x63riteria\x18\x01 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\"\xbb\x01\n\x1aWriteTargetCriteriaRequest\x12 \n\x12\x61\x63quisition_run_id\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\x12=\n\x0epause_criteria\x18\x02 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\x12<\n\rstop_criteria\x18\x03 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\"\x1d\n\x1bWriteTargetCriteriaResponse\"?\n\x1bStreamTargetCriteriaRequest\x12 \n\x12\x61\x63quisition_run_id\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\"\x9b\x01\n\x1cStreamTargetCriteriaResponse\x12=\n\x0epause_criteria\x18\x01 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\x12<\n\rstop_criteria\x18\x02 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\"~\n\x1aWriteCustomProgressRequest\x12 \n\x12\x61\x63quisition_run_id\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\x12>\n\x0f\x63riteria_values\x18\x02 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\"\x1d\n\x1bWriteCustomProgressResponse\"9\n\x15StreamProgressRequest\x12 \n\x12\x61\x63quisition_run_id\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\"X\n\x16StreamProgressResponse\x12>\n\x0f\x63riteria_values\x18\x01 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\"\x98\x06\n\x1c\x45stimatedTimeRemainingUpdate\x12[\n\x0fpause_estimates\x18\x01 \x01(\x0b\x32\x42.minknow_api.run_until.EstimatedTimeRemainingUpdate.EstimatedTimes\x12Z\n\x0estop_estimates\x18\x02 \x01(\x0b\x32\x42.minknow_api.run_until.EstimatedTimeRemainingUpdate.EstimatedTimes\x1a\x0e\n\x0cNotEstimated\x1ag\n\tEstimated\x12,\n\x08min_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08max_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\xc7\x01\n\rEstimatedTime\x12Y\n\rnot_estimated\x18\x01 \x01(\x0b\x32@.minknow_api.run_until.EstimatedTimeRemainingUpdate.NotEstimatedH\x00\x12R\n\testimated\x18\x02 \x01(\x0b\x32=.minknow_api.run_until.EstimatedTimeRemainingUpdate.EstimatedH\x00\x42\x07\n\x05value\x1a\xfb\x01\n\x0e\x45stimatedTimes\x12o\n\x0f\x65stimated_times\x18\x01 \x03(\x0b\x32V.minknow_api.run_until.EstimatedTimeRemainingUpdate.EstimatedTimes.EstimatedTimesEntry\x1ax\n\x13\x45stimatedTimesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12P\n\x05value\x18\x02 \x01(\x0b\x32\x41.minknow_api.run_until.EstimatedTimeRemainingUpdate.EstimatedTime:\x02\x38\x01\"\x9a\x01\n\x0c\x41\x63tionUpdate\x12:\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32*.minknow_api.run_until.ActionUpdate.Action\x12\x10\n\x08\x63riteria\x18\x02 \x01(\t\"<\n\x06\x41\x63tion\x12\x0c\n\x08NoAction\x10\x00\x12\n\n\x06Paused\x10\x01\x12\x0b\n\x07Resumed\x10\x02\x12\x0b\n\x07Stopped\x10\x03\"\xb9\x01\n\x0cScriptUpdate\x12<\n\x07started\x18\x01 \x01(\x0b\x32+.minknow_api.run_until.ScriptUpdate.Started\x12M\n\x10\x63riteria_updated\x18\x02 \x01(\x0b\x32\x33.minknow_api.run_until.ScriptUpdate.CriteriaUpdated\x1a\t\n\x07Started\x1a\x11\n\x0f\x43riteriaUpdated\"\xec\x01\n\x0b\x45rrorUpdate\x12N\n\x10invalid_criteria\x18\x01 \x01(\x0b\x32\x32.minknow_api.run_until.ErrorUpdate.InvalidCriteriaH\x00\x12\x44\n\x0bother_error\x18\x0f \x01(\x0b\x32-.minknow_api.run_until.ErrorUpdate.OtherErrorH\x00\x1a\x1f\n\x0fInvalidCriteria\x12\x0c\n\x04name\x18\x01 \x03(\t\x1a\x1d\n\nOtherError\x12\x0f\n\x07message\x18\x01 \x01(\tB\x07\n\x05\x65rror\"\x85\x03\n\x06Update\x12\\\n\x1f\x65stimated_time_remaining_update\x18\x01 \x01(\x0b\x32\x33.minknow_api.run_until.EstimatedTimeRemainingUpdate\x12:\n\raction_update\x18\x02 \x01(\x0b\x32#.minknow_api.run_until.ActionUpdate\x12:\n\rscript_update\x18\x03 \x01(\x0b\x32#.minknow_api.run_until.ScriptUpdate\x12\x46\n\x17\x63urrent_progress_update\x18\x05 \x01(\x0b\x32%.minknow_api.run_until.CriteriaValues\x12\x38\n\x0c\x65rror_update\x18\x0e \x01(\x0b\x32\".minknow_api.run_until.ErrorUpdate\x12#\n\x05other\x18\x0f \x03(\x0b\x32\x14.google.protobuf.Any\"f\n\x13WriteUpdatesRequest\x12 \n\x12\x61\x63quisition_run_id\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\x12-\n\x06update\x18\x02 \x01(\x0b\x32\x1d.minknow_api.run_until.Update\"\x16\n\x14WriteUpdatesResponse\"K\n\x14StreamUpdatesRequest\x12 \n\x12\x61\x63quisition_run_id\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\x12\x11\n\tstart_idx\x18\x02 \x01(\x03\"}\n\x15StreamUpdatesResponse\x12\x0b\n\x03idx\x18\x01 \x01(\x04\x12(\n\x04time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\x06update\x18\x03 \x01(\x0b\x32\x1d.minknow_api.run_until.Update2\xfb\x06\n\x0fRunUntilService\x12\x80\x01\n\x15get_standard_criteria\x12\x31.minknow_api.run_until.GetStandardCriteriaRequest\x1a\x32.minknow_api.run_until.GetStandardCriteriaResponse\"\x00\x12\x80\x01\n\x15write_target_criteria\x12\x31.minknow_api.run_until.WriteTargetCriteriaRequest\x1a\x32.minknow_api.run_until.WriteTargetCriteriaResponse\"\x00\x12\x85\x01\n\x16stream_target_criteria\x12\x32.minknow_api.run_until.StreamTargetCriteriaRequest\x1a\x33.minknow_api.run_until.StreamTargetCriteriaResponse\"\x00\x30\x01\x12\x84\x01\n\x15write_custom_progress\x12\x31.minknow_api.run_until.WriteCustomProgressRequest\x1a\x32.minknow_api.run_until.WriteCustomProgressResponse\"\x04\x98\xb5\x18\x01\x12v\n\x0fstream_progress\x12,.minknow_api.run_until.StreamProgressRequest\x1a-.minknow_api.run_until.StreamProgressResponse\"\x04\x98\xb5\x18\x01\x30\x01\x12j\n\rwrite_updates\x12*.minknow_api.run_until.WriteUpdatesRequest\x1a+.minknow_api.run_until.WriteUpdatesResponse\"\x00\x12o\n\x0estream_updates\x12+.minknow_api.run_until.StreamUpdatesRequest\x1a,.minknow_api.run_until.StreamUpdatesResponse\"\x00\x30\x01\x42&\n\x1c\x63om.nanoporetech.minknow_api\xa2\x02\x05MKAPIb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.run_until_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034com.nanoporetech.minknow_api\242\002\005MKAPI'
  _CRITERIAVALUES_CRITERIAENTRY._options = None
  _CRITERIAVALUES_CRITERIAENTRY._serialized_options = b'8\001'
  _WRITETARGETCRITERIAREQUEST.fields_by_name['acquisition_run_id']._options = None
  _WRITETARGETCRITERIAREQUEST.fields_by_name['acquisition_run_id']._serialized_options = b'\210\265\030\001'
  _STREAMTARGETCRITERIAREQUEST.fields_by_name['acquisition_run_id']._options = None
  _STREAMTARGETCRITERIAREQUEST.fields_by_name['acquisition_run_id']._serialized_options = b'\210\265\030\001'
  _WRITECUSTOMPROGRESSREQUEST.fields_by_name['acquisition_run_id']._options = None
  _WRITECUSTOMPROGRESSREQUEST.fields_by_name['acquisition_run_id']._serialized_options = b'\210\265\030\001'
  _STREAMPROGRESSREQUEST.fields_by_name['acquisition_run_id']._options = None
  _STREAMPROGRESSREQUEST.fields_by_name['acquisition_run_id']._serialized_options = b'\210\265\030\001'
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIMES_ESTIMATEDTIMESENTRY._options = None
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIMES_ESTIMATEDTIMESENTRY._serialized_options = b'8\001'
  _WRITEUPDATESREQUEST.fields_by_name['acquisition_run_id']._options = None
  _WRITEUPDATESREQUEST.fields_by_name['acquisition_run_id']._serialized_options = b'\210\265\030\001'
  _STREAMUPDATESREQUEST.fields_by_name['acquisition_run_id']._options = None
  _STREAMUPDATESREQUEST.fields_by_name['acquisition_run_id']._serialized_options = b'\210\265\030\001'
  _RUNUNTILSERVICE.methods_by_name['write_custom_progress']._options = None
  _RUNUNTILSERVICE.methods_by_name['write_custom_progress']._serialized_options = b'\230\265\030\001'
  _RUNUNTILSERVICE.methods_by_name['stream_progress']._options = None
  _RUNUNTILSERVICE.methods_by_name['stream_progress']._serialized_options = b'\230\265\030\001'
  _CRITERIAVALUES._serialized_start=146
  _CRITERIAVALUES._serialized_end=304
  _CRITERIAVALUES_CRITERIAENTRY._serialized_start=235
  _CRITERIAVALUES_CRITERIAENTRY._serialized_end=304
  _GETSTANDARDCRITERIAREQUEST._serialized_start=306
  _GETSTANDARDCRITERIAREQUEST._serialized_end=334
  _GETSTANDARDCRITERIARESPONSE._serialized_start=336
  _GETSTANDARDCRITERIARESPONSE._serialized_end=422
  _WRITETARGETCRITERIAREQUEST._serialized_start=425
  _WRITETARGETCRITERIAREQUEST._serialized_end=612
  _WRITETARGETCRITERIARESPONSE._serialized_start=614
  _WRITETARGETCRITERIARESPONSE._serialized_end=643
  _STREAMTARGETCRITERIAREQUEST._serialized_start=645
  _STREAMTARGETCRITERIAREQUEST._serialized_end=708
  _STREAMTARGETCRITERIARESPONSE._serialized_start=711
  _STREAMTARGETCRITERIARESPONSE._serialized_end=866
  _WRITECUSTOMPROGRESSREQUEST._serialized_start=868
  _WRITECUSTOMPROGRESSREQUEST._serialized_end=994
  _WRITECUSTOMPROGRESSRESPONSE._serialized_start=996
  _WRITECUSTOMPROGRESSRESPONSE._serialized_end=1025
  _STREAMPROGRESSREQUEST._serialized_start=1027
  _STREAMPROGRESSREQUEST._serialized_end=1084
  _STREAMPROGRESSRESPONSE._serialized_start=1086
  _STREAMPROGRESSRESPONSE._serialized_end=1174
  _ESTIMATEDTIMEREMAININGUPDATE._serialized_start=1177
  _ESTIMATEDTIMEREMAININGUPDATE._serialized_end=1969
  _ESTIMATEDTIMEREMAININGUPDATE_NOTESTIMATED._serialized_start=1394
  _ESTIMATEDTIMEREMAININGUPDATE_NOTESTIMATED._serialized_end=1408
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATED._serialized_start=1410
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATED._serialized_end=1513
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIME._serialized_start=1516
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIME._serialized_end=1715
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIMES._serialized_start=1718
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIMES._serialized_end=1969
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIMES_ESTIMATEDTIMESENTRY._serialized_start=1849
  _ESTIMATEDTIMEREMAININGUPDATE_ESTIMATEDTIMES_ESTIMATEDTIMESENTRY._serialized_end=1969
  _ACTIONUPDATE._serialized_start=1972
  _ACTIONUPDATE._serialized_end=2126
  _ACTIONUPDATE_ACTION._serialized_start=2066
  _ACTIONUPDATE_ACTION._serialized_end=2126
  _SCRIPTUPDATE._serialized_start=2129
  _SCRIPTUPDATE._serialized_end=2314
  _SCRIPTUPDATE_STARTED._serialized_start=2286
  _SCRIPTUPDATE_STARTED._serialized_end=2295
  _SCRIPTUPDATE_CRITERIAUPDATED._serialized_start=2297
  _SCRIPTUPDATE_CRITERIAUPDATED._serialized_end=2314
  _ERRORUPDATE._serialized_start=2317
  _ERRORUPDATE._serialized_end=2553
  _ERRORUPDATE_INVALIDCRITERIA._serialized_start=2482
  _ERRORUPDATE_INVALIDCRITERIA._serialized_end=2513
  _ERRORUPDATE_OTHERERROR._serialized_start=2515
  _ERRORUPDATE_OTHERERROR._serialized_end=2544
  _UPDATE._serialized_start=2556
  _UPDATE._serialized_end=2945
  _WRITEUPDATESREQUEST._serialized_start=2947
  _WRITEUPDATESREQUEST._serialized_end=3049
  _WRITEUPDATESRESPONSE._serialized_start=3051
  _WRITEUPDATESRESPONSE._serialized_end=3073
  _STREAMUPDATESREQUEST._serialized_start=3075
  _STREAMUPDATESREQUEST._serialized_end=3150
  _STREAMUPDATESRESPONSE._serialized_start=3152
  _STREAMUPDATESRESPONSE._serialized_end=3277
  _RUNUNTILSERVICE._serialized_start=3280
  _RUNUNTILSERVICE._serialized_end=4171
StreamTargetCriteriaRequest.__doc__ = """Attributes:
    acquisition_run_id:
        The acquisition to obtain the Run-Until Criteria for
"""
CriteriaValues.__doc__ = """A map of criterion name -> value  This message is deliberately
flexible, to allow custom Run-Until Scripts to expand the range and
types of available criteria."""
WriteTargetCriteriaRequest.__doc__ = """Attributes:
    acquisition_run_id:
        The acquisition to set the Run-Until Criteria for
"""
EstimatedTimeRemainingUpdate.Estimated.__doc__ = """ These times are estimates of the (UTC) time at which the condition
will be fulfilled  Some idea of the expected accuracy of this estimate
can be obtained by comparing `min_time` with `max_time`.  If the
estimated time is believed to be accurate (e.g. for a "runtime"
criterion), then `min_time` may be equal to `max_time`.  Otherwise, if
the estimate is believed to be inaccurate (e.g. for a "pore_scan"
criterion which is not close to being fulfilled), then `min_time` and
`max_time` may differ significantly.

Attributes:
    min_time:
        Estimated lower bound on the time at which the condition will
        occur (UTC)
    max_time:
        Estimated upper bound on the time at which the condition will
        occur (UTC)
"""
ErrorUpdate.InvalidCriteria.__doc__ = """Indicates that one or more of the supplied target criteria is not
recognised by the  Run-Until Script.  Unrecognised target criteria
will not be used to pause or stop the run."""
EstimatedTimeRemainingUpdate.__doc__ = """Indicates the estimated time remaining  An estimated time may be
provided for each Run-Until Criterion that is specified as an end-
point."""
ErrorUpdate.OtherError.__doc__ = """An error that is not covered by one of the other error types, above."""
EstimatedTimeRemainingUpdate.NotEstimated.__doc__ = """Indicates that a time is not estimated"""
WriteUpdatesRequest.__doc__ = """Attributes:
    acquisition_run_id:
        The acquisition this Run-Until update applies to
"""
StreamProgressResponse.__doc__ = """Attributes:
    criteria_values:
        The run until criteria status  The criteria will always
        contain the `runtime` field, which acts as a timestamp for the
        message.  A Run-Until progress update need not contain updates
        for all criteria.
"""
ScriptUpdate.Started.__doc__ = """Indicates that the run-until script has started and is running"""
ActionUpdate.__doc__ = """Indicates that an action has been performed  When a request is sent
using `write_updates()`, MinKNOW performs the specified action.

Attributes:
    criteria:
        The criteria associated with this action
"""
GetStandardCriteriaResponse.__doc__ = """Attributes:
    criteria:
        A list of valid criteria  An empty value is included for each
        criterion, to indicate the required type of that criterion.
"""
ScriptUpdate.CriteriaUpdated.__doc__ = """Indicates the the Run-Until Script has update its criteria in response
to receiving a `StreamTargetCriteriaResponse` message"""
StreamUpdatesResponse.__doc__ = """Attributes:
    idx:
        The index of this update  The index is incremented after each
        "interesting" update (i.e. an update that contains information
        besides an `estimated_time_remaining_update` or a
        `current_progress_update`). See `Update History`, above, for
        further information.
    time:
        The timestamp of this update (UTC)
    update:
        The update data itself
"""
Update.__doc__ = """Attributes:
    current_progress_update:
        Gives the current values of the criteria (Compare to
        stream_target_criteria call to see %)
    other:
        Space for custom updates from custom Run-Until scripts
"""
WriteCustomProgressRequest.__doc__ = """Attributes:
    acquisition_run_id:
        The acquisition this Run-Until progress update relates to
    criteria_values:
        The current Run-Until criteria state  A Run-Until progress
        update need not contain updates for all criteria.  It must not
        contain updates for "standard" criteria
"""
StreamUpdatesRequest.__doc__ = """Attributes:
    acquisition_run_id:
        The acquisition to stream Run-Until updates for
    start_idx:
        The index of the first update to send.  If an index is set
        that is greater than the current greatest update index, no
        past updates will be sent, but any future updates will be
        sent.  This may mean that you receive updates with an `idx`
        smaller than `start_idx`.  In order to receive only updates
        that are sent after the call to `stream_updates()`, and no
        historic updates, set `start_idx` to `int64_max`.  Setting
        `start_idx` to a negative number will be treated as an offset
        from the end of the updates history. A `start_idx` of `-1`
        will cause the last update to be sent, and any future updates
        to be streamed.  The negative value is clamped such that a
        "large" negative number will be equivalent to setting a
        `start_idx` of `0`.  By default, `start_idx` is `0`, which
        means that all updates from the first update onwards will be
        sent.
"""
EstimatedTimeRemainingUpdate.EstimatedTimes.__doc__ = """Map of Run-Until Criterion to `EstimatedTime` when the criterion will
be fulfilled  Only criteria for which an update is being provided are
contained in the map."""
StreamProgressRequest.__doc__ = """Attributes:
    acquisition_run_id:
        The acquisition to obtain the Run-Until progress updates for
"""
ErrorUpdate.__doc__ = """Indicates that a problem has been encountered by the Run-Until Script"""
# @@protoc_insertion_point(module_scope)
