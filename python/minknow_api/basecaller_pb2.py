# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/basecaller.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from minknow_api import analysis_configuration_pb2 as minknow__api_dot_analysis__configuration__pb2
from minknow_api import protocol_settings_pb2 as minknow__api_dot_protocol__settings__pb2
from minknow_api import rpc_options_pb2 as minknow__api_dot_rpc__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cminknow_api/basecaller.proto\x12\x16minknow_api.basecaller\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a(minknow_api/analysis_configuration.proto\x1a#minknow_api/protocol_settings.proto\x1a\x1dminknow_api/rpc_options.proto\"\x19\n\x17ListConfigsByKitRequest\"\xf4\x03\n\x18ListConfigsByKitResponse\x12`\n\x11\x66low_cell_configs\x18\x01 \x03(\x0b\x32\x45.minknow_api.basecaller.ListConfigsByKitResponse.FlowCellConfigsEntry\x1a\x1d\n\nConfigList\x12\x0f\n\x07\x63onfigs\x18\x01 \x03(\t\x1a\xe0\x01\n\x0bPerFlowCell\x12\x61\n\x0bkit_configs\x18\x01 \x03(\x0b\x32L.minknow_api.basecaller.ListConfigsByKitResponse.PerFlowCell.KitConfigsEntry\x1an\n\x0fKitConfigsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12J\n\x05value\x18\x02 \x01(\x0b\x32;.minknow_api.basecaller.ListConfigsByKitResponse.ConfigList:\x02\x38\x01\x1at\n\x14\x46lowCellConfigsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12K\n\x05value\x18\x02 \x01(\x0b\x32<.minknow_api.basecaller.ListConfigsByKitResponse.PerFlowCell:\x02\x38\x01\"\xed\x03\n\x17StartBasecallingRequest\x12\x0c\n\x04name\x18\x0c \x01(\t\x12\x1f\n\x17input_reads_directories\x18\x01 \x03(\t\x12\x1e\n\x16output_reads_directory\x18\x02 \x01(\t\x12\x15\n\rconfiguration\x18\x03 \x01(\t\x12\x11\n\tfast5_out\x18\x04 \x01(\x08\x12\x16\n\x0e\x63ompress_fastq\x18\x05 \x01(\x08\x12\x16\n\x0e\x64isable_events\x18\x06 \x01(\x08\x12\x11\n\trecursive\x18\x07 \x01(\x08\x12[\n\x17\x62\x61rcoding_configuration\x18\n \x01(\x0b\x32:.minknow_api.analysis_configuration.BarcodingConfiguration\x12[\n\x17\x61lignment_configuration\x18\x0b \x01(\x0b\x32:.minknow_api.analysis_configuration.AlignmentConfiguration\x12\x1d\n\x15\x65nable_read_splitting\x18\r \x01(\x08\x12=\n\x18min_score_read_splitting\x18\x0e \x01(\x0b\x32\x1b.google.protobuf.FloatValue\"&\n\x18StartBasecallingResponse\x12\n\n\x02id\x18\x01 \x01(\t\"\xee\x01\n\x15StartBarcodingRequest\x12\x0c\n\x04name\x18\x0b \x01(\t\x12\x1f\n\x17input_reads_directories\x18\x01 \x03(\t\x12\x1e\n\x16output_reads_directory\x18\x02 \x01(\t\x12\x16\n\x0e\x63ompress_fastq\x18\x04 \x01(\x08\x12\x11\n\trecursive\x18\x05 \x01(\x08\x12[\n\x17\x62\x61rcoding_configuration\x18\n \x01(\x0b\x32:.minknow_api.analysis_configuration.BarcodingConfiguration\"$\n\x16StartBarcodingResponse\x12\n\n\x02id\x18\x01 \x01(\t\"\xd6\x01\n\x15StartAlignmentRequest\x12\x0c\n\x04name\x18\x07 \x01(\t\x12\x1f\n\x17input_reads_directories\x18\x01 \x03(\t\x12\x1e\n\x16output_reads_directory\x18\x02 \x01(\t\x12\x11\n\trecursive\x18\x04 \x01(\x08\x12[\n\x17\x61lignment_configuration\x18\x06 \x01(\x0b\x32:.minknow_api.analysis_configuration.AlignmentConfiguration\"$\n\x16StartAlignmentResponse\x12\n\n\x02id\x18\x01 \x01(\t\"\xce\x03\n\"StartPostProcessingProtocolRequest\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\"\n\x1asequencing_protocol_run_id\x18\x07 \x01(\t\x12\x1d\n\x15input_fast5_directory\x18\x02 \x01(\t\x12\x1d\n\x15input_fastq_directory\x18\x03 \x01(\t\x12\x1b\n\x13input_bam_directory\x18\x04 \x01(\t\x12\x19\n\x11sample_sheet_path\x18\x08 \x01(\t\x12\x18\n\x10output_directory\x18\x05 \x01(\t\x12\x65\n\x0esetting_values\x18\x06 \x03(\x0b\x32M.minknow_api.basecaller.StartPostProcessingProtocolRequest.SettingValuesEntry\x1ay\n\x12SettingValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12R\n\x05value\x18\x02 \x01(\x0b\x32\x43.minknow_api.protocol_settings.ProtocolSetting.ProtocolSettingValue:\x02\x38\x01\"\x87\x03\n\x0cStartRequest\x12T\n\x19start_basecalling_request\x18\x02 \x01(\x0b\x32/.minknow_api.basecaller.StartBasecallingRequestH\x00\x12P\n\x17start_barcoding_request\x18\x03 \x01(\x0b\x32-.minknow_api.basecaller.StartBarcodingRequestH\x00\x12P\n\x17start_alignment_request\x18\x04 \x01(\x0b\x32-.minknow_api.basecaller.StartAlignmentRequestH\x00\x12l\n&start_post_processing_protocol_request\x18\x05 \x01(\x0b\x32:.minknow_api.basecaller.StartPostProcessingProtocolRequestH\x00\x42\x0f\n\rstart_request\"1\n#StartPostProcessingProtocolResponse\x12\n\n\x02id\x18\x01 \x01(\t\"\x1b\n\rCancelRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x10\n\x0e\x43\x61ncelResponse\"\xb4\x05\n\x07RunInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12T\n\x19start_basecalling_request\x18\x02 \x01(\x0b\x32/.minknow_api.basecaller.StartBasecallingRequestH\x00\x12P\n\x17start_barcoding_request\x18\x0b \x01(\x0b\x32-.minknow_api.basecaller.StartBarcodingRequestH\x00\x12P\n\x17start_alignment_request\x18\x0c \x01(\x0b\x32-.minknow_api.basecaller.StartAlignmentRequestH\x00\x12l\n&start_post_processing_protocol_request\x18\r \x01(\x0b\x32:.minknow_api.basecaller.StartPostProcessingProtocolRequestH\x00\x12,\n\x05state\x18\x03 \x01(\x0e\x32\x1d.minknow_api.basecaller.State\x12\x0e\n\x06\x65rrors\x18\x04 \x03(\t\x12\x18\n\x10\x66iles_discovered\x18\x05 \x01(\x05\x12\x18\n\x10progress_current\x18\x06 \x01(\x05\x12\x16\n\x0eprogress_total\x18\x07 \x01(\x05\x12.\n\nstart_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x12\x65stimated_end_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x15\n\x13start_request_oneof\"\xbc\x01\n\x0eGetInfoRequest\x12\x39\n\x06preset\x18\x01 \x01(\x0e\x32\'.minknow_api.basecaller.SelectionPresetH\x00\x12\x0c\n\x02id\x18\x02 \x01(\tH\x00\x12=\n\x04list\x18\x03 \x01(\x0b\x32-.minknow_api.basecaller.GetInfoRequest.IdListH\x00\x1a\x15\n\x06IdList\x12\x0b\n\x03ids\x18\x01 \x03(\tB\x0b\n\tselection\"@\n\x0fGetInfoResponse\x12-\n\x04runs\x18\x01 \x03(\x0b\x32\x1f.minknow_api.basecaller.RunInfo\"\x1f\n\x10\x43learInfoRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"\x13\n\x11\x43learInfoResponse\"*\n\x0cWatchRequest\x12\x1a\n\x12send_finished_runs\x18\x01 \x01(\x08\">\n\rWatchResponse\x12-\n\x04runs\x18\x01 \x03(\x0b\x32\x1f.minknow_api.basecaller.RunInfo\"^\n\x19MakeAlignmentIndexRequest\x12!\n\x19input_alignment_reference\x18\x01 \x01(\t\x12\x1e\n\x16output_alignment_index\x18\x02 \x01(\t\"\x1c\n\x1aMakeAlignmentIndexResponse\"$\n\"ListPostProcessingProtocolsRequest\"\xa6\x01\n\x1aPostProcessingProtocolInfo\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12@\n\x08provider\x18\x05 \x01(\x0e\x32..minknow_api.basecaller.PostProcessingProvider\"l\n#ListPostProcessingProtocolsResponse\x12\x45\n\tprotocols\x18\x01 \x03(\x0b\x32\x32.minknow_api.basecaller.PostProcessingProtocolInfo\"B\n,ListSettingsForPostProcessingProtocolRequest\x12\x12\n\nidentifier\x18\x01 \x01(\t\"\xd2\x01\n-ListSettingsForPostProcessingProtocolResponse\x12\x1c\n\x14requires_fast5_input\x18\x01 \x01(\x08\x12\x1c\n\x14requires_fastq_input\x18\x02 \x01(\x08\x12\x1a\n\x12requires_bam_input\x18\x03 \x01(\x08\x12I\n\x11protocol_settings\x18\x04 \x03(\x0b\x32..minknow_api.protocol_settings.ProtocolSetting\"5\n\x15UpdateProgressRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08progress\x18\x02 \x01(\x02\"\x18\n\x16UpdateProgressResponse\"*\n\x0fSendPingRequest\x12\x17\n\tping_data\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\"\x12\n\x10SendPingResponse*S\n\x05State\x12\x11\n\rSTATE_RUNNING\x10\x00\x12\x11\n\rSTATE_SUCCESS\x10\x01\x12\x0f\n\x0bSTATE_ERROR\x10\x02\x12\x13\n\x0fSTATE_CANCELLED\x10\x03*[\n\x0fSelectionPreset\x12\x16\n\x12PRESET_ALL_RUNNING\x10\x00\x12 \n\x1cPRESET_MOST_RECENTLY_STARTED\x10\x01\x12\x0e\n\nPRESET_ALL\x10\x02*0\n\x16PostProcessingProvider\x12\n\n\x06SCRIPT\x10\x00\x12\n\n\x06\x45PI2ME\x10\x01\x32\xe5\r\n\nBasecaller\x12}\n\x13list_configs_by_kit\x12/.minknow_api.basecaller.ListConfigsByKitRequest\x1a\x30.minknow_api.basecaller.ListConfigsByKitResponse\"\x03\x90\x02\x01\x12x\n\x11start_basecalling\x12/.minknow_api.basecaller.StartBasecallingRequest\x1a\x30.minknow_api.basecaller.StartBasecallingResponse\"\x00\x12r\n\x0fstart_barcoding\x12-.minknow_api.basecaller.StartBarcodingRequest\x1a..minknow_api.basecaller.StartBarcodingResponse\"\x00\x12\x9b\x01\n\x1estart_post_processing_protocol\x12:.minknow_api.basecaller.StartPostProcessingProtocolRequest\x1a;.minknow_api.basecaller.StartPostProcessingProtocolResponse\"\x00\x12r\n\x0fstart_alignment\x12-.minknow_api.basecaller.StartAlignmentRequest\x1a..minknow_api.basecaller.StartAlignmentResponse\"\x00\x12\\\n\x06\x63\x61ncel\x12%.minknow_api.basecaller.CancelRequest\x1a&.minknow_api.basecaller.CancelResponse\"\x03\x90\x02\x02\x12\x62\n\x08get_info\x12&.minknow_api.basecaller.GetInfoRequest\x1a\'.minknow_api.basecaller.GetInfoResponse\"\x03\x90\x02\x01\x30\x01\x12\x66\n\nclear_info\x12(.minknow_api.basecaller.ClearInfoRequest\x1a).minknow_api.basecaller.ClearInfoResponse\"\x03\x90\x02\x02\x12[\n\x05watch\x12$.minknow_api.basecaller.WatchRequest\x1a%.minknow_api.basecaller.WatchResponse\"\x03\x90\x02\x01\x30\x01\x12\x7f\n\x14make_alignment_index\x12\x31.minknow_api.basecaller.MakeAlignmentIndexRequest\x1a\x32.minknow_api.basecaller.MakeAlignmentIndexResponse\"\x00\x12\x9e\x01\n\x1elist_post_processing_protocols\x12:.minknow_api.basecaller.ListPostProcessingProtocolsRequest\x1a;.minknow_api.basecaller.ListPostProcessingProtocolsResponse\"\x03\x90\x02\x02\x12\xbe\x01\n*list_settings_for_post_processing_protocol\x12\x44.minknow_api.basecaller.ListSettingsForPostProcessingProtocolRequest\x1a\x45.minknow_api.basecaller.ListSettingsForPostProcessingProtocolResponse\"\x03\x90\x02\x01\x12\x8b\x01\n(update_post_processing_protocol_progress\x12-.minknow_api.basecaller.UpdateProgressRequest\x1a..minknow_api.basecaller.UpdateProgressResponse\"\x00\x12`\n\tsend_ping\x12\'.minknow_api.basecaller.SendPingRequest\x1a(.minknow_api.basecaller.SendPingResponse\"\x00\x42&\n\x1c\x63om.nanoporetech.minknow_api\xa2\x02\x05MKAPIb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.basecaller_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.nanoporetech.minknow_api\242\002\005MKAPI'
  _globals['_LISTCONFIGSBYKITRESPONSE_PERFLOWCELL_KITCONFIGSENTRY']._options = None
  _globals['_LISTCONFIGSBYKITRESPONSE_PERFLOWCELL_KITCONFIGSENTRY']._serialized_options = b'8\001'
  _globals['_LISTCONFIGSBYKITRESPONSE_FLOWCELLCONFIGSENTRY']._options = None
  _globals['_LISTCONFIGSBYKITRESPONSE_FLOWCELLCONFIGSENTRY']._serialized_options = b'8\001'
  _globals['_STARTPOSTPROCESSINGPROTOCOLREQUEST_SETTINGVALUESENTRY']._options = None
  _globals['_STARTPOSTPROCESSINGPROTOCOLREQUEST_SETTINGVALUESENTRY']._serialized_options = b'8\001'
  _globals['_SENDPINGREQUEST'].fields_by_name['ping_data']._options = None
  _globals['_SENDPINGREQUEST'].fields_by_name['ping_data']._serialized_options = b'\210\265\030\001'
  _globals['_BASECALLER'].methods_by_name['list_configs_by_kit']._options = None
  _globals['_BASECALLER'].methods_by_name['list_configs_by_kit']._serialized_options = b'\220\002\001'
  _globals['_BASECALLER'].methods_by_name['cancel']._options = None
  _globals['_BASECALLER'].methods_by_name['cancel']._serialized_options = b'\220\002\002'
  _globals['_BASECALLER'].methods_by_name['get_info']._options = None
  _globals['_BASECALLER'].methods_by_name['get_info']._serialized_options = b'\220\002\001'
  _globals['_BASECALLER'].methods_by_name['clear_info']._options = None
  _globals['_BASECALLER'].methods_by_name['clear_info']._serialized_options = b'\220\002\002'
  _globals['_BASECALLER'].methods_by_name['watch']._options = None
  _globals['_BASECALLER'].methods_by_name['watch']._serialized_options = b'\220\002\001'
  _globals['_BASECALLER'].methods_by_name['list_post_processing_protocols']._options = None
  _globals['_BASECALLER'].methods_by_name['list_post_processing_protocols']._serialized_options = b'\220\002\002'
  _globals['_BASECALLER'].methods_by_name['list_settings_for_post_processing_protocol']._options = None
  _globals['_BASECALLER'].methods_by_name['list_settings_for_post_processing_protocol']._serialized_options = b'\220\002\001'
  _globals['_STATE']._serialized_start=4771
  _globals['_STATE']._serialized_end=4854
  _globals['_SELECTIONPRESET']._serialized_start=4856
  _globals['_SELECTIONPRESET']._serialized_end=4947
  _globals['_POSTPROCESSINGPROVIDER']._serialized_start=4949
  _globals['_POSTPROCESSINGPROVIDER']._serialized_end=4997
  _globals['_LISTCONFIGSBYKITREQUEST']._serialized_start=231
  _globals['_LISTCONFIGSBYKITREQUEST']._serialized_end=256
  _globals['_LISTCONFIGSBYKITRESPONSE']._serialized_start=259
  _globals['_LISTCONFIGSBYKITRESPONSE']._serialized_end=759
  _globals['_LISTCONFIGSBYKITRESPONSE_CONFIGLIST']._serialized_start=385
  _globals['_LISTCONFIGSBYKITRESPONSE_CONFIGLIST']._serialized_end=414
  _globals['_LISTCONFIGSBYKITRESPONSE_PERFLOWCELL']._serialized_start=417
  _globals['_LISTCONFIGSBYKITRESPONSE_PERFLOWCELL']._serialized_end=641
  _globals['_LISTCONFIGSBYKITRESPONSE_PERFLOWCELL_KITCONFIGSENTRY']._serialized_start=531
  _globals['_LISTCONFIGSBYKITRESPONSE_PERFLOWCELL_KITCONFIGSENTRY']._serialized_end=641
  _globals['_LISTCONFIGSBYKITRESPONSE_FLOWCELLCONFIGSENTRY']._serialized_start=643
  _globals['_LISTCONFIGSBYKITRESPONSE_FLOWCELLCONFIGSENTRY']._serialized_end=759
  _globals['_STARTBASECALLINGREQUEST']._serialized_start=762
  _globals['_STARTBASECALLINGREQUEST']._serialized_end=1255
  _globals['_STARTBASECALLINGRESPONSE']._serialized_start=1257
  _globals['_STARTBASECALLINGRESPONSE']._serialized_end=1295
  _globals['_STARTBARCODINGREQUEST']._serialized_start=1298
  _globals['_STARTBARCODINGREQUEST']._serialized_end=1536
  _globals['_STARTBARCODINGRESPONSE']._serialized_start=1538
  _globals['_STARTBARCODINGRESPONSE']._serialized_end=1574
  _globals['_STARTALIGNMENTREQUEST']._serialized_start=1577
  _globals['_STARTALIGNMENTREQUEST']._serialized_end=1791
  _globals['_STARTALIGNMENTRESPONSE']._serialized_start=1793
  _globals['_STARTALIGNMENTRESPONSE']._serialized_end=1829
  _globals['_STARTPOSTPROCESSINGPROTOCOLREQUEST']._serialized_start=1832
  _globals['_STARTPOSTPROCESSINGPROTOCOLREQUEST']._serialized_end=2294
  _globals['_STARTPOSTPROCESSINGPROTOCOLREQUEST_SETTINGVALUESENTRY']._serialized_start=2173
  _globals['_STARTPOSTPROCESSINGPROTOCOLREQUEST_SETTINGVALUESENTRY']._serialized_end=2294
  _globals['_STARTREQUEST']._serialized_start=2297
  _globals['_STARTREQUEST']._serialized_end=2688
  _globals['_STARTPOSTPROCESSINGPROTOCOLRESPONSE']._serialized_start=2690
  _globals['_STARTPOSTPROCESSINGPROTOCOLRESPONSE']._serialized_end=2739
  _globals['_CANCELREQUEST']._serialized_start=2741
  _globals['_CANCELREQUEST']._serialized_end=2768
  _globals['_CANCELRESPONSE']._serialized_start=2770
  _globals['_CANCELRESPONSE']._serialized_end=2786
  _globals['_RUNINFO']._serialized_start=2789
  _globals['_RUNINFO']._serialized_end=3481
  _globals['_GETINFOREQUEST']._serialized_start=3484
  _globals['_GETINFOREQUEST']._serialized_end=3672
  _globals['_GETINFOREQUEST_IDLIST']._serialized_start=3638
  _globals['_GETINFOREQUEST_IDLIST']._serialized_end=3659
  _globals['_GETINFORESPONSE']._serialized_start=3674
  _globals['_GETINFORESPONSE']._serialized_end=3738
  _globals['_CLEARINFOREQUEST']._serialized_start=3740
  _globals['_CLEARINFOREQUEST']._serialized_end=3771
  _globals['_CLEARINFORESPONSE']._serialized_start=3773
  _globals['_CLEARINFORESPONSE']._serialized_end=3792
  _globals['_WATCHREQUEST']._serialized_start=3794
  _globals['_WATCHREQUEST']._serialized_end=3836
  _globals['_WATCHRESPONSE']._serialized_start=3838
  _globals['_WATCHRESPONSE']._serialized_end=3900
  _globals['_MAKEALIGNMENTINDEXREQUEST']._serialized_start=3902
  _globals['_MAKEALIGNMENTINDEXREQUEST']._serialized_end=3996
  _globals['_MAKEALIGNMENTINDEXRESPONSE']._serialized_start=3998
  _globals['_MAKEALIGNMENTINDEXRESPONSE']._serialized_end=4026
  _globals['_LISTPOSTPROCESSINGPROTOCOLSREQUEST']._serialized_start=4028
  _globals['_LISTPOSTPROCESSINGPROTOCOLSREQUEST']._serialized_end=4064
  _globals['_POSTPROCESSINGPROTOCOLINFO']._serialized_start=4067
  _globals['_POSTPROCESSINGPROTOCOLINFO']._serialized_end=4233
  _globals['_LISTPOSTPROCESSINGPROTOCOLSRESPONSE']._serialized_start=4235
  _globals['_LISTPOSTPROCESSINGPROTOCOLSRESPONSE']._serialized_end=4343
  _globals['_LISTSETTINGSFORPOSTPROCESSINGPROTOCOLREQUEST']._serialized_start=4345
  _globals['_LISTSETTINGSFORPOSTPROCESSINGPROTOCOLREQUEST']._serialized_end=4411
  _globals['_LISTSETTINGSFORPOSTPROCESSINGPROTOCOLRESPONSE']._serialized_start=4414
  _globals['_LISTSETTINGSFORPOSTPROCESSINGPROTOCOLRESPONSE']._serialized_end=4624
  _globals['_UPDATEPROGRESSREQUEST']._serialized_start=4626
  _globals['_UPDATEPROGRESSREQUEST']._serialized_end=4679
  _globals['_UPDATEPROGRESSRESPONSE']._serialized_start=4681
  _globals['_UPDATEPROGRESSRESPONSE']._serialized_end=4705
  _globals['_SENDPINGREQUEST']._serialized_start=4707
  _globals['_SENDPINGREQUEST']._serialized_end=4749
  _globals['_SENDPINGRESPONSE']._serialized_start=4751
  _globals['_SENDPINGRESPONSE']._serialized_end=4769
  _globals['_BASECALLER']._serialized_start=5000
  _globals['_BASECALLER']._serialized_end=6765
RunInfo.__doc__ = """Attributes:
    id:
        The ID of the run, as returned by start().
    start_request_oneof:
        The original message used to start the run.
    start_basecalling_request:
        Set if basecalling reads
    start_barcoding_request:
        Set if barcoding reads
    start_alignment_request:
        Set if aligning reads
    start_post_processing_protocol_request:
        Set if aligning reads
    state:
        What state the run is in.  While the basecalling is running
        the state field will be ``STATE_RUNNING``.
    errors:
        If state is STATE_ERROR, this will contain (some of) the
        errors encountered.  Note that if there are a lot of errors,
        only some may be returned.
    files_discovered:
        The number of files selected for input.
    progress_current:
        The current basecalling progress (with respect to
        progress_total).  This is intended to be an estimate of how
        close to completion the basecalling run is. The numbers have
        no particular meaning other than as a proportion of
        progress_total.  Note that this only really has useful meaning
        while state is STATE_RUNNING. On STATE_SUCCESS, it will always
        be the same as progress_total. On STATE_ERROR or
        STATE_CANCELLED, it may give some indication of how far
        through basecalling was when it failed or was cancelled.
    progress_total:
        The maximum value of progress_current.  (progress_current /
        progress_total) * 100 will give a percentage completion.  If
        this is 0, it should be interpreted as "unknown progress".
    start_time:
        When basecalling was started (UTC).
    end_time:
        When basecalling ended (UTC).  Unset if basecalling is still
        running.
    estimated_end_time:
        An estimate for when basecalling will end (UTC).  Unset if
        basecalling has finished, or if an estimate cannot be
        calculated (eg: because the baescalling software does not
        support it).  Since 3.6.
"""
StartAlignmentRequest.__doc__ = """Attributes:
    name:
        User specified name to identify the alignment run.
    input_reads_directories:
        Input directories to search for reads to be aligned.
        Currently, only one directory can be specified, but this
        definition allows for multiple in the future without breaking
        compatibility.
    output_reads_directory:
        Output directory where aligned reads will be placed.
    recursive:
        Recursively find fast5 files to align in the
        `input_reads_directories`.  If False, only the fast5 files
        directly in one of the `input_reads_directories` will be
        aligned. If True, subdirectories of those directories will
        also be searched recursively.
    alignment_configuration:
        Options to control alignment performed once basecalling reads
        is complete.
"""
ListSettingsForPostProcessingProtocolRequest.__doc__ = """Attributes:
    identifier:
        specify the protocol with a string containing all the
        protocol's identifying components, eg:
        "SYSTEM:post_processing/artic"
"""
StartPostProcessingProtocolResponse.__doc__ = """Attributes:
    id:
        An identifier for the protocol run that was started. This can
        be used to monitor or cancel the run.
"""
StartPostProcessingProtocolRequest.__doc__ = """Attributes:
    identifier:
        identifier value from a protocol returned from
        list_post_processing_protocols.
    sequencing_protocol_run_id:
        Optionally specify a sequencing protocol that is linked with
        this analysis.
    input_fast5_directory:
        Input directories for the protocol (omit those which the
        protocol doesn't require).
    sample_sheet_path:
        Path to the sample sheet output by minknow
    output_directory:
        Output directory where the analysed output should be written.
    setting_values:
        Configured values for display settings for the protocol (see
        basecaller.list_settings_for_protocol) keys missing from the
        original protocol will cause errors.
"""
ListSettingsForPostProcessingProtocolResponse.__doc__ = """Attributes:
    requires_fast5_input:
        Does the protocol require fast5 files as input
    requires_fastq_input:
        Does the protocol require fastq files as input
    requires_bam_input:
        Does the protocol require bam files as input
    protocol_settings:
        List of protocol settings used by the post processing protocol
"""
ListConfigsByKitResponse.ConfigList.__doc__ = """Attributes:
    configs:
        List of configuration names, to be used in
        ``StartBasecallingRequest.configuration``
"""
StartRequest.__doc__ = """ Protobuf messages for input/output of RPC calls

Attributes:
    dont_wait_for_device_ready:
        Prevent waiting until the device is ready before starting
        acquisition.  Defaults to false.  By default, MinKNOW will
        block in the start() call for the device and flow cell to be
        ready for acquisition (which may take several seconds after
        plugging in the flow cell on some devices). Setting this
        option will cause the call to return with an error if the
        device is not already prepared to acquire data.  Since 1.14
    generate_report:
        Generate duty time and throughput reports.  Note that this
        setting will be ignored (and no reports will be generated) if
        no protocol is running at the time acquisition is started.
        The default setting (AUTO) will only generate reports if
        purpose is set to SEQUENCING.  Since 3.0
    send_sequencing_read_metrics:
        Whether sequencing read metrics should be reported to Oxford
        Nanopore.  These are performance metrics that are used to
        improve the sequencing technology. They do not include any
        actual sequencing data, only statistics about read lengths,
        duty time and similar generic performance information.  The
        default setting (AUTO) will only send metrics if purpose is
        set to SEQUENCING.  Since 3.0
    send_basecalling_metrics:
        Whether basecalling metrics should be reported to Oxford
        Nanopore.  These are performance metrics that are used to
        improve the sequencing technology. They do not include any
        actual sequencing data, only statistics about basecalling
        performance.  The default setting (AUTO) will only send
        metrics if purpose is set to SEQUENCING.  NB: this setting is
        ignored if live basecalling is not enabled, since there will
        be no metrics to send.  Since 3.2
    purpose:
        Specify the purpose of this acquisition period.  This affects
        various defaults (see the Purpose enum documentation for more
        details). It may also affect how the user interface presents
        the state of the protocol.  Since 3.2
    analysis:
        Perform analysis for this acquisition period.  If this is
        disabled, no reads, no events, no channel states and no
        basecalls will be generated. Any RPCs that depend on any of
        these will fail. No reads-based files will be produced at all,
        regardless of any other settings.  This is mostly useful for
        calibration (although you should normally use the purpose
        field rather than setting this explicitly).  The default
        setting (AUTO) will use the persistent setting from the
        analysis_configuraiton service, unless the purpose is set to
        CALIBRATION.  Since 3.2
    file_output:
        Allow file output for this acquisition period.  If this is
        disabled, the file output settings will be ignored for this
        acquisition period, and no data files will be produced. Note
        that reports are NOT managed by this setting.  Note that
        setting this to FORCE will simply make file output respect the
        bulk and read writer configurations. If each file output type
        is disabled, you will still get no file output.  This is
        mostly useful for calibration (although you should normally
        use the purpose field rather than setting this explicitly).
        The default setting (AUTO) will only suppress file output if
        purpose is set to CALIBRATION.  Since 3.2
    generate_final_summary:
        Write a final_summary.txt file.  If file_output is disabled,
        the final_summary.txt file will not be written regardless of
        this setting.  The default setting (AUTO) will only enable
        writing a final_summary.txt file if the purpose is set to
        SEQUENCING.  Since 3.5 (NB: in 3.3 and 3.4, final_summary.txt
        was always written out if file_output was enabled).
    start_request:
        Start request that will be used to trigger analysis, used to
        union over all the different types of analysis possible.
"""
MakeAlignmentIndexRequest.__doc__ = """Attributes:
    input_alignment_reference:
        Input fasta reference to use for building the index.
    output_alignment_index:
        Output file path to write index (mmi file) to.  Must have a
        ".mmi" extension, and the paths parent directory must exist.
"""
StartBarcodingRequest.__doc__ = """Attributes:
    name:
        User specified name to identify the barcoding run.
    input_reads_directories:
        Input directories to search for reads to be basecalled.
        Currently, only one directory can be specified, but this
        definition allows for multiple in the future without breaking
        compatibility.
    output_reads_directory:
        Output directory where called reads will be placed.  Reads
        will be sorted into subdirectories based on the sequencing run
        they came from.
    compress_fastq:
        Enable gzip compression of output FASTQ files.
    recursive:
        Recursively find fast5 files to basecall in the
        `input_reads_directories`.  If False, only the fast5 files
        directly in one of the `input_reads_directories` will be
        basecalled. If True, subdirectories of those directories will
        also be searched recursively.
    barcoding_configuration:
        Options to control barcoding performed once basecalling reads
        is complete.
"""
WatchResponse.__doc__ = """Attributes:
    runs:
        The current state of some of the runs.
    values:
        The values that have changed.  The first received message will
        contain the current state of all the watched values.
        Subsequent messages will only contain the values that changed.
    removed_values:
        The values that have been removed.
"""
StartBasecallingResponse.__doc__ = """Attributes:
    id:
        An identifier for the basecalling run that was started. This
        can be used to monitor or cancel the run.
"""
ListConfigsByKitResponse.__doc__ = """Attributes:
    flow_cell_configs:
        Key: flow cell type (eg: "FLO-MIN107") Value: FlowCellConfigs
        describing configurations available for that flow cell.
"""
PostProcessingProtocolInfo.__doc__ = """Attributes:
    identifier:
        System identifier for the protocol
    name:
        Readable name for the protocol (appropriate for use as a key
        in translation database).  Note that this may not be unique:
        in particular, the EPI2ME provider lists every version of a
        workflow as a separate post-processing protocol.
    version:
        Protocol version.  This might not be set for all protocols or
        all providers.
    description:
        A description of the protocol.
    provider:
        The source of the post-processing protocol.
"""
GetInfoResponse.__doc__ = """Attributes:
    runs:
        Information about the requested runs.
"""
SendPingResponse.__doc__ = """Since 5.0"""
WatchRequest.__doc__ = """Attributes:
    send_finished_runs:
        By default, no information will be sent about runs that were
        already finished when this call was made. Setting this to true
        will cause the state of already-finished runs to be returned.
    names:
        The names of the values you wish to watch.
    allow_missing:
        Whether to allow missing values.  If set, names that are not
        present in the store will be omitted from the first response,
        but will still be watched. If and when they are added, a
        message will be sent with the set values. Otherwise, missing
        values will cause an immediate error.  Defaults to 'false'
"""
SendPingRequest.__doc__ = """Since 5.0

Attributes:
    ping_data:
        The json data to send as a ping.  note: if this string is not
        a valid json object, an error will be raised.
    days_until_expiry:
        Should the ping fail to send, the number of days the ping will
        be stored before being cleaned up.
"""
ListConfigsByKitResponse.PerFlowCell.__doc__ = """Attributes:
    kit_configs:
        Key: kit name (eg: "SQK-LSK109") Value: list of configuration
        names
"""
UpdateProgressRequest.__doc__ = """Attributes:
    id:
        id of the protocol to update (stored in environment variable
        for python process)
    progress:
        Progress indicator, 0-1.
"""
StartBasecallingRequest.__doc__ = """Attributes:
    name:
        User specified name to identify the basecall run.
    input_reads_directories:
        Input directories to search for reads to be basecalled.
        Currently, only one directory can be specified, but this
        definition allows for multiple in the future without breaking
        compatibility.
    output_reads_directory:
        Output directory where called reads will be placed.  Reads
        will be sorted into subdirectories based on the sequencing run
        they came from.
    configuration:
        The name of the basecalling configuration to use.
    fast5_out:
        Enable output of .fast5 files containing original raw reads,
        event data/trace table from basecall and basecall result
        sequence.  This causes .fast5 files to be output in addition
        to FASTQ files.  DEPRECATED: This option does not have any
        effect - the basecaller no longer has the ability to write
        fast5 files.
    compress_fastq:
        Enable gzip compression of output FASTQ files.
    disable_events:
        Prevent events / trace tables being written to .fast5 files.
        If event tables are not required for downstream processing
        (eg: for 1d^2) then it is more efficient (and produces smaller
        files) to disable them.  This has no effect if ``fast5_out``
        is not enabled.
    recursive:
        Recursively find fast5 files to basecall in the
        `input_reads_directories`.  If False, only the fast5 files
        directly in one of the `input_reads_directories` will be
        basecalled. If True, subdirectories of those directories will
        also be searched recursively.
    barcoding_configuration:
        Options to control barcoding performed once basecalling reads
        is complete.
    alignment_configuration:
        Options to control alignment performed once basecalling reads
        is complete.
    enable_read_splitting:
        Enable read splitting in guppy  Note: Since 5.9 this option
        has no effect, the basecaller is responsible for deciding when
        read splitting should be enabled.
    min_score_read_splitting:
        Override score to use for guppy read splitting. If not
        specified a default value is used from guppy.  Note: Since 5.9
        this option has no effect, the basecaller is responsible for
        deciding when read splitting should be enabled.
"""
StartBarcodingResponse.__doc__ = """Attributes:
    id:
        An identifier for the basecalling run that was started. This
        can be used to monitor or cancel the run.
"""
StartAlignmentResponse.__doc__ = """Attributes:
    id:
        An identifier for the alignment run that was started. This can
        be used to monitor or cancel the run.
"""
CancelRequest.__doc__ = """Attributes:
    id:
        An identifier as returned from a call to start() or list().
"""
GetInfoRequest.__doc__ = """Attributes:
    selection:
        The selection of runs to return information about.  If no
        selection is provided, the call will return all currently-
        running basecall runs (as though PRESET_ALL_RUNNING were
        selected).
    preset:
        A pre-determined selection of runs.
    id:
        An identifier, as returned by start().
    list:
        A list of identifiers, as returned by start().
"""
# @@protoc_insertion_point(module_scope)
