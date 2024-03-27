# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/promethion_device.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from minknow_api import rpc_options_pb2 as minknow__api_dot_rpc__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#minknow_api/promethion_device.proto\x12\x1dminknow_api.promethion_device\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1dminknow_api/rpc_options.proto\"7\n\x10WaveformSettings\x12\x10\n\x08voltages\x18\x01 \x03(\x01\x12\x11\n\tfrequency\x18\x02 \x01(\x01\"\xfb\x03\n\x0e\x44\x65viceSettings\x12\x37\n\x12sampling_frequency\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x32\n\x0cramp_voltage\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x16\n\x0c\x62ias_voltage\x18\x03 \x01(\x01H\x00\x12P\n\x15\x62ias_voltage_waveform\x18\x04 \x01(\x0b\x32/.minknow_api.promethion_device.WaveformSettingsH\x00\x12>\n\x1asaturation_control_enabled\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12<\n\x18\x66\x61st_calibration_enabled\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x37\n\x12temperature_target\x18\x07 \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12\x43\n\x07timings\x18\x08 \x01(\x0b\x32\x32.minknow_api.promethion_device.TimingEnginePeriodsB\x16\n\x14\x62ias_voltage_setting\"\xf5\x04\n\x13TimingEnginePeriods\x12*\n\x04RST1\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12/\n\tRST1_CDS1\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12*\n\x04\x43\x44S1\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12/\n\tCDS1_DATA\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12*\n\x04\x44\x41TA\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12/\n\tDATA_RST2\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12*\n\x04RST2\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12/\n\tRST2_CDS2\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12*\n\x04\x43\x44S2\x18\t \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12-\n\x07\x43\x44S2_SH\x18\n \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12(\n\x02SH\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12-\n\x07SH_RST1\x18\x0c \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x36\n\x12use_default_values\x18\r \x01(\x0b\x32\x1a.google.protobuf.BoolValue\"\x8e\x01\n\x12PixelBlockSettings\x12\x41\n\x1bregen_current_voltage_clamp\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x35\n\x0funblock_voltage\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\"\xaf\x11\n\rPixelSettings\x12\x45\n\x05input\x18\x01 \x01(\x0b\x32\x36.minknow_api.promethion_device.PixelSettings.InputWell\x12P\n\roverload_mode\x18\x02 \x01(\x0e\x32\x39.minknow_api.promethion_device.PixelSettings.OverloadMode\x12T\n\x10\x63utoff_frequency\x18\x03 \x01(\x0e\x32:.minknow_api.promethion_device.PixelSettings.LowPassFilter\x12T\n\x0fgain_multiplier\x18\x04 \x01(\x0e\x32;.minknow_api.promethion_device.PixelSettings.GainMultiplier\x12R\n\x0egain_capacitor\x18\x05 \x01(\x0e\x32:.minknow_api.promethion_device.PixelSettings.GainCapacitor\x12V\n\x10\x63\x61libration_mode\x18\x06 \x01(\x0e\x32<.minknow_api.promethion_device.PixelSettings.CalibrationMode\x12Q\n\x0funblock_voltage\x18\x07 \x01(\x0e\x32\x38.minknow_api.promethion_device.PixelSettings.UnblockMode\x12\x34\n\x10\x63urrent_inverted\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x1bmembrane_simulation_enabled\x18\t \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12^\n\x14regeneration_current\x18\n \x01(\x0e\x32@.minknow_api.promethion_device.PixelSettings.RegenerationCurrent\x12\x45\n!regeneration_current_test_enabled\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12N\n\x0c\x62ias_current\x18\x0c \x01(\x0e\x32\x38.minknow_api.promethion_device.PixelSettings.BiasCurrent\x1a\x94\x02\n\tInputWell\x12V\n\ninput_well\x18\x01 \x01(\x0e\x32\x42.minknow_api.promethion_device.PixelSettings.InputWell.InputConfig\x12]\n\x11regeneration_well\x18\x02 \x01(\x0e\x32\x42.minknow_api.promethion_device.PixelSettings.InputWell.InputConfig\"P\n\x0bInputConfig\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06WELL_1\x10\x01\x12\n\n\x06WELL_2\x10\x02\x12\n\n\x06WELL_3\x10\x03\x12\n\n\x06WELL_4\x10\x04\x12\x07\n\x03\x41LL\x10\x05\"x\n\x0cOverloadMode\x12\x11\n\rOVERLOAD_KEEP\x10\x00\x12\x15\n\x11OVERLOAD_SET_FLAG\x10\x01\x12\x16\n\x12OVERLOAD_LATCH_OFF\x10\x02\x12\x12\n\x0eOVERLOAD_CLEAR\x10\x03\x12\x12\n\x0eOVERLOAD_LIMIT\x10\x04\"\x95\x01\n\rLowPassFilter\x12\x0c\n\x08LPF_KEEP\x10\x00\x12\r\n\tLPF_10kHz\x10\x01\x12\r\n\tLPF_20kHz\x10\x02\x12\r\n\tLPF_30kHz\x10\x03\x12\r\n\tLPF_40kHz\x10\x04\x12\r\n\tLPF_50kHz\x10\x05\x12\r\n\tLPF_60kHz\x10\x06\x12\r\n\tLPF_70kHz\x10\x07\x12\r\n\tLPF_80kHz\x10\x08\"@\n\x0eGainMultiplier\x12\x10\n\x0cINTGAIN_KEEP\x10\x00\x12\r\n\tINTGAIN_2\x10\x01\x12\r\n\tINTGAIN_4\x10\x02\"h\n\rGainCapacitor\x12\x0f\n\x0bINTCAP_KEEP\x10\x00\x12\x10\n\x0cINTCAP_100fF\x10\x01\x12\x10\n\x0cINTCAP_200fF\x10\x02\x12\x10\n\x0cINTCAP_500fF\x10\x03\x12\x10\n\x0cINTCAP_600fF\x10\x04\"A\n\x0f\x43\x61librationMode\x12\x0e\n\nCALIB_KEEP\x10\x00\x12\x0e\n\nCALIB_FAST\x10\x01\x12\x0e\n\nCALIB_SLOW\x10\x02\"@\n\x0bUnblockMode\x12\x10\n\x0cUNBLOCK_KEEP\x10\x00\x12\x0e\n\nUNBLOCK_ON\x10\x01\x12\x0f\n\x0bUNBLOCK_OFF\x10\x02\"\xb6\x02\n\x13RegenerationCurrent\x12\x0e\n\nREGEN_KEEP\x10\x00\x12\r\n\tREGEN_0pA\x10\x01\x12\x0e\n\nREGEN_50pA\x10\x02\x12\x0f\n\x0bREGEN_100pA\x10\x03\x12\x0f\n\x0bREGEN_150pA\x10\x04\x12\x0f\n\x0bREGEN_400pA\x10\x05\x12\x0f\n\x0bREGEN_450pA\x10\x06\x12\x0f\n\x0bREGEN_500pA\x10\x07\x12\x0f\n\x0bREGEN_550pA\x10\x08\x12\x0f\n\x0bREGEN_800pA\x10\t\x12\x0f\n\x0bREGEN_850pA\x10\n\x12\x0f\n\x0bREGEN_900pA\x10\x0b\x12\x0f\n\x0bREGEN_950pA\x10\x0c\x12\x10\n\x0cREGEN_1200pA\x10\r\x12\x10\n\x0cREGEN_1250pA\x10\x0e\x12\x10\n\x0cREGEN_1300pA\x10\x0f\x12\x10\n\x0cREGEN_1350pA\x10\x10\"Y\n\x0b\x42iasCurrent\x12\r\n\tBIAS_KEEP\x10\x00\x12\x0c\n\x08\x42IAS_OFF\x10\x01\x12\x0c\n\x08\x42IAS_LOW\x10\x02\x12\r\n\tBIAS_HIGH\x10\x03\x12\x10\n\x0c\x42IAS_NOMINAL\x10\x04\"d\n\x1b\x43hangeDeviceSettingsRequest\x12\x45\n\x08settings\x18\x01 \x01(\x0b\x32-.minknow_api.promethion_device.DeviceSettingsB\x04\x90\xb5\x18\x01\"\\\n\x1c\x43hangeDeviceSettingsResponse\x12<\n\x17real_sampling_frequency\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\"\x1a\n\x18GetDeviceSettingsRequest\"b\n\x19GetDeviceSettingsResponse\x12\x45\n\x08settings\x18\x01 \x01(\x0b\x32-.minknow_api.promethion_device.DeviceSettingsB\x04\x90\xb5\x18\x01\"\xbf\x02\n\x1f\x43hangePixelBlockSettingsRequest\x12\x65\n\x0cpixel_blocks\x18\x01 \x03(\x0b\x32O.minknow_api.promethion_device.ChangePixelBlockSettingsRequest.PixelBlocksEntry\x12N\n\x13pixel_block_default\x18\x02 \x01(\x0b\x32\x31.minknow_api.promethion_device.PixelBlockSettings\x1a\x65\n\x10PixelBlocksEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12@\n\x05value\x18\x02 \x01(\x0b\x32\x31.minknow_api.promethion_device.PixelBlockSettings:\x02\x38\x01\"\"\n ChangePixelBlockSettingsResponse\"\x1e\n\x1cGetPixelBlockSettingsRequest\"\xeb\x01\n\x1dGetPixelBlockSettingsResponse\x12\x63\n\x0cpixel_blocks\x18\x01 \x03(\x0b\x32M.minknow_api.promethion_device.GetPixelBlockSettingsResponse.PixelBlocksEntry\x1a\x65\n\x10PixelBlocksEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12@\n\x05value\x18\x02 \x01(\x0b\x32\x31.minknow_api.promethion_device.PixelBlockSettings:\x02\x38\x01\"\x95\x02\n\x1a\x43hangePixelSettingsRequest\x12U\n\x06pixels\x18\x01 \x03(\x0b\x32\x45.minknow_api.promethion_device.ChangePixelSettingsRequest.PixelsEntry\x12\x43\n\rpixel_default\x18\x02 \x01(\x0b\x32,.minknow_api.promethion_device.PixelSettings\x1a[\n\x0bPixelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12;\n\x05value\x18\x02 \x01(\x0b\x32,.minknow_api.promethion_device.PixelSettings:\x02\x38\x01\"\x1d\n\x1b\x43hangePixelSettingsResponse\"/\n\x17GetPixelSettingsRequest\x12\x14\n\x06pixels\x18\x01 \x03(\rB\x04\x88\xb5\x18\x01\"X\n\x18GetPixelSettingsResponse\x12<\n\x06pixels\x18\x01 \x03(\x0b\x32,.minknow_api.promethion_device.PixelSettings\"2\n\x18StreamTemperatureRequest\x12\x16\n\x0eperiod_seconds\x18\x01 \x01(\r\"\x84\x02\n\x16GetTemperatureResponse\x12\x39\n\x14\x66lowcell_temperature\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12\x38\n\x13\x63hamber_temperature\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12<\n\x17pixel_block_temperature\x18\x03 \x03(\x0b\x32\x1b.google.protobuf.FloatValue\x12\x37\n\x12target_temperature\x18\x04 \x01(\x0b\x32\x1b.google.protobuf.FloatValue2\xb6\x08\n\x17PromethionDeviceService\x12\x96\x01\n\x16\x63hange_device_settings\x12:.minknow_api.promethion_device.ChangeDeviceSettingsRequest\x1a;.minknow_api.promethion_device.ChangeDeviceSettingsResponse\"\x03\x90\x02\x02\x12\x8d\x01\n\x13get_device_settings\x12\x37.minknow_api.promethion_device.GetDeviceSettingsRequest\x1a\x38.minknow_api.promethion_device.GetDeviceSettingsResponse\"\x03\x90\x02\x01\x12\xa3\x01\n\x1b\x63hange_pixel_block_settings\x12>.minknow_api.promethion_device.ChangePixelBlockSettingsRequest\x1a?.minknow_api.promethion_device.ChangePixelBlockSettingsResponse\"\x03\x90\x02\x02\x12\x9a\x01\n\x18get_pixel_block_settings\x12;.minknow_api.promethion_device.GetPixelBlockSettingsRequest\x1a<.minknow_api.promethion_device.GetPixelBlockSettingsResponse\"\x03\x90\x02\x01\x12\x93\x01\n\x15\x63hange_pixel_settings\x12\x39.minknow_api.promethion_device.ChangePixelSettingsRequest\x1a:.minknow_api.promethion_device.ChangePixelSettingsResponse\"\x03\x90\x02\x02\x12\x8a\x01\n\x12get_pixel_settings\x12\x36.minknow_api.promethion_device.GetPixelSettingsRequest\x1a\x37.minknow_api.promethion_device.GetPixelSettingsResponse\"\x03\x90\x02\x01\x12\x8b\x01\n\x12stream_temperature\x12\x37.minknow_api.promethion_device.StreamTemperatureRequest\x1a\x35.minknow_api.promethion_device.GetTemperatureResponse\"\x03\x90\x02\x01\x30\x01\x42&\n\x1c\x63om.nanoporetech.minknow_api\xa2\x02\x05MKAPIb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.promethion_device_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.nanoporetech.minknow_api\242\002\005MKAPI'
  _globals['_CHANGEDEVICESETTINGSREQUEST'].fields_by_name['settings']._options = None
  _globals['_CHANGEDEVICESETTINGSREQUEST'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_GETDEVICESETTINGSRESPONSE'].fields_by_name['settings']._options = None
  _globals['_GETDEVICESETTINGSRESPONSE'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_CHANGEPIXELBLOCKSETTINGSREQUEST_PIXELBLOCKSENTRY']._options = None
  _globals['_CHANGEPIXELBLOCKSETTINGSREQUEST_PIXELBLOCKSENTRY']._serialized_options = b'8\001'
  _globals['_GETPIXELBLOCKSETTINGSRESPONSE_PIXELBLOCKSENTRY']._options = None
  _globals['_GETPIXELBLOCKSETTINGSRESPONSE_PIXELBLOCKSENTRY']._serialized_options = b'8\001'
  _globals['_CHANGEPIXELSETTINGSREQUEST_PIXELSENTRY']._options = None
  _globals['_CHANGEPIXELSETTINGSREQUEST_PIXELSENTRY']._serialized_options = b'8\001'
  _globals['_GETPIXELSETTINGSREQUEST'].fields_by_name['pixels']._options = None
  _globals['_GETPIXELSETTINGSREQUEST'].fields_by_name['pixels']._serialized_options = b'\210\265\030\001'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['change_device_settings']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['change_device_settings']._serialized_options = b'\220\002\002'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['get_device_settings']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['get_device_settings']._serialized_options = b'\220\002\001'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['change_pixel_block_settings']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['change_pixel_block_settings']._serialized_options = b'\220\002\002'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['get_pixel_block_settings']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['get_pixel_block_settings']._serialized_options = b'\220\002\001'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['change_pixel_settings']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['change_pixel_settings']._serialized_options = b'\220\002\002'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['get_pixel_settings']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['get_pixel_settings']._serialized_options = b'\220\002\001'
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['stream_temperature']._options = None
  _globals['_PROMETHIONDEVICESERVICE'].methods_by_name['stream_temperature']._serialized_options = b'\220\002\001'
  _globals['_WAVEFORMSETTINGS']._serialized_start=133
  _globals['_WAVEFORMSETTINGS']._serialized_end=188
  _globals['_DEVICESETTINGS']._serialized_start=191
  _globals['_DEVICESETTINGS']._serialized_end=698
  _globals['_TIMINGENGINEPERIODS']._serialized_start=701
  _globals['_TIMINGENGINEPERIODS']._serialized_end=1330
  _globals['_PIXELBLOCKSETTINGS']._serialized_start=1333
  _globals['_PIXELBLOCKSETTINGS']._serialized_end=1475
  _globals['_PIXELSETTINGS']._serialized_start=1478
  _globals['_PIXELSETTINGS']._serialized_end=3701
  _globals['_PIXELSETTINGS_INPUTWELL']._serialized_start=2442
  _globals['_PIXELSETTINGS_INPUTWELL']._serialized_end=2718
  _globals['_PIXELSETTINGS_INPUTWELL_INPUTCONFIG']._serialized_start=2638
  _globals['_PIXELSETTINGS_INPUTWELL_INPUTCONFIG']._serialized_end=2718
  _globals['_PIXELSETTINGS_OVERLOADMODE']._serialized_start=2720
  _globals['_PIXELSETTINGS_OVERLOADMODE']._serialized_end=2840
  _globals['_PIXELSETTINGS_LOWPASSFILTER']._serialized_start=2843
  _globals['_PIXELSETTINGS_LOWPASSFILTER']._serialized_end=2992
  _globals['_PIXELSETTINGS_GAINMULTIPLIER']._serialized_start=2994
  _globals['_PIXELSETTINGS_GAINMULTIPLIER']._serialized_end=3058
  _globals['_PIXELSETTINGS_GAINCAPACITOR']._serialized_start=3060
  _globals['_PIXELSETTINGS_GAINCAPACITOR']._serialized_end=3164
  _globals['_PIXELSETTINGS_CALIBRATIONMODE']._serialized_start=3166
  _globals['_PIXELSETTINGS_CALIBRATIONMODE']._serialized_end=3231
  _globals['_PIXELSETTINGS_UNBLOCKMODE']._serialized_start=3233
  _globals['_PIXELSETTINGS_UNBLOCKMODE']._serialized_end=3297
  _globals['_PIXELSETTINGS_REGENERATIONCURRENT']._serialized_start=3300
  _globals['_PIXELSETTINGS_REGENERATIONCURRENT']._serialized_end=3610
  _globals['_PIXELSETTINGS_BIASCURRENT']._serialized_start=3612
  _globals['_PIXELSETTINGS_BIASCURRENT']._serialized_end=3701
  _globals['_CHANGEDEVICESETTINGSREQUEST']._serialized_start=3703
  _globals['_CHANGEDEVICESETTINGSREQUEST']._serialized_end=3803
  _globals['_CHANGEDEVICESETTINGSRESPONSE']._serialized_start=3805
  _globals['_CHANGEDEVICESETTINGSRESPONSE']._serialized_end=3897
  _globals['_GETDEVICESETTINGSREQUEST']._serialized_start=3899
  _globals['_GETDEVICESETTINGSREQUEST']._serialized_end=3925
  _globals['_GETDEVICESETTINGSRESPONSE']._serialized_start=3927
  _globals['_GETDEVICESETTINGSRESPONSE']._serialized_end=4025
  _globals['_CHANGEPIXELBLOCKSETTINGSREQUEST']._serialized_start=4028
  _globals['_CHANGEPIXELBLOCKSETTINGSREQUEST']._serialized_end=4347
  _globals['_CHANGEPIXELBLOCKSETTINGSREQUEST_PIXELBLOCKSENTRY']._serialized_start=4246
  _globals['_CHANGEPIXELBLOCKSETTINGSREQUEST_PIXELBLOCKSENTRY']._serialized_end=4347
  _globals['_CHANGEPIXELBLOCKSETTINGSRESPONSE']._serialized_start=4349
  _globals['_CHANGEPIXELBLOCKSETTINGSRESPONSE']._serialized_end=4383
  _globals['_GETPIXELBLOCKSETTINGSREQUEST']._serialized_start=4385
  _globals['_GETPIXELBLOCKSETTINGSREQUEST']._serialized_end=4415
  _globals['_GETPIXELBLOCKSETTINGSRESPONSE']._serialized_start=4418
  _globals['_GETPIXELBLOCKSETTINGSRESPONSE']._serialized_end=4653
  _globals['_GETPIXELBLOCKSETTINGSRESPONSE_PIXELBLOCKSENTRY']._serialized_start=4246
  _globals['_GETPIXELBLOCKSETTINGSRESPONSE_PIXELBLOCKSENTRY']._serialized_end=4347
  _globals['_CHANGEPIXELSETTINGSREQUEST']._serialized_start=4656
  _globals['_CHANGEPIXELSETTINGSREQUEST']._serialized_end=4933
  _globals['_CHANGEPIXELSETTINGSREQUEST_PIXELSENTRY']._serialized_start=4842
  _globals['_CHANGEPIXELSETTINGSREQUEST_PIXELSENTRY']._serialized_end=4933
  _globals['_CHANGEPIXELSETTINGSRESPONSE']._serialized_start=4935
  _globals['_CHANGEPIXELSETTINGSRESPONSE']._serialized_end=4964
  _globals['_GETPIXELSETTINGSREQUEST']._serialized_start=4966
  _globals['_GETPIXELSETTINGSREQUEST']._serialized_end=5013
  _globals['_GETPIXELSETTINGSRESPONSE']._serialized_start=5015
  _globals['_GETPIXELSETTINGSRESPONSE']._serialized_end=5103
  _globals['_STREAMTEMPERATUREREQUEST']._serialized_start=5105
  _globals['_STREAMTEMPERATUREREQUEST']._serialized_end=5155
  _globals['_GETTEMPERATURERESPONSE']._serialized_start=5158
  _globals['_GETTEMPERATURERESPONSE']._serialized_end=5418
  _globals['_PROMETHIONDEVICESERVICE']._serialized_start=5421
  _globals['_PROMETHIONDEVICESERVICE']._serialized_end=6499
ChangePixelBlockSettingsRequest.__doc__ = """Attributes:
    pixel_blocks:
        1 based map of different pixel blocks settings, a sparse map
        is accepted, keys should be integers between 1 and 12.
    pixel_block_default:
        If supplied, contains settings applied to every block before
        then applying any specific settings in the per block settings.
"""
GetPixelSettingsRequest.__doc__ = """Attributes:
    pixels:
        The channels (one based) to return data for. A sparse map is
        accepted
"""
GetTemperatureResponse.__doc__ = """Attributes:
    target_temperature:
        Return the temperature target the device is aiming to reach.
    flowcell_temperature:
        Temperature as measured by thermistor TH2 on the P-Chip.
    chamber_temperature:
        Flow-cell chamber-temperature, calculated from the pixel-block
        temperatures
    pixel_block_temperature:
        Temperature measured at each sensor in the ASIC, there are 12
        sensors, one sensor per pixel-block
"""
ChangePixelSettingsRequest.__doc__ = """Attributes:
    pixels:
        1 based map of up to 3000 different pixel settings
    pixel_default:
        If supplied, contains settings applied to every pixel before
        then applying any specific settings in the per pixel settings.
"""
PixelBlockSettings.__doc__ = """Attributes:
    regen_current_voltage_clamp:
        Voltage clamp for regeneration circuit (in millivolts)  The
        voltage in the regeneration circuit is clamped under this
        value, whilst applying the current specified in each pixel's
        settings.  The acceptable input range is -1000..1000
        (inclusive)
    unblock_voltage:
        The unblock voltage to apply when a pixel is unblocking.  The
        acceptable input range is -1000..1000 (inclusive)
"""
WaveformSettings.__doc__ = """Attributes:
    voltages:
        The waveform data applied to the device (in millivolts)  Must
        contain 32 values, in order to be a valid waveform.
    frequency:
        The frequency of the applied waveform, in Hz.  Valid values
        are between 7.8125Hz and 500Hz.
"""
GetPixelBlockSettingsResponse.__doc__ = """Attributes:
    pixel_blocks:
        1 based map of different pixel blocks settings, containing 12
        entries.
"""
PixelSettings.InputWell.__doc__ = """Attributes:
    input_well:
        Control which well is driving the adc minknow reads from.  ALL
        is not a valid value here (other values are acceptable).
    regeneration_well:
        Control which wells are being regenerated (has the specified
        regeneration current driven to it).  All possible Input values
        are acceptable, as long as the input is not the active adc
        input. For example, { input: 1, regeneration: all } is
        invalid, as an well cannot be both input and regenerated.
"""
PixelSettings.__doc__ = """Attributes:
    input:
        The input driving the adv
    overload_mode:
        The mode the asic uses to handle currents that go above its
        adc range.
    cutoff_frequency:
        Signal filter for input adc signal.
    gain_multiplier:
        Signal gain multiplier, applied to the integrator circuit.
    gain_capacitor:
        Gain capacitor, used in the integrator circuit.
    calibration_mode:
        The calibration mode to use.
    unblock_voltage:
        Controls the application of the unblock voltage to the pixel.
    current_inverted:
        Inverts the current's polarity.
    membrane_simulation_enabled:
        Control the state of the membrane simulation.
    regeneration_current:
        Control the regeneration current used when regenerating
        well's.
    regeneration_current_test_enabled:
        Control if the regeneration current test is enabled.  This
        connects the regeneration current to the integration adc
        circuit and the input well. and allows users to read regen
        current via the channel adc value.
    bias_current:
        The bias current for the amplifier - this controls the level
        of noise of the signal.  The higher the bias current, the
        lower the noise, but the bigger the heat and power drawn by
        the amplifier. If it is set to off, no signal readings can be
        made.
"""
DeviceSettings.__doc__ = """Attributes:
    sampling_frequency:
        The number of measurements to take each second.  Possible
        values are between 1000, and 10000. If the value is outside of
        this range, it will be clamped within it  This value cannot be
        changed during acquisition.
    ramp_voltage:
        The value to apply as the ramp voltage (in millivolts)  Valid
        values are in the range -1250mv..1250mv
    bias_voltage_setting:
        Settings controlling the device bias voltage
    bias_voltage:
        The value to apply as the bias voltage (in millivolts)  Valid
        values are in the range -1250mv..1250mv
    bias_voltage_waveform:
        The waveform settings
    saturation_control_enabled:
        Enables saturation control on the device
    fast_calibration_enabled:
        Enable use of the fast calibration mode across the device
        DEPRECATED since 5.5. This will be removed in a future
        release.
    temperature_target:
        If the device is capable (see
        device.get_device_info().temperature_controllable) then this
        sets the minimum and maximum temperatures of the flow-cell.
        These values must be between the limits specified in the
        application config, see: min_user_setpoint_temperature_celsius
        and max_user_setpoint_temperature_celsius
    timings:
        If specified, the device will adopt these timings to set how
        long is spent at various stages of the current digitisation
        processes. The message includes a way of returning to default
        timings.  This value cannot be changed during acquisition
"""
StreamTemperatureRequest.__doc__ = """Attributes:
    period_seconds:
        How often temperature updates should be sent Defaults to a
        period of 1 second, if not specified, or set to 0
    acquisition_run_id:
        The acquisition id of the experiment.
    data_selection:
        The desired data selection.  The units for all values are
        `seconds since the start of the experiment`.
"""
ChangeDeviceSettingsResponse.__doc__ = """Attributes:
    real_sampling_frequency:
        The sampling frequency actually applied to the hardware, as
        close as possible to the requested rate.  Note: only returned
        if sampling rate was set as part of this call.
"""
GetPixelSettingsResponse.__doc__ = """Attributes:
    pixels:
        List of all requested pixel settings, in the order requested.
"""
TimingEnginePeriods.__doc__ = """ Timing-engine periods are specified in 5ns units. Some of the timing
mechanism can only achieve 10ns accuracy, so even numbers are
preferred.  Note: There is a timing feature in the ASIC that requires
the sum of the RST1 and DATA periods to be a multiple of 16

Attributes:
    RST1:
        Reset1 phase  Note: Commands are written to the ASIC during
        this period, to allow sufficient time to write the commands,
        this should never be less than 1.2us or 240.
    RST1_CDS1:
        Reset1 to CDS1 transition
    CDS1:
        CDS1 phase (Correlated Double Sampling) sample-point 1
    CDS1_DATA:
        CDS1 to DATA transition
    DATA:
        DATA transfer phase  NOTE: Setting this value has no effect,
        MinKNOW will choose a value for DATA itself to achieve the
        required frame-rate. Reading it will return the chosen DATA
        period.
    DATA_RST2:
        DATA transfer to Reset2 transition. MinKNOW may increase this
        value by small amounts so that when changing the DATA period,
        the sum of the RST1 and DATA periods is a multiple of 16 and
        the frame-rate and integration-period are maintained.
    RST2:
        Reset2
    RST2_CDS2:
        Reset2 to CDS2 transition
    CDS2:
        CDS2 Phase (sample-point 2)
    CDS2_SH:
        CDS2 to SH transition
    SH:
        SH phase (Sample and Hold)
    SH_RST1:
        SH to Reset1 transition
    use_default_values:
        If written true, other fields will be ignored and the hardware
        will use default timings. When read will return true if
        previously set true, it will not tell you if the timing
        periods you previously entered are the same as the default
        values.
"""
# @@protoc_insertion_point(module_scope)
