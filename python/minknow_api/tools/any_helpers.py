"""Tools for packing/unpacking `google.protobuf.Any` messages"""

from google.protobuf import (
    any_pb2,
    timestamp_pb2,
    wrappers_pb2,
    duration_pb2,
    api_pb2,
    type_pb2,
    field_mask_pb2,
    struct_pb2,
    source_context_pb2,
    empty_pb2,
)


def make_any(message) -> any_pb2.Any:
    """Packs the specified message into a protobuf Any"""
    any_message = any_pb2.Any()
    any_message.Pack(message)
    return any_message


def make_double_any(value: float) -> any_pb2.Any:
    return make_any(wrappers_pb2.DoubleValue(value=value))


def make_float_any(value: float) -> any_pb2.Any:
    return make_any(wrappers_pb2.FloatValue(value=value))


def make_int64_any(value: int) -> any_pb2.Any:
    return make_any(wrappers_pb2.Int64Value(value=value))


def make_uint64_any(value: int) -> any_pb2.Any:
    return make_any(wrappers_pb2.UInt64Value(value=value))


def make_int32_any(value: int) -> any_pb2.Any:
    return make_any(wrappers_pb2.Int32Value(value=value))


def make_uint32_any(value: int) -> any_pb2.Any:
    return make_any(wrappers_pb2.UInt32Value(value=value))


def make_bool_any(value: bool) -> any_pb2.Any:
    return make_any(wrappers_pb2.BoolValue(value=value))


def make_string_any(value: str) -> any_pb2.Any:
    return make_any(wrappers_pb2.StringValue(value=value))


def make_bytes_any(value: bytes) -> any_pb2.Any:
    return make_any(wrappers_pb2.BytesValue(value=value))


def unpack_any(message_type, any_message: any_pb2.Any):
    """Unpacks an `Any` message into the specified `message_type`"""

    message = message_type()
    unpacked_ok = any_message.Unpack(message)
    if not unpacked_ok:
        raise TypeError(
            "Could not unpack as `any_message` does not contain supplied `message_type`"
        )
    return message


def unpack_well_known_type_any(any_message: any_pb2.Any):
    """Unpacks well-known types that are wrapped in an Any

    Detects the message type based on the `Any`

    Also unwraps well-known wrapper types for convenience
    """
    wrapped_types = {
        t.DESCRIPTOR.full_name: t
        for t in (
            wrappers_pb2.DoubleValue,
            wrappers_pb2.FloatValue,
            wrappers_pb2.Int64Value,
            wrappers_pb2.UInt64Value,
            wrappers_pb2.Int32Value,
            wrappers_pb2.UInt32Value,
            wrappers_pb2.BoolValue,
            wrappers_pb2.StringValue,
            wrappers_pb2.BytesValue,
        )
    }

    type_name = any_message.TypeName()

    wrapped_type = wrapped_types.get(type_name, None)
    if wrapped_type:
        return unpack_any(message_type=wrapped_type, any_message=any_message).value

    well_known_types = {
        t.DESCRIPTOR.full_name: t
        for t in (
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
    }

    well_known_type = well_known_types.get(type_name, None)
    if well_known_type:
        return unpack_any(message_type=well_known_type, any_message=any_message)

    # Special case the `Empty` message and return None
    if any_message.Is(empty_pb2.Empty.DESCRIPTOR):
        return None

    raise TypeError("Supplied `any_message` did not contain a well-known type")
