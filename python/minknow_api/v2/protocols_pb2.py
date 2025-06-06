# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/v2/protocols.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from minknow_api import protocol_pb2 as minknow__api_dot_protocol__pb2
from minknow_api import manager_pb2 as minknow__api_dot_manager__pb2
from util import status_pb2 as util_dot_status__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eminknow_api/v2/protocols.proto\x12\x17minknow_api.v2.protocol\x1a\x1aminknow_api/protocol.proto\x1a\x19minknow_api/manager.proto\x1a\x11util/status.proto\"\xdf\x01\n\x15\x42\x65ginProtocolsRequest\x12R\n\x08requests\x18\x01 \x03(\x0b\x32@.minknow_api.v2.protocol.BeginProtocolsRequest.IndividualRequest\x1ar\n\x11IndividualRequest\x12\x1f\n\x17\x66low_cell_position_name\x18\x01 \x01(\t\x12<\n\x08settings\x18\x02 \x01(\x0b\x32*.minknow_api.protocol.BeginProtocolRequest\"\x99\x02\n\x16\x42\x65ginProtocolsResponse\x12U\n\tresponses\x18\x01 \x03(\x0b\x32\x42.minknow_api.v2.protocol.BeginProtocolsResponse.IndividualResponse\x1a\xa7\x01\n\x12IndividualResponse\x12\x1f\n\x17\x66low_cell_position_name\x18\x01 \x01(\t\x12?\n\x08response\x18\x02 \x01(\x0b\x32+.minknow_api.protocol.BeginProtocolResponseH\x00\x12$\n\x06status\x18\x03 \x01(\x0b\x32\x12.google.rpc.StatusH\x00\x42\t\n\x07payload\"\xdf\x01\n\x15StartProtocolsRequest\x12R\n\x08requests\x18\x01 \x03(\x0b\x32@.minknow_api.v2.protocol.StartProtocolsRequest.IndividualRequest\x1ar\n\x11IndividualRequest\x12\x1f\n\x17\x66low_cell_position_name\x18\x01 \x01(\t\x12<\n\x08settings\x18\x02 \x01(\x0b\x32*.minknow_api.protocol.StartProtocolRequest\"\x99\x02\n\x16StartProtocolsResponse\x12U\n\tresponses\x18\x01 \x03(\x0b\x32\x42.minknow_api.v2.protocol.StartProtocolsResponse.IndividualResponse\x1a\xa7\x01\n\x12IndividualResponse\x12\x1f\n\x17\x66low_cell_position_name\x18\x01 \x01(\t\x12?\n\x08response\x18\x02 \x01(\x0b\x32+.minknow_api.protocol.StartProtocolResponseH\x00\x12$\n\x06status\x18\x03 \x01(\x0b\x32\x12.google.rpc.StatusH\x00\x42\t\n\x07payload\"S\n\x14StopProtocolsRequest\x12;\n\x08requests\x18\x01 \x03(\x0b\x32).minknow_api.protocol.StopProtocolRequest\"\x85\x02\n\x15StopProtocolsResponse\x12T\n\tresponses\x18\x01 \x03(\x0b\x32\x41.minknow_api.v2.protocol.StopProtocolsResponse.IndividualResponse\x1a\x95\x01\n\x12IndividualResponse\x12\x0e\n\x06run_id\x18\x01 \x01(\t\x12>\n\x08response\x18\x02 \x01(\x0b\x32*.minknow_api.protocol.StopProtocolResponseH\x00\x12$\n\x06status\x18\x03 \x01(\x0b\x32\x12.google.rpc.StatusH\x00\x42\t\n\x07payload2\xd0\x04\n\x10ProtocolsService\x12t\n\x0f\x62\x65gin_protocols\x12..minknow_api.v2.protocol.BeginProtocolsRequest\x1a/.minknow_api.v2.protocol.BeginProtocolsResponse\"\x00\x12t\n\x0fstart_protocols\x12..minknow_api.v2.protocol.StartProtocolsRequest\x1a/.minknow_api.v2.protocol.StartProtocolsResponse\"\x00\x12q\n\x0estop_protocols\x12-.minknow_api.v2.protocol.StopProtocolsRequest\x1a..minknow_api.v2.protocol.StopProtocolsResponse\"\x00\x12\x63\n\x0cget_run_info\x12\'.minknow_api.protocol.GetRunInfoRequest\x1a%.minknow_api.protocol.ProtocolRunInfo\"\x03\x90\x02\x01\x12x\n\x12list_protocol_runs\x12-.minknow_api.protocol.ListProtocolRunsRequest\x1a..minknow_api.protocol.ListProtocolRunsResponse\"\x03\x90\x02\x01\x42\x61\n\x1f\x63om.nanoporetech.minknow_api.v2Z6github.com/nanoporetech/minknow_api/go/gen/v2/protocol\xa2\x02\x05MKAPIb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.v2.protocols_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\037com.nanoporetech.minknow_api.v2Z6github.com/nanoporetech/minknow_api/go/gen/v2/protocol\242\002\005MKAPI'
  _globals['_PROTOCOLSSERVICE'].methods_by_name['get_run_info']._options = None
  _globals['_PROTOCOLSSERVICE'].methods_by_name['get_run_info']._serialized_options = b'\220\002\001'
  _globals['_PROTOCOLSSERVICE'].methods_by_name['list_protocol_runs']._options = None
  _globals['_PROTOCOLSSERVICE'].methods_by_name['list_protocol_runs']._serialized_options = b'\220\002\001'
  _globals['_BEGINPROTOCOLSREQUEST']._serialized_start=134
  _globals['_BEGINPROTOCOLSREQUEST']._serialized_end=357
  _globals['_BEGINPROTOCOLSREQUEST_INDIVIDUALREQUEST']._serialized_start=243
  _globals['_BEGINPROTOCOLSREQUEST_INDIVIDUALREQUEST']._serialized_end=357
  _globals['_BEGINPROTOCOLSRESPONSE']._serialized_start=360
  _globals['_BEGINPROTOCOLSRESPONSE']._serialized_end=641
  _globals['_BEGINPROTOCOLSRESPONSE_INDIVIDUALRESPONSE']._serialized_start=474
  _globals['_BEGINPROTOCOLSRESPONSE_INDIVIDUALRESPONSE']._serialized_end=641
  _globals['_STARTPROTOCOLSREQUEST']._serialized_start=644
  _globals['_STARTPROTOCOLSREQUEST']._serialized_end=867
  _globals['_STARTPROTOCOLSREQUEST_INDIVIDUALREQUEST']._serialized_start=753
  _globals['_STARTPROTOCOLSREQUEST_INDIVIDUALREQUEST']._serialized_end=867
  _globals['_STARTPROTOCOLSRESPONSE']._serialized_start=870
  _globals['_STARTPROTOCOLSRESPONSE']._serialized_end=1151
  _globals['_STARTPROTOCOLSRESPONSE_INDIVIDUALRESPONSE']._serialized_start=984
  _globals['_STARTPROTOCOLSRESPONSE_INDIVIDUALRESPONSE']._serialized_end=1151
  _globals['_STOPPROTOCOLSREQUEST']._serialized_start=1153
  _globals['_STOPPROTOCOLSREQUEST']._serialized_end=1236
  _globals['_STOPPROTOCOLSRESPONSE']._serialized_start=1239
  _globals['_STOPPROTOCOLSRESPONSE']._serialized_end=1500
  _globals['_STOPPROTOCOLSRESPONSE_INDIVIDUALRESPONSE']._serialized_start=1351
  _globals['_STOPPROTOCOLSRESPONSE_INDIVIDUALRESPONSE']._serialized_end=1500
  _globals['_PROTOCOLSSERVICE']._serialized_start=1503
  _globals['_PROTOCOLSSERVICE']._serialized_end=2095
BeginProtocolsRequest.IndividualRequest.__doc__ = """Attributes:
    flow_cell_position_name:
        The position on which to start this protocol.
"""
BeginProtocolsResponse.IndividualResponse.__doc__ = """Represents the response from the proxied call to 'begin_protocol' on a
specific flow cell."""
StartProtocolsRequest.IndividualRequest.__doc__ = """Attributes:
    flow_cell_position_name:
        The position on which to start this protocol.
"""
# @@protoc_insertion_point(module_scope)
