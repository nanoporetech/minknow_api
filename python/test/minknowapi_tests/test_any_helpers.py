from google.protobuf import (
    wrappers_pb2,
    api_pb2,
    duration_pb2,
    type_pb2,
    field_mask_pb2,
    struct_pb2,
    source_context_pb2,
    timestamp_pb2,
    empty_pb2,
    any_pb2,
)

from minknow_api.protocol_pb2 import BarcodeUserData
from minknow_api.tools import any_helpers

import pytest


def test_pack_unpack():
    """Test packing an unpacking a Protobuf message to/from a Protobuf Any

    We use `BarcodeUserData` as our test message, 'cos it's explicitly NOT a well known type

    - Check round-tripping (packing and unpacking to the same message type)
    - Check unpacking to the wrong message type throws as expected
    - Check unpacking using `unpack_well_known_type_any()` throws as expected (because we are explicitly NOT using a
      well-known type as our message type)
    """

    message = BarcodeUserData(barcode_name="abc")

    any_message = any_helpers.make_any(message)
    assert message == any_helpers.unpack_any(BarcodeUserData, any_message)

    any_message = any_helpers.make_any(BarcodeUserData(barcode_name="abc"))
    assert message == any_helpers.unpack_any(BarcodeUserData, any_message)

    # Try unpacking as the wrong type
    with pytest.raises(TypeError):
        any_helpers.unpack_any(timestamp_pb2.Timestamp, any_message)

    # Try unpacking as `well_known_type`
    # (this is not a well-known type...)
    with pytest.raises(TypeError):
        any_helpers.unpack_well_known_type_any(any_message)


def test_unwrap_well_known_types():
    """Test packing and unpacking of "well known type" messages to/from a Protobuf Any

    - Check that all well-known types can be round-tripped
    - Check that they can be unpacked with `unpack_well_known_type_any()`

    There's a distinction between:
    - "wrapped types"
        - i.e. those that `unpack_well_known_type_any()` unpacks AND unwraps
    - All other "well known types"
        - i.e. those that `unpack_well_known_type_any()` just unpacks

    """
    wrapped_types = (
        (wrappers_pb2.DoubleValue, float),
        (wrappers_pb2.FloatValue, float),
        (wrappers_pb2.Int64Value, int),
        (wrappers_pb2.UInt64Value, int),
        (wrappers_pb2.Int32Value, int),
        (wrappers_pb2.UInt32Value, int),
        (wrappers_pb2.BoolValue, bool),
        (wrappers_pb2.StringValue, str),
        (wrappers_pb2.BytesValue, bytes),
        (empty_pb2.Empty, type(None)),
    )

    for message_type, _ in wrapped_types:
        message = message_type()
        any_message = any_helpers.make_any(message=message)
        result = any_helpers.unpack_any(
            message_type=message_type, any_message=any_message
        )
        assert result == message

    for message_type, result_type in wrapped_types:
        message = message_type()
        any_message = any_helpers.make_any(message=message)
        result = any_helpers.unpack_well_known_type_any(any_message=any_message)
        assert isinstance(result, result_type)
        # Source message was empty
        # So the result should be an empty `result_type`
        assert result == result_type()

    well_known_types = (
        any_pb2.Any,
        api_pb2.Api,
        duration_pb2.Duration,
        type_pb2.Enum,
        type_pb2.EnumValue,
        type_pb2.Field,
        field_mask_pb2.FieldMask,
        struct_pb2.ListValue,
        api_pb2.Method,
        api_pb2.Mixin,
        type_pb2.Option,
        source_context_pb2.SourceContext,
        struct_pb2.Struct,
        timestamp_pb2.Timestamp,
        type_pb2.Type,
        struct_pb2.Value,
    )

    for message_type in well_known_types:
        message = message_type()
        any_message = any_helpers.make_any(message=message)
        result = any_helpers.unpack_any(
            message_type=message_type, any_message=any_message
        )
        assert result == message

    for message_type in well_known_types:
        message = message_type()
        any_message = any_helpers.make_any(message)
        result = any_helpers.unpack_well_known_type_any(any_message=any_message)
        assert result == message


def test_wrapped_types():
    """Test packing and unpacking of "wrapped well known type" messages to/from a Protobuf Any

    - Check that values that have corresponding well-known type wrappers can be round-tripped
    """

    def do_test(make_wrapped_message, wrapped_type, value):
        any_message = make_wrapped_message(value)

        # Unpack and unwrap using `unpack_any`
        wrapped_message = any_helpers.unpack_any(
            message_type=wrapped_type, any_message=any_message
        )
        unwrapped_value = wrapped_message.value

        assert isinstance(wrapped_message, wrapped_type)
        assert unwrapped_value == value

        # Unpack and unwrap using `unpack_well_known_type_any`
        unwrapped_value = any_helpers.unpack_well_known_type_any(
            any_message=any_message
        )

        assert unwrapped_value == value

    do_test(any_helpers.make_double_any, wrappers_pb2.DoubleValue, 42.0)
    do_test(any_helpers.make_double_any, wrappers_pb2.DoubleValue, 123)

    do_test(any_helpers.make_float_any, wrappers_pb2.FloatValue, 42.0)
    do_test(any_helpers.make_float_any, wrappers_pb2.FloatValue, 123)

    do_test(any_helpers.make_int64_any, wrappers_pb2.Int64Value, 123)
    do_test(any_helpers.make_int64_any, wrappers_pb2.Int64Value, -123)

    do_test(any_helpers.make_uint64_any, wrappers_pb2.UInt64Value, 123)

    do_test(any_helpers.make_int32_any, wrappers_pb2.Int32Value, 123)
    do_test(any_helpers.make_int32_any, wrappers_pb2.Int32Value, -123)

    do_test(any_helpers.make_uint32_any, wrappers_pb2.UInt32Value, 123)

    do_test(any_helpers.make_bool_any, wrappers_pb2.BoolValue, True)
    do_test(any_helpers.make_bool_any, wrappers_pb2.BoolValue, False)

    do_test(any_helpers.make_string_any, wrappers_pb2.StringValue, "abc")

    do_test(
        any_helpers.make_bytes_any, wrappers_pb2.BytesValue, bytes([0x11, 0x22, 0x33])
    )
