# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/report_data.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from minknow_api import acquisition_pb2 as minknow__api_dot_acquisition__pb2
from minknow_api import analysis_configuration_pb2 as minknow__api_dot_analysis__configuration__pb2
from minknow_api import log_pb2 as minknow__api_dot_log__pb2
from minknow_api import protocol_pb2 as minknow__api_dot_protocol__pb2
from minknow_api import run_until_pb2 as minknow__api_dot_run__until__pb2
from minknow_api import statistics_pb2 as minknow__api_dot_statistics__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dminknow_api/report_data.proto\x12\x17minknow_api.report_data\x1a\x1dminknow_api/acquisition.proto\x1a(minknow_api/analysis_configuration.proto\x1a\x15minknow_api/log.proto\x1a\x1aminknow_api/protocol.proto\x1a\x1bminknow_api/run_until.proto\x1a\x1cminknow_api/statistics.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x99\x01\n\x11\x41\x63quisitionOutput\x12=\n\x04type\x18\x01 \x01(\x0e\x32/.minknow_api.report_data.AcquisitionOutputTypes\x12\x45\n\x04plot\x18\x02 \x03(\x0b\x32\x37.minknow_api.statistics.StreamAcquisitionOutputResponse\"\xb1\x02\n\x13ReadLengthHistogram\x12@\n\x10read_length_type\x18\x01 \x01(\x0e\x32&.minknow_api.statistics.ReadLengthType\x12\x42\n\x11\x62ucket_value_type\x18\x02 \x01(\x0e\x32\'.minknow_api.statistics.BucketValueType\x12G\n\x04plot\x18\x03 \x01(\x0b\x32\x39.minknow_api.statistics.StreamReadLengthHistogramResponse\x12K\n\x08outliers\x18\x04 \x01(\x0b\x32\x39.minknow_api.statistics.StreamReadLengthHistogramResponse\"\x90\x01\n\x0f\x42\x61secallBoxplot\x12\x46\n\x04type\x18\x01 \x01(\x0e\x32\x38.minknow_api.statistics.StreamBoxplotRequest.BoxplotType\x12\x35\n\x04plot\x18\x02 \x01(\x0b\x32\'.minknow_api.statistics.BoxplotResponse\"\xa2\x07\n\x14\x41\x63quistionReportData\x12I\n\x14\x61\x63quisition_run_info\x18\x01 \x01(\x0b\x32+.minknow_api.acquisition.AcquisitionRunInfo\x12\x13\n\x0b\x62ucket_size\x18\x02 \x01(\x05\x12\x41\n\tduty_time\x18\x03 \x03(\x0b\x32..minknow_api.statistics.StreamDutyTimeResponse\x12I\n\rwriter_output\x18\x04 \x03(\x0b\x32\x32.minknow_api.statistics.StreamWriterOutputResponse\x12\x46\n\x0btemperature\x18\x05 \x03(\x0b\x32\x31.minknow_api.statistics.StreamTemperatureResponse\x12H\n\x0c\x62ias_voltage\x18\x06 \x03(\x0b\x32\x32.minknow_api.statistics.StreamBiasVoltagesResponse\x12\x46\n\x12\x61\x63quisition_output\x18\x07 \x03(\x0b\x32*.minknow_api.report_data.AcquisitionOutput\x12K\n\x15read_length_histogram\x18\x08 \x03(\x0b\x32,.minknow_api.report_data.ReadLengthHistogram\x12P\n\x11qscore_histograms\x18\x0b \x03(\x0b\x32\x35.minknow_api.statistics.StreamQScoreHistogramResponse\x12\x42\n\x10\x62\x61secall_boxplot\x18\t \x03(\x0b\x32(.minknow_api.report_data.BasecallBoxplot\x12\x37\n\x10run_until_update\x18\n \x01(\x0b\x32\x1d.minknow_api.run_until.Update\x12N\n\rwriter_config\x18\x0c \x01(\x0b\x32\x37.minknow_api.analysis_configuration.WriterConfiguration\x12V\n\x11\x62\x61secaller_config\x18\r \x01(\x0b\x32;.minknow_api.analysis_configuration.BasecallerConfiguration\",\n\x04Host\x12\x0e\n\x06serial\x18\x01 \x01(\t\x12\x14\n\x0cproduct_name\x18\x02 \x01(\t\"\xbc\x02\n\nReportData\x12+\n\x04host\x18\x02 \x01(\x0b\x32\x1d.minknow_api.report_data.Host\x12@\n\x11protocol_run_info\x18\x03 \x01(\x0b\x32%.minknow_api.protocol.ProtocolRunInfo\x12\x43\n\x0c\x61\x63quisitions\x18\x04 \x03(\x0b\x32-.minknow_api.report_data.AcquistionReportData\x12\x33\n\ruser_messages\x18\x05 \x03(\x0b\x32\x1c.minknow_api.log.UserMessage\x12?\n\x1breport_data_generation_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampJ\x04\x08\x01\x10\x02*\x9b\x01\n\x16\x41\x63quisitionOutputTypes\x12\x0b\n\x07\x41llData\x10\x00\x12\x1e\n\x1aSplitByBarcodeAndAlignment\x10\x01\x12\x12\n\x0eSplitByBarcode\x10\x02\x12\x14\n\x10SplitByAlignment\x10\x03\x12\x14\n\x10SplitByEndReason\x10\x04\x12\x14\n\x10SplitByBedRegion\x10\x05\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.report_data_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ACQUISITIONOUTPUTTYPES']._serialized_start=2184
  _globals['_ACQUISITIONOUTPUTTYPES']._serialized_end=2339
  _globals['_ACQUISITIONOUTPUT']._serialized_start=275
  _globals['_ACQUISITIONOUTPUT']._serialized_end=428
  _globals['_READLENGTHHISTOGRAM']._serialized_start=431
  _globals['_READLENGTHHISTOGRAM']._serialized_end=736
  _globals['_BASECALLBOXPLOT']._serialized_start=739
  _globals['_BASECALLBOXPLOT']._serialized_end=883
  _globals['_ACQUISTIONREPORTDATA']._serialized_start=886
  _globals['_ACQUISTIONREPORTDATA']._serialized_end=1816
  _globals['_HOST']._serialized_start=1818
  _globals['_HOST']._serialized_end=1862
  _globals['_REPORTDATA']._serialized_start=1865
  _globals['_REPORTDATA']._serialized_end=2181
Host.__doc__ = """This is a subset of the information available from the describe_host()
call"""
AcquistionReportData.__doc__ = """This is spelt incorrectly (should be AcquisitionReportData)

Attributes:
    acquisition_run_info:
        Information about the executed acquisition
    bucket_size:
        Size of buckets for all statistics data, in minutes.
    duty_time:
        Statistics snapshots for the acquisition period. Formatted
        into the same bucket size for all datatypes, computed from the
        length of the experiment.
    writer_config:
        Information about the writer configuration  Since 5.9
    basecaller_config:
        Information about the basecaller configuration  Since 5.9
"""
ReportData.__doc__ = """This field has been removed  Since 5.6

Attributes:
    protocol_run_info:
        Information about the executed protocol.
    acquisitions:
        Information about the acquisitions that are a part of the
        protocol.
    user_messages:
        All the user messages from protocol start to protocol end.
    report_data_generation_time:
        The time at which the report data was generated (UTC)
"""
# @@protoc_insertion_point(module_scope)
