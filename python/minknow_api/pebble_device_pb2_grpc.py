# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from minknow_api import pebble_device_pb2 as minknow__api_dot_pebble__device__pb2


class PebbleDeviceServiceStub(object):
    """Interface to control Pebble devices.
    This service should be treated as experimental and subject to change
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.change_device_settings = channel.unary_unary(
                '/minknow_api.pebble_device.PebbleDeviceService/change_device_settings',
                request_serializer=minknow__api_dot_pebble__device__pb2.ChangeDeviceSettingsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_pebble__device__pb2.ChangeDeviceSettingsResponse.FromString,
                )
        self.get_device_settings = channel.unary_unary(
                '/minknow_api.pebble_device.PebbleDeviceService/get_device_settings',
                request_serializer=minknow__api_dot_pebble__device__pb2.GetDeviceSettingsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_pebble__device__pb2.GetDeviceSettingsResponse.FromString,
                )
        self.change_channel_settings = channel.unary_unary(
                '/minknow_api.pebble_device.PebbleDeviceService/change_channel_settings',
                request_serializer=minknow__api_dot_pebble__device__pb2.ChangeChannelSettingsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_pebble__device__pb2.ChangeChannelSettingsResponse.FromString,
                )
        self.get_channel_settings = channel.unary_unary(
                '/minknow_api.pebble_device.PebbleDeviceService/get_channel_settings',
                request_serializer=minknow__api_dot_pebble__device__pb2.GetChannelSettingsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_pebble__device__pb2.GetChannelSettingsResponse.FromString,
                )
        self.change_research_only_settings = channel.unary_unary(
                '/minknow_api.pebble_device.PebbleDeviceService/change_research_only_settings',
                request_serializer=minknow__api_dot_pebble__device__pb2.ChangeResearchOnlySettingsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_pebble__device__pb2.ChangeResearchOnlySettingsResponse.FromString,
                )


class PebbleDeviceServiceServicer(object):
    """Interface to control Pebble devices.
    This service should be treated as experimental and subject to change
    """

    def change_device_settings(self, request, context):
        """Change the settings which apply to the whole device.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_device_settings(self, request, context):
        """Get the current settings which apply to the whole device.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def change_channel_settings(self, request, context):
        """Change the settings which apply to the referenced channels.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_channel_settings(self, request, context):
        """Get the channels settings for the requested channel's
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def change_research_only_settings(self, request, context):
        """Experimental access for research purposes to modify low level settings
        Note: Access will be removed once device integration complete
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PebbleDeviceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'change_device_settings': grpc.unary_unary_rpc_method_handler(
                    servicer.change_device_settings,
                    request_deserializer=minknow__api_dot_pebble__device__pb2.ChangeDeviceSettingsRequest.FromString,
                    response_serializer=minknow__api_dot_pebble__device__pb2.ChangeDeviceSettingsResponse.SerializeToString,
            ),
            'get_device_settings': grpc.unary_unary_rpc_method_handler(
                    servicer.get_device_settings,
                    request_deserializer=minknow__api_dot_pebble__device__pb2.GetDeviceSettingsRequest.FromString,
                    response_serializer=minknow__api_dot_pebble__device__pb2.GetDeviceSettingsResponse.SerializeToString,
            ),
            'change_channel_settings': grpc.unary_unary_rpc_method_handler(
                    servicer.change_channel_settings,
                    request_deserializer=minknow__api_dot_pebble__device__pb2.ChangeChannelSettingsRequest.FromString,
                    response_serializer=minknow__api_dot_pebble__device__pb2.ChangeChannelSettingsResponse.SerializeToString,
            ),
            'get_channel_settings': grpc.unary_unary_rpc_method_handler(
                    servicer.get_channel_settings,
                    request_deserializer=minknow__api_dot_pebble__device__pb2.GetChannelSettingsRequest.FromString,
                    response_serializer=minknow__api_dot_pebble__device__pb2.GetChannelSettingsResponse.SerializeToString,
            ),
            'change_research_only_settings': grpc.unary_unary_rpc_method_handler(
                    servicer.change_research_only_settings,
                    request_deserializer=minknow__api_dot_pebble__device__pb2.ChangeResearchOnlySettingsRequest.FromString,
                    response_serializer=minknow__api_dot_pebble__device__pb2.ChangeResearchOnlySettingsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'minknow_api.pebble_device.PebbleDeviceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PebbleDeviceService(object):
    """Interface to control Pebble devices.
    This service should be treated as experimental and subject to change
    """

    @staticmethod
    def change_device_settings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.pebble_device.PebbleDeviceService/change_device_settings',
            minknow__api_dot_pebble__device__pb2.ChangeDeviceSettingsRequest.SerializeToString,
            minknow__api_dot_pebble__device__pb2.ChangeDeviceSettingsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_device_settings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.pebble_device.PebbleDeviceService/get_device_settings',
            minknow__api_dot_pebble__device__pb2.GetDeviceSettingsRequest.SerializeToString,
            minknow__api_dot_pebble__device__pb2.GetDeviceSettingsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def change_channel_settings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.pebble_device.PebbleDeviceService/change_channel_settings',
            minknow__api_dot_pebble__device__pb2.ChangeChannelSettingsRequest.SerializeToString,
            minknow__api_dot_pebble__device__pb2.ChangeChannelSettingsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_channel_settings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.pebble_device.PebbleDeviceService/get_channel_settings',
            minknow__api_dot_pebble__device__pb2.GetChannelSettingsRequest.SerializeToString,
            minknow__api_dot_pebble__device__pb2.GetChannelSettingsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def change_research_only_settings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.pebble_device.PebbleDeviceService/change_research_only_settings',
            minknow__api_dot_pebble__device__pb2.ChangeResearchOnlySettingsRequest.SerializeToString,
            minknow__api_dot_pebble__device__pb2.ChangeResearchOnlySettingsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
