from minknow_api.device import DeviceType
from minknow_api.device_service import GetDeviceInfoResponse


def test_api_device_types_have_a_device_type_enum_value():
    for name, value in GetDeviceInfoResponse.DeviceType.items():
        device_type = DeviceType(value)
        assert device_type.name == name


def test_device_type_enum_values_are_in_the_api():
    api_name_map = {k: v for k, v in GetDeviceInfoResponse.DeviceType.items()}
    for device_type in DeviceType:
        assert device_type.value in GetDeviceInfoResponse.DeviceType.values()
        assert api_name_map[device_type.name] == device_type.value


def test_all_device_type_enum_groups():
    for device_type in DeviceType:
        # Must be only one of minion-like, promethion-like or Pebble
        types_of_thing = 0
        types_of_thing += 1 if device_type.is_minion_like() else 0
        types_of_thing += 1 if device_type.is_promethion_like() else 0
        types_of_thing += 1 if device_type == DeviceType.PEBBLE else 0
        assert (
            types_of_thing == 1
        ), f"{device_type} must be only be one kind of type of device"


def test_p2_solo_device_enum_entry_exists():
    """Explicit regression test for INST-5629."""
    DeviceType(GetDeviceInfoResponse.P2_SOLO) == DeviceType.P2_SOLO
