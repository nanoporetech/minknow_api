# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow_api/instance.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from minknow_api import acquisition_pb2 as minknow__api_dot_acquisition__pb2
from minknow_api import device_pb2 as minknow__api_dot_device__pb2
from minknow_api import protocol_pb2 as minknow__api_dot_protocol__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aminknow_api/instance.proto\x12\x14minknow_api.instance\x1a\x1dminknow_api/acquisition.proto\x1a\x18minknow_api/device.proto\x1a\x1aminknow_api/protocol.proto\"\x17\n\x15GetVersionInfoRequest\"\xa6\x05\n\x16GetVersionInfoResponse\x12L\n\x07minknow\x18\x01 \x01(\x0b\x32;.minknow_api.instance.GetVersionInfoResponse.MinknowVersion\x12\r\n\x05\x62ream\x18\x02 \x01(\t\x12\x1c\n\x14\x64istribution_version\x18\x03 \x01(\t\x12\\\n\x13\x64istribution_status\x18\x04 \x01(\x0e\x32?.minknow_api.instance.GetVersionInfoResponse.DistributionStatus\x12\x1e\n\x16protocol_configuration\x18\x05 \x01(\t\x12X\n\x11installation_type\x18\x06 \x01(\x0e\x32=.minknow_api.instance.GetVersionInfoResponse.InstallationType\x12 \n\x18\x62\x61secaller_build_version\x18\t \x01(\t\x12$\n\x1c\x62\x61secaller_connected_version\x18\n \x01(\t\x1aK\n\x0eMinknowVersion\x12\r\n\x05major\x18\x01 \x01(\x05\x12\r\n\x05minor\x18\x02 \x01(\x05\x12\r\n\x05patch\x18\x03 \x01(\x05\x12\x0c\n\x04\x66ull\x18\x04 \x01(\t\"I\n\x12\x44istributionStatus\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06STABLE\x10\x01\x12\x0c\n\x08UNSTABLE\x10\x02\x12\x0c\n\x08MODIFIED\x10\x03\"M\n\x10InstallationType\x12\x07\n\x03ONT\x10\x00\x12\x06\n\x02NC\x10\x01\x12\x08\n\x04PROD\x10\x02\x12\r\n\tQ_RELEASE\x10\x03\x12\x0f\n\x0bOND_RELEASE\x10\x04J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\t\"\x1d\n\x1bGetOutputDirectoriesRequest\"?\n\x11OutputDirectories\x12\x0e\n\x06output\x18\x01 \x01(\t\x12\x0b\n\x03log\x18\x02 \x01(\t\x12\r\n\x05reads\x18\x03 \x01(\t\"$\n\"GetDefaultOutputDirectoriesRequest\")\n\x19SetOutputDirectoryRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\"\x1c\n\x1aSetOutputDirectoryResponse\"(\n\x18SetReadsDirectoryRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\"\x1b\n\x19SetReadsDirectoryResponse\"\xfa\x01\n\x17\x46ilesystemDiskSpaceInfo\x12\x15\n\rfilesystem_id\x18\x01 \x01(\t\x12\x17\n\x0f\x62ytes_available\x18\x02 \x01(\x04\x12\x16\n\x0e\x62ytes_capacity\x18\x03 \x01(\x04\x12\x0c\n\x04what\x18\x04 \x03(\t\x12\x1d\n\x15\x62ytes_to_stop_cleanly\x18\x05 \x01(\x04\x12\x1f\n\x17\x62ytes_when_alert_issued\x18\x06 \x01(\x04\x12\x17\n\x0frecommend_alert\x18\x07 \x01(\x08\x12\x16\n\x0erecommend_stop\x18\x08 \x01(\x08\x12\x18\n\x10\x62ytes_per_second\x18\t \x01(\x03\"\x19\n\x17GetDiskSpaceInfoRequest\",\n\x1aStreamDiskSpaceInfoRequest\x12\x0e\n\x06period\x18\x01 \x01(\r\"m\n\x18GetDiskSpaceInfoResponse\x12Q\n\x1a\x66ilesystem_disk_space_info\x18\x01 \x03(\x0b\x32-.minknow_api.instance.FilesystemDiskSpaceInfo\"\x15\n\x13GetMachineIdRequest\"*\n\x14GetMachineIdResponse\x12\x12\n\nmachine_id\x18\x01 \x01(\t\"\x1f\n\x1dStreamInstanceActivityRequest\"\x9a\x01\n\nDeviceInfo\x12L\n\x0c\x64\x65vice_state\x18\x01 \x01(\x0e\x32\x36.minknow_api.device.GetDeviceStateResponse.DeviceState\x12>\n\x0b\x64\x65vice_info\x18\x02 \x01(\x0b\x32).minknow_api.device.GetDeviceInfoResponse\",\n\rBasecallSpeed\x12\x1b\n\x13mean_basecall_speed\x18\x01 \x01(\x02\")\n\x03N50\x12\x0b\n\x03n50\x18\x01 \x01(\x02\x12\x15\n\restimated_n50\x18\x02 \x01(\x02\"\xaf\x06\n\x1eStreamInstanceActivityResponse\x12\x37\n\x0b\x64\x65vice_info\x18\x01 \x01(\x0b\x32 .minknow_api.instance.DeviceInfoH\x00\x12\x45\n\x0e\x66low_cell_info\x18\x02 \x01(\x0b\x32+.minknow_api.device.GetFlowCellInfoResponseH\x00\x12\x42\n\x11protocol_run_info\x18\x03 \x01(\x0b\x32%.minknow_api.protocol.ProtocolRunInfoH\x00\x12K\n\x14\x61\x63quisition_run_info\x18\x04 \x01(\x0b\x32+.minknow_api.acquisition.AcquisitionRunInfoH\x00\x12_\n\x10\x66low_cell_health\x18\x05 \x01(\x0b\x32\x43.minknow_api.instance.StreamInstanceActivityResponse.FlowCellHealthH\x00\x12I\n\ryield_summary\x18\x06 \x01(\x0b\x32\x30.minknow_api.acquisition.AcquisitionYieldSummaryH\x00\x12=\n\x0e\x62\x61secall_speed\x18\x07 \x01(\x0b\x32#.minknow_api.instance.BasecallSpeedH\x00\x12(\n\x03n50\x18\x08 \x01(\x0b\x32\x19.minknow_api.instance.N50H\x00\x1a\xd6\x01\n\x0e\x46lowCellHealth\x12\x83\x01\n\x19\x63hannel_state_percentages\x18\x01 \x03(\x0b\x32`.minknow_api.instance.StreamInstanceActivityResponse.FlowCellHealth.ChannelStatePercentagesEntry\x1a>\n\x1c\x43hannelStatePercentagesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\x42\x0e\n\x0cstream_value2\x8a\t\n\x0fInstanceService\x12r\n\x10get_version_info\x12+.minknow_api.instance.GetVersionInfoRequest\x1a,.minknow_api.instance.GetVersionInfoResponse\"\x03\x90\x02\x01\x12y\n\x16get_output_directories\x12\x31.minknow_api.instance.GetOutputDirectoriesRequest\x1a\'.minknow_api.instance.OutputDirectories\"\x03\x90\x02\x01\x12\x88\x01\n\x1eget_default_output_directories\x12\x38.minknow_api.instance.GetDefaultOutputDirectoriesRequest\x1a\'.minknow_api.instance.OutputDirectories\"\x03\x90\x02\x01\x12~\n\x14set_output_directory\x12/.minknow_api.instance.SetOutputDirectoryRequest\x1a\x30.minknow_api.instance.SetOutputDirectoryResponse\"\x03\x90\x02\x02\x12{\n\x13set_reads_directory\x12..minknow_api.instance.SetReadsDirectoryRequest\x1a/.minknow_api.instance.SetReadsDirectoryResponse\"\x03\x90\x02\x02\x12|\n\x13get_disk_space_info\x12-.minknow_api.instance.GetDiskSpaceInfoRequest\x1a..minknow_api.instance.GetDiskSpaceInfoResponse\"\x06\x88\x02\x01\x90\x02\x01\x12\x84\x01\n\x16stream_disk_space_info\x12\x30.minknow_api.instance.StreamDiskSpaceInfoRequest\x1a..minknow_api.instance.GetDiskSpaceInfoResponse\"\x06\x88\x02\x01\x90\x02\x01\x30\x01\x12l\n\x0eget_machine_id\x12).minknow_api.instance.GetMachineIdRequest\x1a*.minknow_api.instance.GetMachineIdResponse\"\x03\x90\x02\x01\x12\x8c\x01\n\x18stream_instance_activity\x12\x33.minknow_api.instance.StreamInstanceActivityRequest\x1a\x34.minknow_api.instance.StreamInstanceActivityResponse\"\x03\x90\x02\x01\x30\x01\x42[\n\x1c\x63om.nanoporetech.minknow_apiZ3github.com/nanoporetech/minknow_api/go/gen/instance\xa2\x02\x05MKAPIb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'minknow_api.instance_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.nanoporetech.minknow_apiZ3github.com/nanoporetech/minknow_api/go/gen/instance\242\002\005MKAPI'
  _globals['_STREAMINSTANCEACTIVITYRESPONSE_FLOWCELLHEALTH_CHANNELSTATEPERCENTAGESENTRY']._options = None
  _globals['_STREAMINSTANCEACTIVITYRESPONSE_FLOWCELLHEALTH_CHANNELSTATEPERCENTAGESENTRY']._serialized_options = b'8\001'
  _globals['_INSTANCESERVICE'].methods_by_name['get_version_info']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['get_version_info']._serialized_options = b'\220\002\001'
  _globals['_INSTANCESERVICE'].methods_by_name['get_output_directories']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['get_output_directories']._serialized_options = b'\220\002\001'
  _globals['_INSTANCESERVICE'].methods_by_name['get_default_output_directories']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['get_default_output_directories']._serialized_options = b'\220\002\001'
  _globals['_INSTANCESERVICE'].methods_by_name['set_output_directory']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['set_output_directory']._serialized_options = b'\220\002\002'
  _globals['_INSTANCESERVICE'].methods_by_name['set_reads_directory']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['set_reads_directory']._serialized_options = b'\220\002\002'
  _globals['_INSTANCESERVICE'].methods_by_name['get_disk_space_info']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['get_disk_space_info']._serialized_options = b'\210\002\001\220\002\001'
  _globals['_INSTANCESERVICE'].methods_by_name['stream_disk_space_info']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['stream_disk_space_info']._serialized_options = b'\210\002\001\220\002\001'
  _globals['_INSTANCESERVICE'].methods_by_name['get_machine_id']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['get_machine_id']._serialized_options = b'\220\002\001'
  _globals['_INSTANCESERVICE'].methods_by_name['stream_instance_activity']._options = None
  _globals['_INSTANCESERVICE'].methods_by_name['stream_instance_activity']._serialized_options = b'\220\002\001'
  _globals['_GETVERSIONINFOREQUEST']._serialized_start=137
  _globals['_GETVERSIONINFOREQUEST']._serialized_end=160
  _globals['_GETVERSIONINFORESPONSE']._serialized_start=163
  _globals['_GETVERSIONINFORESPONSE']._serialized_end=841
  _globals['_GETVERSIONINFORESPONSE_MINKNOWVERSION']._serialized_start=600
  _globals['_GETVERSIONINFORESPONSE_MINKNOWVERSION']._serialized_end=675
  _globals['_GETVERSIONINFORESPONSE_DISTRIBUTIONSTATUS']._serialized_start=677
  _globals['_GETVERSIONINFORESPONSE_DISTRIBUTIONSTATUS']._serialized_end=750
  _globals['_GETVERSIONINFORESPONSE_INSTALLATIONTYPE']._serialized_start=752
  _globals['_GETVERSIONINFORESPONSE_INSTALLATIONTYPE']._serialized_end=829
  _globals['_GETOUTPUTDIRECTORIESREQUEST']._serialized_start=843
  _globals['_GETOUTPUTDIRECTORIESREQUEST']._serialized_end=872
  _globals['_OUTPUTDIRECTORIES']._serialized_start=874
  _globals['_OUTPUTDIRECTORIES']._serialized_end=937
  _globals['_GETDEFAULTOUTPUTDIRECTORIESREQUEST']._serialized_start=939
  _globals['_GETDEFAULTOUTPUTDIRECTORIESREQUEST']._serialized_end=975
  _globals['_SETOUTPUTDIRECTORYREQUEST']._serialized_start=977
  _globals['_SETOUTPUTDIRECTORYREQUEST']._serialized_end=1018
  _globals['_SETOUTPUTDIRECTORYRESPONSE']._serialized_start=1020
  _globals['_SETOUTPUTDIRECTORYRESPONSE']._serialized_end=1048
  _globals['_SETREADSDIRECTORYREQUEST']._serialized_start=1050
  _globals['_SETREADSDIRECTORYREQUEST']._serialized_end=1090
  _globals['_SETREADSDIRECTORYRESPONSE']._serialized_start=1092
  _globals['_SETREADSDIRECTORYRESPONSE']._serialized_end=1119
  _globals['_FILESYSTEMDISKSPACEINFO']._serialized_start=1122
  _globals['_FILESYSTEMDISKSPACEINFO']._serialized_end=1372
  _globals['_GETDISKSPACEINFOREQUEST']._serialized_start=1374
  _globals['_GETDISKSPACEINFOREQUEST']._serialized_end=1399
  _globals['_STREAMDISKSPACEINFOREQUEST']._serialized_start=1401
  _globals['_STREAMDISKSPACEINFOREQUEST']._serialized_end=1445
  _globals['_GETDISKSPACEINFORESPONSE']._serialized_start=1447
  _globals['_GETDISKSPACEINFORESPONSE']._serialized_end=1556
  _globals['_GETMACHINEIDREQUEST']._serialized_start=1558
  _globals['_GETMACHINEIDREQUEST']._serialized_end=1579
  _globals['_GETMACHINEIDRESPONSE']._serialized_start=1581
  _globals['_GETMACHINEIDRESPONSE']._serialized_end=1623
  _globals['_STREAMINSTANCEACTIVITYREQUEST']._serialized_start=1625
  _globals['_STREAMINSTANCEACTIVITYREQUEST']._serialized_end=1656
  _globals['_DEVICEINFO']._serialized_start=1659
  _globals['_DEVICEINFO']._serialized_end=1813
  _globals['_BASECALLSPEED']._serialized_start=1815
  _globals['_BASECALLSPEED']._serialized_end=1859
  _globals['_N50']._serialized_start=1861
  _globals['_N50']._serialized_end=1902
  _globals['_STREAMINSTANCEACTIVITYRESPONSE']._serialized_start=1905
  _globals['_STREAMINSTANCEACTIVITYRESPONSE']._serialized_end=2720
  _globals['_STREAMINSTANCEACTIVITYRESPONSE_FLOWCELLHEALTH']._serialized_start=2490
  _globals['_STREAMINSTANCEACTIVITYRESPONSE_FLOWCELLHEALTH']._serialized_end=2704
  _globals['_STREAMINSTANCEACTIVITYRESPONSE_FLOWCELLHEALTH_CHANNELSTATEPERCENTAGESENTRY']._serialized_start=2642
  _globals['_STREAMINSTANCEACTIVITYRESPONSE_FLOWCELLHEALTH_CHANNELSTATEPERCENTAGESENTRY']._serialized_end=2704
  _globals['_INSTANCESERVICE']._serialized_start=2723
  _globals['_INSTANCESERVICE']._serialized_end=3885
GetVersionInfoResponse.__doc__ = """Version of the basecaller MinKNOW is running with.  Since 5.0 This
field has been updated since 6.0  guppy_connected_version

Attributes:
    minknow:
        What minknow version is installed. Split into major, minor and
        patch versions Also includes the full version as a string,
        which contain the major, minor and patch numbers as well as if
        the version is pre-release version (~pre), whether it is a
        release candidate (~rc#) or whether it is a variant version
        (i.e. for conferences) (-variant). For non-release builds it
        also includes the hash of the commit it is based on, and
        whether the working copy is different from that has (-dirty)
    bream:
        The version of Bream that is installed.  An invalid
        installation will cause this to return "0.0.0".  Prior to 5.0,
        this field was called "protocols".  Since 5.0
    distribution_version:
        Describes the distribution that this MinKNOW installation is
        part of, usually this will be the Metapackage version
        number/identity, this will be "unknown" if the distribution-
        version hasn't been set. This information is also communicated
        in the Manager's DaemonMessage in daemon.proto
    distribution_status:
        Indicates if the MinKNOW distribution including components
        such as Bream are stable, unstable or have been modified.
    protocol_configuration:
        The version of the protocol configuration files that is
        installed.  An invalid installation will cause this to return
        "0.0.0".  Prior to 5.0, this field was called "configuration".
        Since 5.0
    installation_type:
        The installation type of MinKNOW.  The installation type may
        affect the available features, or the update process.  Since
        4.1
"""
StreamInstanceActivityResponse.__doc__ = """Attributes:
    device_info:
        Information about whether the device is connected or not, and
        if it is, gives information about the connected device
    flow_cell_info:
        Information about the currently connected flow cell  Note: if
        no flow cell is connected this [flow_cell_info.has_flow_cell]
        will be false
    protocol_run_info:
        Information about the in progress protocol.  Note if no
        protocol is active this message will not be present.
    acquisition_run_info:
        Information about the current acquisition run  Note if no
        acquisition is active the message will not be present.
    flow_cell_health:
        Information about the health of the flow cell within the
        current run  Note: only available if a run is in progress
    yield_summary:
        Acquisition yield information. Describes information such as
        number of reads, what number of those reads have passed or
        failed basecalling etc. Rate limited to 1 second per update
    basecall_speed:
        Basecall speed information Note: only available if an
        acquisition with basecalling enabled is in progress
    n50:
        n50 information  Contains the n50 value, measured in
        basecalled bases and estimated bases  Note: basecalled bases
        only available if an acquisition with basecalling enabled is
        in progress
"""
N50.__doc__ = """Attributes:
    n50:
        N50 data, in basecalled bases  This value is only streamed for
        acquisitions where basecalling is enabled.  The latest value
        is sent once per minute
    estimated_n50:
        N50 data, in estimated bases  The latest value is sent once
        per minute
"""
GetMachineIdResponse.__doc__ = """Attributes:
    machine_id:
        The machine_id MinKNOW uses for this host.
"""
DeviceInfo.__doc__ = """Attributes:
    device_state:
        The current state of the device
    device_info:
        Information about the connected device (or no content if
        disconnected see: device_state)
"""
FilesystemDiskSpaceInfo.__doc__ = """disk-usage information for one file-system

Attributes:
    filesystem_id:
        The name of the file-system
    bytes_available:
        How much space is left on the file-system
    bytes_capacity:
        The total capacity of the file-system when empty.
    what:
        A list of what MinKNOW stores on this file-system, eg: reads,
        logs, intermediate-files
    bytes_to_stop_cleanly:
        MinKNOW needs this much space to stop experiments. If
        bytes_available goes below this number, data could be lost!
    bytes_when_alert_issued:
        The amount of space left on the file-system when
        recommend_alert was set true.
    recommend_alert:
        MinKNOW recommends that you alert someone about the disk-usage
    recommend_stop:
        MinKNOW recommends that you stop experiments due to disk-usage
        concerns
    bytes_per_second:
        Rate of change in bytes_available (per second) +'ve numbers
        indicate that bytes_available is decreasing and space is being
        used A value of 0 can indicate that this has not applicable or
        not available.
    file_types_stored:
        A list of what types of file MinKNOW stores on this file-
        system, eg: reads, logs, intermediate-files, etc.
"""
StreamInstanceActivityResponse.FlowCellHealth.__doc__ = """Attributes:
    channel_state_percentages:
        Map between channel state name and a percentage of how much
        time that state has been active with respect to all other
        channel states  This is over one minute of time this is
        calculated over
"""
OutputDirectories.__doc__ = """Attributes:
    output:
        The base output directory. Anything that is output to files is
        branched from this directory.
    log:
        Directory where logs will be stored.
    reads:
        Base directory where reads will be outputted.
"""
StreamDiskSpaceInfoRequest.__doc__ = """Attributes:
    period:
        Disk space information will be streamed with this value
        determining the period in seconds between updates. A period of
        0 is invalid
"""
BasecallSpeed.__doc__ = """Attributes:
    mean_basecall_speed:
        Mean basecall speed, in bases per second.  This value is only
        streamed for acquisitions where basecalling is enabled.  The
        value reported here is the value stored in last completed
        basecall boxplot bucket Each boxplot bucket covers a duration
        of `boxplot_time_coverage_in_minutes`
"""
# @@protoc_insertion_point(module_scope)
