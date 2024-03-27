# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/minion_device.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fminknow_api/minion_device.proto\x12\x19minknow_api.minion_device\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1dminknow_api/rpc_options.proto\",\n\x10TemperatureRange\x12\x0b\n\x03min\x18\x05 \x01(\x02\x12\x0b\n\x03max\x18\x06 \x01(\x02\"\x89\x02\n\x1bSamplingFrequencyParameters\x12\x15\n\rclock_divider\x18\x01 \x01(\r\x12\x18\n\x10integration_time\x18\x02 \x01(\r\x12V\n\x0b\x63lock_speed\x18\x03 \x01(\x0e\x32\x41.minknow_api.minion_device.SamplingFrequencyParameters.ClockSpeed\"a\n\nClockSpeed\x12\x10\n\x0c\x43LOCK_128MHz\x10\x00\x12\x0f\n\x0b\x43LOCK_64MHz\x10\x01\x12\x0f\n\x0b\x43LOCK_32MHz\x10\x02\x12\x0f\n\x0b\x43LOCK_16MHz\x10\x03\x12\x0e\n\nCLOCK_8MHz\x10\x04\"\x88\x16\n\x14MinionDeviceSettings\x12\x31\n\x0c\x62ias_voltage\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x38\n\x12sampling_frequency\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12Z\n\x0e\x63hannel_config\x18\x03 \x03(\x0b\x32\x42.minknow_api.minion_device.MinionDeviceSettings.ChannelConfigEntry\x12>\n\x1a\x65nable_temperature_control\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12G\n\x12temperature_target\x18\x05 \x01(\x0b\x32+.minknow_api.minion_device.TemperatureRange\x12[\n\rint_capacitor\x18\x06 \x01(\x0e\x32\x44.minknow_api.minion_device.MinionDeviceSettings.IntegrationCapacitor\x12\x32\n\x0ctest_current\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x34\n\x0funblock_voltage\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x35\n\x11overcurrent_limit\x18\n \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x36\n\x10samples_to_reset\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x45\n\x07th_gain\x18\x0c \x01(\x0e\x32\x34.minknow_api.minion_device.MinionDeviceSettings.Gain\x12\x30\n\nsinc_delay\x18\r \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x33\n\x0eth_sample_time\x18\x0e \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12\x33\n\x0eint_reset_time\x18\x0f \x01(\x0b\x32\x1b.google.protobuf.FloatValue\x12S\n\x0fsinc_decimation\x18\x10 \x01(\x0e\x32:.minknow_api.minion_device.MinionDeviceSettings.Decimation\x12V\n\x0flow_pass_filter\x18\x11 \x01(\x0e\x32=.minknow_api.minion_device.MinionDeviceSettings.LowPassFilter\x12Z\n\x11non_overlap_clock\x18\x12 \x01(\x0e\x32?.minknow_api.minion_device.MinionDeviceSettings.NonOverlapClock\x12\x32\n\x0c\x62ias_current\x18\x13 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12<\n\x16\x63ompensation_capacitor\x18\x14 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12Y\n\x19sampling_frequency_params\x18\x15 \x01(\x0b\x32\x36.minknow_api.minion_device.SamplingFrequencyParameters\x12\x35\n\x11\x65nable_asic_power\x18\x16 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12K\n\tfan_speed\x18\x17 \x01(\x0e\x32\x38.minknow_api.minion_device.MinionDeviceSettings.FanSpeed\x12\x37\n\x13\x61llow_full_fan_stop\x18\x18 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x43\n\x1f\x65nable_soft_temperature_control\x18\x19 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12>\n\x1a\x65nable_bias_voltage_lookup\x18\x1a \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12!\n\x19\x62ias_voltage_lookup_table\x18\x1b \x03(\x05\x1as\n\x12\x43hannelConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12L\n\x05value\x18\x02 \x01(\x0e\x32=.minknow_api.minion_device.MinionDeviceSettings.ChannelConfig:\x02\x38\x01\"-\n\x04Gain\x12\r\n\tGAIN_KEEP\x10\x00\x12\n\n\x06GAIN_1\x10\x01\x12\n\n\x06GAIN_5\x10\x02\"G\n\nDecimation\x12\x13\n\x0f\x44\x45\x43IMATION_KEEP\x10\x00\x12\x11\n\rDECIMATION_32\x10\x01\x12\x11\n\rDECIMATION_64\x10\x02\"y\n\rLowPassFilter\x12\x0c\n\x08LPF_KEEP\x10\x00\x12\x0c\n\x08LPF_5kHz\x10\x01\x12\r\n\tLPF_10kHz\x10\x02\x12\r\n\tLPF_20kHz\x10\x03\x12\r\n\tLPF_40kHz\x10\x04\x12\r\n\tLPF_80kHz\x10\x05\x12\x10\n\x0cLPF_DISABLED\x10\x06\"G\n\x0fNonOverlapClock\x12\x0c\n\x08NOC_KEEP\x10\x00\x12\x12\n\x0eNOC_1_HS_CLOCK\x10\x01\x12\x12\n\x0eNOC_2_HS_CLOCK\x10\x02\"q\n\x14IntegrationCapacitor\x12\x0f\n\x0bINTCAP_KEEP\x10\x00\x12\x11\n\rINTCAP_62_5fF\x10\x01\x12\x10\n\x0cINTCAP_250fF\x10\x02\x12\x0e\n\nINTCAP_1pF\x10\x03\x12\x13\n\x0fINTCAP_1_1875pF\x10\x04\"f\n\x08\x46\x61nSpeed\x12\x11\n\rFANSPEED_KEEP\x10\x00\x12\x10\n\x0c\x46\x41NSPEED_OFF\x10\x01\x12\x10\n\x0c\x46\x41NSPEED_LOW\x10\x02\x12\x11\n\rFANSPEED_HIGH\x10\x03\x12\x10\n\x0c\x46\x41NSPEED_MAX\x10\x04\"\xbd\x03\n\rChannelConfig\x12\x17\n\x13\x43HANNEL_CONFIG_KEEP\x10\x00\x12\x10\n\x0c\x44ISCONNECTED\x10\x01\x12\x17\n\x13WELL_1_BIAS_VOLTAGE\x10\x02\x12\x17\n\x13WELL_2_BIAS_VOLTAGE\x10\x03\x12\x17\n\x13WELL_3_BIAS_VOLTAGE\x10\x04\x12\x17\n\x13WELL_4_BIAS_VOLTAGE\x10\x05\x12\x10\n\x0cTEST_CURRENT\x10\x06\x12\x1a\n\x16WELL_1_UNBLOCK_VOLTAGE\x10\x07\x12\x1a\n\x16WELL_2_UNBLOCK_VOLTAGE\x10\x08\x12\x1a\n\x16WELL_3_UNBLOCK_VOLTAGE\x10\t\x12\x1a\n\x16WELL_4_UNBLOCK_VOLTAGE\x10\n\x12\x1b\n\x17TEST_CURRENT_VIA_WELL_1\x10\x0b\x12\x1b\n\x17TEST_CURRENT_VIA_WELL_2\x10\x0c\x12\x1b\n\x17TEST_CURRENT_VIA_WELL_3\x10\r\x12\x1b\n\x17TEST_CURRENT_VIA_WELL_4\x10\x0e\x12\x1b\n\x17GROUND_THROUGH_RESISTOR\x10\x0f\x12\n\n\x06GROUND\x10\x10\"\xbf\x01\n\x15\x43hangeSettingsRequest\x12G\n\x08settings\x18\x01 \x01(\x0b\x32/.minknow_api.minion_device.MinionDeviceSettingsB\x04\x90\xb5\x18\x01\x12]\n\x16\x63hannel_config_default\x18\x02 \x01(\x0e\x32=.minknow_api.minion_device.MinionDeviceSettings.ChannelConfig\"\x18\n\x16\x43hangeSettingsResponse\"\x14\n\x12GetSettingsRequest\"^\n\x13GetSettingsResponse\x12G\n\x08settings\x18\x01 \x01(\x0b\x32/.minknow_api.minion_device.MinionDeviceSettingsB\x04\x90\xb5\x18\x01\"\x14\n\x12GetFanSpeedRequest\"\"\n\x13GetFanSpeedResponse\x12\x0b\n\x03rpm\x18\x01 \x01(\r2\xfb\x02\n\x13MinionDeviceService\x12{\n\x0f\x63hange_settings\x12\x30.minknow_api.minion_device.ChangeSettingsRequest\x1a\x31.minknow_api.minion_device.ChangeSettingsResponse\"\x03\x90\x02\x02\x12r\n\x0cget_settings\x12-.minknow_api.minion_device.GetSettingsRequest\x1a..minknow_api.minion_device.GetSettingsResponse\"\x03\x90\x02\x01\x12s\n\rget_fan_speed\x12-.minknow_api.minion_device.GetFanSpeedRequest\x1a..minknow_api.minion_device.GetFanSpeedResponse\"\x03\x90\x02\x01\x42&\n\x1c\x63om.nanoporetech.minknow_api\xa2\x02\x05MKAPIb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.minion_device_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.nanoporetech.minknow_api\242\002\005MKAPI'
  _globals['_MINIONDEVICESETTINGS_CHANNELCONFIGENTRY']._options = None
  _globals['_MINIONDEVICESETTINGS_CHANNELCONFIGENTRY']._serialized_options = b'8\001'
  _globals['_CHANGESETTINGSREQUEST'].fields_by_name['settings']._options = None
  _globals['_CHANGESETTINGSREQUEST'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_GETSETTINGSRESPONSE'].fields_by_name['settings']._options = None
  _globals['_GETSETTINGSRESPONSE'].fields_by_name['settings']._serialized_options = b'\220\265\030\001'
  _globals['_MINIONDEVICESERVICE'].methods_by_name['change_settings']._options = None
  _globals['_MINIONDEVICESERVICE'].methods_by_name['change_settings']._serialized_options = b'\220\002\002'
  _globals['_MINIONDEVICESERVICE'].methods_by_name['get_settings']._options = None
  _globals['_MINIONDEVICESERVICE'].methods_by_name['get_settings']._serialized_options = b'\220\002\001'
  _globals['_MINIONDEVICESERVICE'].methods_by_name['get_fan_speed']._options = None
  _globals['_MINIONDEVICESERVICE'].methods_by_name['get_fan_speed']._serialized_options = b'\220\002\001'
  _globals['_TEMPERATURERANGE']._serialized_start=125
  _globals['_TEMPERATURERANGE']._serialized_end=169
  _globals['_SAMPLINGFREQUENCYPARAMETERS']._serialized_start=172
  _globals['_SAMPLINGFREQUENCYPARAMETERS']._serialized_end=437
  _globals['_SAMPLINGFREQUENCYPARAMETERS_CLOCKSPEED']._serialized_start=340
  _globals['_SAMPLINGFREQUENCYPARAMETERS_CLOCKSPEED']._serialized_end=437
  _globals['_MINIONDEVICESETTINGS']._serialized_start=440
  _globals['_MINIONDEVICESETTINGS']._serialized_end=3264
  _globals['_MINIONDEVICESETTINGS_CHANNELCONFIGENTRY']._serialized_start=2166
  _globals['_MINIONDEVICESETTINGS_CHANNELCONFIGENTRY']._serialized_end=2281
  _globals['_MINIONDEVICESETTINGS_GAIN']._serialized_start=2283
  _globals['_MINIONDEVICESETTINGS_GAIN']._serialized_end=2328
  _globals['_MINIONDEVICESETTINGS_DECIMATION']._serialized_start=2330
  _globals['_MINIONDEVICESETTINGS_DECIMATION']._serialized_end=2401
  _globals['_MINIONDEVICESETTINGS_LOWPASSFILTER']._serialized_start=2403
  _globals['_MINIONDEVICESETTINGS_LOWPASSFILTER']._serialized_end=2524
  _globals['_MINIONDEVICESETTINGS_NONOVERLAPCLOCK']._serialized_start=2526
  _globals['_MINIONDEVICESETTINGS_NONOVERLAPCLOCK']._serialized_end=2597
  _globals['_MINIONDEVICESETTINGS_INTEGRATIONCAPACITOR']._serialized_start=2599
  _globals['_MINIONDEVICESETTINGS_INTEGRATIONCAPACITOR']._serialized_end=2712
  _globals['_MINIONDEVICESETTINGS_FANSPEED']._serialized_start=2714
  _globals['_MINIONDEVICESETTINGS_FANSPEED']._serialized_end=2816
  _globals['_MINIONDEVICESETTINGS_CHANNELCONFIG']._serialized_start=2819
  _globals['_MINIONDEVICESETTINGS_CHANNELCONFIG']._serialized_end=3264
  _globals['_CHANGESETTINGSREQUEST']._serialized_start=3267
  _globals['_CHANGESETTINGSREQUEST']._serialized_end=3458
  _globals['_CHANGESETTINGSRESPONSE']._serialized_start=3460
  _globals['_CHANGESETTINGSRESPONSE']._serialized_end=3484
  _globals['_GETSETTINGSREQUEST']._serialized_start=3486
  _globals['_GETSETTINGSREQUEST']._serialized_end=3506
  _globals['_GETSETTINGSRESPONSE']._serialized_start=3508
  _globals['_GETSETTINGSRESPONSE']._serialized_end=3602
  _globals['_GETFANSPEEDREQUEST']._serialized_start=3604
  _globals['_GETFANSPEEDREQUEST']._serialized_end=3624
  _globals['_GETFANSPEEDRESPONSE']._serialized_start=3626
  _globals['_GETFANSPEEDRESPONSE']._serialized_end=3660
  _globals['_MINIONDEVICESERVICE']._serialized_start=3663
  _globals['_MINIONDEVICESERVICE']._serialized_end=4042
GetSettingsResponse.__doc__ = """Response for MinionDeviceService.get_settings

Attributes:
    settings:
        MinION device settings
"""
GetSettingsRequest.__doc__ = """Request for MinionDeviceService.get_settings"""
MinionDeviceSettings.__doc__ = """Describes the MinION device settings.  Both unset structures and
*_KEEP values in enums indicate "no change". When changing settings,
these are the default values.

Attributes:
    bias_voltage:
        The voltage potential to be applied across the wells (in
        millivolts).  This voltage drives the process of forcing
        molecules through the nanopores.  The range of possible values
        is -1275 to 1275 inclusive, in 5mv steps.  When setting this
        value, if the provided value is not a multiple of 5, an error
        will be returned.
    sampling_frequency:
        The number of measurements to take each second.  This value is
        derived from the sampling_frequency_params values, and so not
        all values are possible.  When changing the sampling
        frequency, either this value can be provided, or the values in
        sampling_frequency_params can be provided (attempting to
        provide both will cause the RPC to fail with an error). If
        this value is provided, the nearest admissible value will be
        used (eg: if 3000Hz is requested, 3012Hz will be applied).
        This value cannot be changed during acquisition, and changing
        it will invalidate the current calibration.  Note that setting
        the sampling frequency to over 20000Hz (20KHz) will force the
        sinc_decimation value to 32.
    channel_config:
        The per-channel configuration.  Each channel can be set to one
        of 16 states, which specifies the set of electrical
        connections to make. This includes which, if any, of the four
        wells linked to the channel to use.  Note that channel names
        start at 1. If you pass 0 as a key in this map, it will result
        in an error.  When changing the device settings, any omitted
        channels (or channels set to CHANNEL_CONFIG_KEEP) will use the
        default value set in
        ChangeSettingsRequest.channel_config_default.
    enable_temperature_control:
        Whether to enable temperature control.  If true, the device
        will attempt to keep its temperature within the bounds given
        by ``temperature_lower_bound`` and
        ``temperature_upper_bound``. If false, it will not do any
        temperature control.  Default is enabled.  It is recommended
        that this is enabled. If temperature control is disabled, the
        device may overheat. In this case, it will turn itself off,
        and must be unplugged and allowed to cool before using again.
    temperature_target:
        The target temperature range for the device.  If
        enable_temperature_control is set to true, the device will
        attempt to keep its temperature between the min and max values
        provided here.  Default is defined in application config.
        Note that if soft temperature control is enabled, only the
        ``max`` temperature is used.
    int_capacitor:
        Integration capacitor value.  This affects the sensitivity of
        the measurement: lower capacitor values give more sensitive
        measurements (but also more noise). Changing this will
        invalidate the current calibration.  Default is 250.0
    test_current:
        The level of current used in the TEST_CURRENT channel
        configuration.  This can be set in the range 0pA to 350pA in
        50pA intervals, default is 100.0
    unblock_voltage:
        The unblock voltage potential (in millivolts).  When a channel
        is set to one of the UNBLOCK configurations, the specified
        well will have this voltage applied across it, rather than
        bias_voltage.  The range of possible values is -372 to 0
        inclusive, in 12mv steps,  default is 0.  When setting this
        value, if the provided value is not a multiple of 12, an error
        will be returned.
    overcurrent_limit:
        Whether to enable detection of excessive current.  The ADC
        output of a channel that trips the over-current depends on
        what track and hold gain has been set to.  Default is enabled.
    samples_to_reset:
        The the number of integrator resets per sample.  The range of
        possible values is 0 to 255, default is 1
    th_gain:
        Track/Hold gain.  Default is 5.0
    sinc_delay:
        Delay from 2:1 mux switch to sinc filter enable in ADC clocks.
        The range of possible values is 0 to 15, default is 4.0
    th_sample_time:
        Track/Hold sample time in microseconds (us).  The range of
        possible values is 0.5us to 7.5us in steps of 0.5us, default
        is 0.5.
    int_reset_time:
        Integrator reset time in microseconds (us).  This value forms
        a part of the integration time specified in the sampling
        frequency parameters.  The range of possible values is 1us to
        16us in steps of 0.5us, default is 3.5.
    sinc_decimation:
        Decimation.  If the integration time is set to less than 50us
        (or, equivalently, the sampling frequency is set to greater
        than 20KHz), this value will be forced to 32.  Default is
        64.0.
    low_pass_filter:
        Low pass filter that should be applied.  Default is 40kHz
    non_overlap_clock:
        Amount of non-overlap for non-overlapping clocks.  Default is
        NOC_1_HS_CLOCK.
    bias_current:
        Bias current.  This can be set in the range 0 to 15 in
        intervals of 5, default is 5.
    compensation_capacitor:
        Compensation capacitor value.  This can be set in the range 0
        to 49 in intervals of 7, default is 14.
    sampling_frequency_params:
        Sampling frequency parameters.  The sampling_frequency value
        is calculated from these settings.  When changing the sampling
        frequency, either the values here can be provided, or a
        sampling_frequency can be provided (attempting to provide both
        will cause the RPC to fail with an error).  WARNING: This
        should not be used in a change_settings call without
        consulting the hardware documentation for permissible
        combinations of values. MinKNOW will only do minimal checking
        of the values given here; if you use invalid combinations of
        settings, the device will be unable to acquire data, and may
        even be permanently damaged.  This value cannot be changed
        during acquisition.
    enable_asic_power:
        Enable ASIC analogue supply voltage.  This must be enabled to
        heat and acquire data from the ASIC. It can be disabled to
        save power, but doing so will allow the ASIC to cool down, and
        it will take time to heat it up again.  Default is true.
    fan_speed:
        The speed of the fan when temperature control is off.  If
        ``enable_temperature_control`` is false, this setting will be
        ignored, as the temperature control routines on the device
        will control the speed of the fan.  Note that this setting
        does not apply to GridIONs.  Default is FANSPEED_MAX.
    allow_full_fan_stop:
        Whether to allow the fan to completely stop.  Allowing the fan
        to stop causes issues on some old MinION models.  Note that
        this setting does not apply to GridIONs.  Default is false.
    enable_soft_temperature_control:
        Enable soft temperature control.  "Soft" temperature control
        is a more intelligent temperature control algorithm. It works
        on a single target temperature, and dynamically adjusts the
        fan speed to reach that temperature quickly, and then
        maintains the target temperature with high precision.  If this
        is disabled, "hard" temperature control is used instead. This
        is a naive algorithm that simply turns the fan up when
        dropping below the minimum temperature and turns it down when
        going above the maximum temperature.  If
        ``enable_temperature_control`` is false, this setting is
        ignored.  It is recommended that this is enabled.  Default is
        true.
    enable_bias_voltage_lookup:
        Use the bias voltage lookup table to set the bias voltage.  If
        this is enabled, the bias voltage will be updated every
        millisecond with each entry in the bias voltage lookup table
        (see ``bias_voltage_lookup_table``) in turn, cycling through
        when the end of the table is reached.  This has the effect of
        producing a bias voltage waveform.  When enabling this, it is
        required to either provide the lookup table entries at the
        same time, or to have already provided them in a previous
        call.  Default is false.
    bias_voltage_lookup_table:
        The bias voltage lookup table.  If no entries are provided,
        the existing lookup table (if any) is preserved.  See
        ``enable_bias_voltage_lookup``.  Up to 75 values can be
        provided. The values have the same constraints as
        ``bias_voltage``.
"""
ChangeSettingsRequest.__doc__ = """Attributes:
    settings:
        MinION device settings
    channel_config_default:
        The default channel configuration.  This provides the default
        configuration to apply to any channels not listed in
        settings.channel_config.
"""
TemperatureRange.__doc__ = """Temperature range.

Attributes:
    min:
        The minimum temperature in degrees Celsius.  If temperature
        control is enabled, the device will attempt to keep its
        temperature at or above this value.  Must be less than or
        equal to max.  When soft temperature control is enabled, this
        value is not used.
    max:
        The maximum temperature in degrees Celsius.  If temperature
        control is enabled, the device will attempt to keep its
        temperature at or below this value.  Must be less than or
        equal to min.  When soft temperature control is enabled, this
        is used as the target temperature, and ``min`` is not used.
"""
SamplingFrequencyParameters.__doc__ = """These values control the sampling frequency.

Attributes:
    clock_divider:
        Clock divider.  Values over 31 cannot be set.
    integration_time:
        The time spent sampling a data point, in microseconds.  Must
        be between 30 and 1023 (inclusive).  Note that setting the
        integration_time to less than 50 will force the
        sinc_decimation value to 32.
    clock_speed:
        The speed of the high-speed clock.
"""
# @@protoc_insertion_point(module_scope)
