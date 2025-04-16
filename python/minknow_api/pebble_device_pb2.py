# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/pebble_device.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fminknow_api/pebble_device.proto\x12\x19minknow_api.pebble_device\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1dminknow_api/rpc_options.proto\"]\n\x10WaveformSettings\x12\x10\n\x08voltages\x18\x01 \x03(\x01\x12\x37\n\x11samples_per_entry\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\"\xed\x02\n\x13TimingEnginePeriods\x12J\n\x06states\x18\x03 \x03(\x0b\x32:.minknow_api.pebble_device.TimingEnginePeriods.StatesEntry\x12\x36\n\x12use_default_values\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x1ag\n\x0bTimingState\x12-\n\x08\x64uration\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12)\n\x04mask\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x1ai\n\x0bStatesEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12I\n\x05value\x18\x02 \x01(\x0b\x32:.minknow_api.pebble_device.TimingEnginePeriods.TimingState:\x02\x38\x01\"\xd2\x01\n\x18OverloadProtectionConfig\x12+\n\x07\x65nabled\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12-\n\x07periods\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12,\n\x07min_adc\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07max_adc\x18\x04 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\"\xad\n\n\x0e\x44\x65viceSettings\x12\x30\n\x0bsample_rate\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x37\n\x12temperature_target\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12\x36\n\x11reference_voltage\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x34\n\x0funblock_voltage\x18\x04 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12X\n\x13regen_current_range\x18\x05 \x01(\x0e\x32;.minknow_api.pebble_device.DeviceSettings.RegenCurrentRange\x12\x32\n\rregen_current\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x41\n\x1bregen_current_voltage_clamp\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x34\n\x0c\x62ias_voltage\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.DoubleValueH\x00\x12L\n\x15\x62ias_voltage_waveform\x18\t \x01(\x0b\x32+.minknow_api.pebble_device.WaveformSettingsH\x00\x12\x32\n\rint_capacitor\x18\n \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12W\n\x11lpf_time_constant\x18\x0b \x01(\x0e\x32<.minknow_api.pebble_device.DeviceSettings.LowPassFilterValue\x12?\n\x07timings\x18\x0c \x01(\x0b\x32..minknow_api.pebble_device.TimingEnginePeriods\x12\x35\n\x11power_save_active\x18\r \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12P\n\x13overload_protection\x18\x0e \x01(\x0b\x32\x33.minknow_api.pebble_device.OverloadProtectionConfig\"\xb5\x01\n\x11RegenCurrentRange\x12\x14\n\x10REGEN_RANGE_KEEP\x10\x00\x12 \n\x1cREGEN_RANGE_0_5nA_STEP_0_1nA\x10\x01\x12$\n REGEN_RANGE_0_667nA_STEP_0_133nA\x10\x02\x12 \n\x1cREGEN_RANGE_1_0nA_STEP_0_2nA\x10\x03\x12 \n\x1cREGEN_RANGE_2_0nA_STEP_0_4nA\x10\x04\"\xc5\x01\n\x12LowPassFilterValue\x12\x0c\n\x08LPF_KEEP\x10\x00\x12\x0c\n\x08LPF_0_us\x10\x01\x12\x13\n\x0fLPF_696kHz_2_us\x10\x02\x12\x13\n\x0fLPF_348kHz_4_us\x10\x03\x12\x13\n\x0fLPF_232kHz_7_us\x10\x04\x12\x13\n\x0fLPF_174kHz_9_us\x10\x05\x12\x14\n\x10LPF_139kHz_11_us\x10\x06\x12\x14\n\x10LPF_116kHz_13_us\x10\x07\x12\x13\n\x0fLPF_99kHz_16_us\x10\x08\x42\x16\n\x14\x62ias_voltage_setting\"`\n\x1b\x43hangeDeviceSettingsRequest\x12\x41\n\x08settings\x18\x01 \x01(\x0b\x32).minknow_api.pebble_device.DeviceSettingsB\x04\x90\xb5\x18\x01\"U\n\x1c\x43hangeDeviceSettingsResponse\x12\x35\n\x10real_sample_rate\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\"\x1a\n\x18GetDeviceSettingsRequest\"^\n\x19GetDeviceSettingsResponse\x12\x41\n\x08settings\x18\x01 \x01(\x0b\x32).minknow_api.pebble_device.DeviceSettingsB\x04\x90\xb5\x18\x01\"\xc0\x02\n\x0f\x43hannelSettings\x12\x45\n\x05input\x18\x01 \x01(\x0e\x32\x30.minknow_api.pebble_device.ChannelSettings.InputB\x04\x88\xb5\x18\x01\x12\x43\n\x04mode\x18\x02 \x01(\x0e\x32/.minknow_api.pebble_device.ChannelSettings.ModeB\x04\x88\xb5\x18\x01\"=\n\x05Input\x12\x11\n\rNO_CONNECTION\x10\x00\x12\n\n\x06WELL_1\x10\x01\x12\n\n\x06WELL_2\x10\x02\x12\t\n\x05OTHER\x10\x03\"b\n\x04Mode\x12\x0c\n\x08INACTIVE\x10\x00\x12\n\n\x06\x41\x43TIVE\x10\x01\x12\x0b\n\x07UNBLOCK\x10\x02\x12\x17\n\x13MEMBRANE_SIMULATION\x10\x03\x12\t\n\x05REGEN\x10\x04\x12\x0f\n\x0b\x43\x41LIBRATION\x10\x05\"\x99\x02\n\x1c\x43hangeChannelSettingsRequest\x12W\n\x08\x63hannels\x18\x01 \x03(\x0b\x32\x45.minknow_api.pebble_device.ChangeChannelSettingsRequest.ChannelsEntry\x12\x43\n\x0f\x63hannel_default\x18\x02 \x01(\x0b\x32*.minknow_api.pebble_device.ChannelSettings\x1a[\n\rChannelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\x39\n\x05value\x18\x02 \x01(\x0b\x32*.minknow_api.pebble_device.ChannelSettings:\x02\x38\x01\"\x1f\n\x1d\x43hangeChannelSettingsResponse\"3\n\x19GetChannelSettingsRequest\x12\x16\n\x08\x63hannels\x18\x01 \x03(\rB\x04\x88\xb5\x18\x01\"Z\n\x1aGetChannelSettingsResponse\x12<\n\x08\x63hannels\x18\x01 \x03(\x0b\x32*.minknow_api.pebble_device.ChannelSettings\"\xe0\x02\n\x14ResearchOnlySettings\x12V\n\x0b\x61sic_writes\x18\x05 \x03(\x0b\x32\x41.minknow_api.pebble_device.ResearchOnlySettings.AsicRegisterWrite\x12\x62\n\x11instrument_writes\x18\t \x03(\x0b\x32G.minknow_api.pebble_device.ResearchOnlySettings.InstrumentRegisterWrite\x1a\x42\n\x11\x41sicRegisterWrite\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\r\x12\r\n\x05\x64\x65lay\x18\x04 \x01(\r\x1aH\n\x17InstrumentRegisterWrite\x12\x0f\n\x07\x61\x64\x64ress\x18\x06 \x01(\r\x12\r\n\x05value\x18\x07 \x01(\r\x12\r\n\x05\x64\x65lay\x18\x08 \x01(\r\"l\n!ChangeResearchOnlySettingsRequest\x12G\n\x08settings\x18\x01 \x01(\x0b\x32/.minknow_api.pebble_device.ResearchOnlySettingsB\x04\x90\xb5\x18\x01\"$\n\"ChangeResearchOnlySettingsResponse2\xf5\x05\n\x13PebbleDeviceService\x12\x8e\x01\n\x16\x63hange_device_settings\x12\x36.minknow_api.pebble_device.ChangeDeviceSettingsRequest\x1a\x37.minknow_api.pebble_device.ChangeDeviceSettingsResponse\"\x03\x90\x02\x02\x12\x85\x01\n\x13get_device_settings\x12\x33.minknow_api.pebble_device.GetDeviceSettingsRequest\x1a\x34.minknow_api.pebble_device.GetDeviceSettingsResponse\"\x03\x90\x02\x01\x12\x91\x01\n\x17\x63hange_channel_settings\x12\x37.minknow_api.pebble_device.ChangeChannelSettingsRequest\x1a\x38.minknow_api.pebble_device.ChangeChannelSettingsResponse\"\x03\x90\x02\x02\x12\x88\x01\n\x14get_channel_settings\x12\x34.minknow_api.pebble_device.GetChannelSettingsRequest\x1a\x35.minknow_api.pebble_device.GetChannelSettingsResponse\"\x03\x90\x02\x01\x12\xa5\x01\n\x1d\x63hange_research_only_settings\x12<.minknow_api.pebble_device.ChangeResearchOnlySettingsRequest\x1a=.minknow_api.pebble_device.ChangeResearchOnlySettingsResponse\"\x07\x90\x02\x02\x98\xb5\x18\x01\x42`\n\x1c\x63om.nanoporetech.minknow_apiZ8github.com/nanoporetech/minknow_api/go/gen/pebble_device\xa2\x02\x05MKAPIb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.pebble_device_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.nanoporetech.minknow_apiZ8github.com/nanoporetech/minknow_api/go/gen/pebble_device\242\002\005MKAPI'
  _globals['_TIMINGENGINEPERIODS_STATESENTRY']._options = None
  _globals['_TIMINGENGINEPERIODS_STATESENTRY']._serialized_options = b'8\001'
  _globals['_CHANGEDEVICESETTINGSREQUEST'].fields_by_name['settings']._options = None
  _globals['_CHANGEDEVICESETTINGSREQUEST'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_GETDEVICESETTINGSRESPONSE'].fields_by_name['settings']._options = None
  _globals['_GETDEVICESETTINGSRESPONSE'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_CHANNELSETTINGS'].fields_by_name['input']._options = None
  _globals['_CHANNELSETTINGS'].fields_by_name['input']._serialized_options = b'\210\265\030\001'
  _globals['_CHANNELSETTINGS'].fields_by_name['mode']._options = None
  _globals['_CHANNELSETTINGS'].fields_by_name['mode']._serialized_options = b'\210\265\030\001'
  _globals['_CHANGECHANNELSETTINGSREQUEST_CHANNELSENTRY']._options = None
  _globals['_CHANGECHANNELSETTINGSREQUEST_CHANNELSENTRY']._serialized_options = b'8\001'
  _globals['_GETCHANNELSETTINGSREQUEST'].fields_by_name['channels']._options = None
  _globals['_GETCHANNELSETTINGSREQUEST'].fields_by_name['channels']._serialized_options = b'\210\265\030\001'
  _globals['_CHANGERESEARCHONLYSETTINGSREQUEST'].fields_by_name['settings']._options = None
  _globals['_CHANGERESEARCHONLYSETTINGSREQUEST'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['change_device_settings']._options = None
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['change_device_settings']._serialized_options = b'\220\002\002'
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['get_device_settings']._options = None
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['get_device_settings']._serialized_options = b'\220\002\001'
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['change_channel_settings']._options = None
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['change_channel_settings']._serialized_options = b'\220\002\002'
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['get_channel_settings']._options = None
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['get_channel_settings']._serialized_options = b'\220\002\001'
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['change_research_only_settings']._options = None
  _globals['_PEBBLEDEVICESERVICE'].methods_by_name['change_research_only_settings']._serialized_options = b'\220\002\002\230\265\030\001'
  _globals['_WAVEFORMSETTINGS']._serialized_start=125
  _globals['_WAVEFORMSETTINGS']._serialized_end=218
  _globals['_TIMINGENGINEPERIODS']._serialized_start=221
  _globals['_TIMINGENGINEPERIODS']._serialized_end=586
  _globals['_TIMINGENGINEPERIODS_TIMINGSTATE']._serialized_start=376
  _globals['_TIMINGENGINEPERIODS_TIMINGSTATE']._serialized_end=479
  _globals['_TIMINGENGINEPERIODS_STATESENTRY']._serialized_start=481
  _globals['_TIMINGENGINEPERIODS_STATESENTRY']._serialized_end=586
  _globals['_OVERLOADPROTECTIONCONFIG']._serialized_start=589
  _globals['_OVERLOADPROTECTIONCONFIG']._serialized_end=799
  _globals['_DEVICESETTINGS']._serialized_start=802
  _globals['_DEVICESETTINGS']._serialized_end=2127
  _globals['_DEVICESETTINGS_REGENCURRENTRANGE']._serialized_start=1722
  _globals['_DEVICESETTINGS_REGENCURRENTRANGE']._serialized_end=1903
  _globals['_DEVICESETTINGS_LOWPASSFILTERVALUE']._serialized_start=1906
  _globals['_DEVICESETTINGS_LOWPASSFILTERVALUE']._serialized_end=2103
  _globals['_CHANGEDEVICESETTINGSREQUEST']._serialized_start=2129
  _globals['_CHANGEDEVICESETTINGSREQUEST']._serialized_end=2225
  _globals['_CHANGEDEVICESETTINGSRESPONSE']._serialized_start=2227
  _globals['_CHANGEDEVICESETTINGSRESPONSE']._serialized_end=2312
  _globals['_GETDEVICESETTINGSREQUEST']._serialized_start=2314
  _globals['_GETDEVICESETTINGSREQUEST']._serialized_end=2340
  _globals['_GETDEVICESETTINGSRESPONSE']._serialized_start=2342
  _globals['_GETDEVICESETTINGSRESPONSE']._serialized_end=2436
  _globals['_CHANNELSETTINGS']._serialized_start=2439
  _globals['_CHANNELSETTINGS']._serialized_end=2759
  _globals['_CHANNELSETTINGS_INPUT']._serialized_start=2598
  _globals['_CHANNELSETTINGS_INPUT']._serialized_end=2659
  _globals['_CHANNELSETTINGS_MODE']._serialized_start=2661
  _globals['_CHANNELSETTINGS_MODE']._serialized_end=2759
  _globals['_CHANGECHANNELSETTINGSREQUEST']._serialized_start=2762
  _globals['_CHANGECHANNELSETTINGSREQUEST']._serialized_end=3043
  _globals['_CHANGECHANNELSETTINGSREQUEST_CHANNELSENTRY']._serialized_start=2952
  _globals['_CHANGECHANNELSETTINGSREQUEST_CHANNELSENTRY']._serialized_end=3043
  _globals['_CHANGECHANNELSETTINGSRESPONSE']._serialized_start=3045
  _globals['_CHANGECHANNELSETTINGSRESPONSE']._serialized_end=3076
  _globals['_GETCHANNELSETTINGSREQUEST']._serialized_start=3078
  _globals['_GETCHANNELSETTINGSREQUEST']._serialized_end=3129
  _globals['_GETCHANNELSETTINGSRESPONSE']._serialized_start=3131
  _globals['_GETCHANNELSETTINGSRESPONSE']._serialized_end=3221
  _globals['_RESEARCHONLYSETTINGS']._serialized_start=3224
  _globals['_RESEARCHONLYSETTINGS']._serialized_end=3576
  _globals['_RESEARCHONLYSETTINGS_ASICREGISTERWRITE']._serialized_start=3436
  _globals['_RESEARCHONLYSETTINGS_ASICREGISTERWRITE']._serialized_end=3502
  _globals['_RESEARCHONLYSETTINGS_INSTRUMENTREGISTERWRITE']._serialized_start=3504
  _globals['_RESEARCHONLYSETTINGS_INSTRUMENTREGISTERWRITE']._serialized_end=3576
  _globals['_CHANGERESEARCHONLYSETTINGSREQUEST']._serialized_start=3578
  _globals['_CHANGERESEARCHONLYSETTINGSREQUEST']._serialized_end=3686
  _globals['_CHANGERESEARCHONLYSETTINGSRESPONSE']._serialized_start=3688
  _globals['_CHANGERESEARCHONLYSETTINGSRESPONSE']._serialized_end=3724
  _globals['_PEBBLEDEVICESERVICE']._serialized_start=3727
  _globals['_PEBBLEDEVICESERVICE']._serialized_end=4484
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
        values are in the range [-Vref..Vref]mv INVALID_ARGUMENT will
        be returned if outside this range
    bias_voltage_waveform:
        The wavetable settings
    saturation_control_enabled:
        Enables saturation control on the device
    fast_calibration_enabled:
        Enable use of the fast calibration mode across the device
        DEPRECATED since 5.5. This will be removed in a future
        release.
    temperature_target:
        If the device is capable (see
        device.get_device_info().temperature_controllable) then this
        sets the target temperature to keep the flow-cell at.  This
        value must be between the limits specified in the application
        config, see: min_user_setpoint_temperature_celsius and
        max_user_setpoint_temperature_celsius INVALID_ARGUMENT will be
        returned if outside these limits
    timings:
        If specified, the device will adopt these timings to set how
        long is spent at various stages of the sampling process. The
        message includes a way of returning to default timings.
        FAILED_PRECONDITION will be returned if attempting to change
        during acquisition
    sample_rate:
        The number of measurements to take each second.  Possible
        values are between 1000, and 5000. If the value is outside of
        this range, it will be clamped within it  FAILED_PRECONDITION
        will be returned if attempting to change during acquisition
    reference_voltage:
        The reference voltage Vref  This value must be within the
        range of [700..1100](mV) and will be rounded down to the
        nearest 50mV. INVALID_ARGUMENT will be returned if outside
        these limits
    unblock_voltage:
        The unblock voltage to apply when a channel is unblocking.
        The acceptable input range depends on Vref The default Vref of
        900mV gives the unblock level a range between [-840..900]mV
        INVALID_ARGUMENT will be returned if outside of the limits set
        depending on Vref
    regen_current_range:
        Determines the range of regen current available for selection
        Range 0.5nA, step 0.1nA         Range 0.667nA, step 0.133nA
        Range 1.0nA, step 0.2nA (DEFAULT)         Range 2.0nA, step
        0.4nA INVALID_ARGUMENT will be returned if range option does
        not exist
    regen_current:
        Control the regeneration current used when regenerating
        well's.  The acceptable value is in pico Amps and depends on
        the specified regen_current_range option. Will round down to
        nearest acceptable step in value within the range.
        INVALID_ARGUMENT will be returned if outside the acceptable
        range
    regen_current_voltage_clamp:
        Voltage clamp for regeneration circuit (in millivolts)  The
        voltage in the regeneration circuit is clamped under this
        value, whilst applying the current specified in each quads
        settings.  This is a +/- voltage relative to Vref The polarity
        is determined by the regen current With a default Vref of
        900mV this gives the regen level a range of [0..840]mV
        INVALID_ARGUMENT will be returned if outside the acceptable
        range
    int_capacitor:
        Integration capacitor used for controlling the Gain This size
        of the capacitance used is based on the provided setting with
        a value of [0..31]  Refer to §2.3.1 of the OG2 ASIC
        documentation for both the nominal and measured capacitance
        that each setting produces.  This value is applied globally to
        all QUADs and therefore all channels  INVALID_ARGUMENT will be
        returned if outside the range of [0..31]
    lpf_time_constant:
        Low pass filter time constant This modifies the anti-alias
        resistor to produce a specific time constant for the low pass
        filter.
    power_save_active:
        Enable ASIC power save.  Setting to active will save power,
        but doing so will allow the ASIC to cool down, and it will
        take time to heat it up again along with performing a device
        reset.
    overload_protection:
        Settings for the hardware based saturation/overload protection
        (spike suppression)
"""
ChangeDeviceSettingsResponse.__doc__ = """Attributes:
    real_sampling_frequency:
        The sampling frequency actually applied to the hardware, as
        close as possible to the requested rate.  Note: only returned
        if sampling rate was set as part of this call.
    real_sample_rate:
        The sampling frequency actually applied to the hardware, as
        close as possible to the requested rate.  Note: only returned
        if sampling rate was set as part of this call.
"""
OverloadProtectionConfig.__doc__ = """Attributes:
    enabled:
        Set to enable or disable hardware based overload protection
        (saturation).
    periods:
        Threshold for the number of periods counted over threshold
        before disconnection. Valid value must be between [0..7]
        INVALID_ARGUMENT will be returned if not between these values
    min_adc:
        The minimum adc value that is not a saturation.  If this value
        is not specified, the previous value is kept. Valid value must
        be between [-2047..2047] INVALID_ARGUMENT will be returned if
        not between these values
    max_adc:
        The maximum adc value that is not a saturation.  If this value
        is not specified, the previous value is kept. Valid value must
        be between [-2047..2047] INVALID_ARGUMENT will be returned if
        not between these values
"""
GetChannelSettingsRequest.__doc__ = """Attributes:
    channels:
        The channels (one based) to return data for.
"""
ChannelSettings.__doc__ = """Attributes:
    input:
        The input to be digitised
    mode:
        The channel mode
"""
ResearchOnlySettings.AsicRegisterWrite.__doc__ = """Attributes:
    address:
        Register to write to, value between 0..254
    value:
        Value to write to the register, value between 0..255 Note: If
        value over two registers (high and low) then two separate
        writes required
    delay:
        Delay to add after this write, before the next
"""
GetChannelSettingsResponse.__doc__ = """Attributes:
    channels:
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
    states:
        Zero index based map [0-15] of up to 16 timing engine states
"""
ResearchOnlySettings.__doc__ = """Attributes:
    asic_writes:
        List of ASIC register writes to append Use at own risk as no
        validation is performed on the address or value of the
        individual writes.  The number of writes in single request
        limited to 128 due to internal MinKNOW limitations
        INVALID_ARGUMENT will be returned if greater than this limit
    instrument_writes:
        List of instrument register writes Use at own risk as no
        validation is performed on the address or value of the
        individual writes.  The number of writes in single request
        limited to 16 due to internal MinKNOW limitations
        INVALID_ARGUMENT will be returned if greater than this limit
"""
TimingEnginePeriods.TimingState.__doc__ = """Attributes:
    duration:
        The duration spent in each state is 1 more TEclock period than
        set in the associated register, so setting 1 results in a
        delay of 2 clock periods
    mask:
        The mask is built up of 7 user settable timing signals bit 0:
        INT_RESET bit 1: CDS_SAMPLE bit 2: CDS_RESET bit 3: DIG_ENABLE
        bit 4: CDS_SELECT bit 5: SYNC_MASTER bit 6: CML_ENABLE
"""
ChangeChannelSettingsRequest.__doc__ = """Attributes:
    channels:
        1 based map of up to 400 different channel settings
    channel_default:
        If supplied, contains settings applied to every channel before
        then applying any specific settings in the per channel
        settings.
"""
ResearchOnlySettings.InstrumentRegisterWrite.__doc__ = """Attributes:
    address:
        Register to write
    value:
        Value
    delay:
        Delay to add after this write, before the next
"""
WaveformSettings.__doc__ = """Attributes:
    voltages:
        The waveform data applied to the device (in millivolts)
        INVALID_ARGUMENT will be returned if the length of voltages is
        greater than 254 INVALID_ARGUMENT will be returned if one of
        the voltages is outside of [-Vref..Vref]mV
    frequency:
        The frequency of the applied waveform, in Hz.  Valid values
        are between 7.8125Hz and 500Hz.
    samples_per_entry:
        The number of samples each wavetable entry will be valid for
        Valid value must be between [1..31] INVALID_ARGUMENT will be
        returned if not between these values
"""
# @@protoc_insertion_point(module_scope)
