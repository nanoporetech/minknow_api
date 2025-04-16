# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from minknow_api.ui.sequencing_run import presets_pb2 as minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2


class PresetsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.store_preset = channel.unary_unary(
                '/minknow_api.ui.sequencing_run.presets.PresetsService/store_preset',
                request_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.StorePresetRequest.SerializeToString,
                response_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.StorePresetResponse.FromString,
                )
        self.delete_preset = channel.unary_unary(
                '/minknow_api.ui.sequencing_run.presets.PresetsService/delete_preset',
                request_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.DeletePresetRequest.SerializeToString,
                response_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.DeletePresetResponse.FromString,
                )
        self.get_preset = channel.unary_unary(
                '/minknow_api.ui.sequencing_run.presets.PresetsService/get_preset',
                request_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetPresetRequest.SerializeToString,
                response_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetPresetResponse.FromString,
                )
        self.list_presets = channel.unary_unary(
                '/minknow_api.ui.sequencing_run.presets.PresetsService/list_presets',
                request_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.ListPresetsRequest.SerializeToString,
                response_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.ListPresetsResponse.FromString,
                )
        self.check_preset = channel.unary_unary(
                '/minknow_api.ui.sequencing_run.presets.PresetsService/check_preset',
                request_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.CheckPresetRequest.SerializeToString,
                response_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.CheckPresetResponse.FromString,
                )
        self.get_start_protocol = channel.unary_unary(
                '/minknow_api.ui.sequencing_run.presets.PresetsService/get_start_protocol',
                request_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetStartProtocolRequest.SerializeToString,
                response_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetStartProtocolResponse.FromString,
                )


class PresetsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def store_preset(self, request, context):
        """Store preset data. Input can contain a (protobuf) preset object or a (json) string
        preset. Will store the preset in persistent storage and return a unique preset id
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_preset(self, request, context):
        """Delete a stored preset (limited to user presets). The given preset id will have its
        corresponding preset records erased fromd disc
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_preset(self, request, context):
        """Returns a preset.
        The input can reference a stored preset file via its preset id, or can provide a preset object with the purpose
        of converting the type of the preset into either a protobuf or string.
        The preset return type should be specified in the request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list_presets(self, request, context):
        """Lists all stored presets. Returns a valid subset of preset ids and meta data
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def check_preset(self, request, context):
        """Check if a preset is valid. Validity is determined by if the preset can be successfully serialised into a Preset object.
        If given a preset id, then validity requires the corresponding preset file to be present and for the preset file itself to be a valid.
        If provided a preset string, then validity is determined.
        Finally, if a preset object is provided, then it is assumed valid.

        Returns preset meta data if it is valid, otherwise returns INVALID_ARGUMENT.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_start_protocol(self, request, context):
        """Gets a start request. Given an preset id, object or string, returns a valid corresponding start request
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PresetsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'store_preset': grpc.unary_unary_rpc_method_handler(
                    servicer.store_preset,
                    request_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.StorePresetRequest.FromString,
                    response_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.StorePresetResponse.SerializeToString,
            ),
            'delete_preset': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_preset,
                    request_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.DeletePresetRequest.FromString,
                    response_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.DeletePresetResponse.SerializeToString,
            ),
            'get_preset': grpc.unary_unary_rpc_method_handler(
                    servicer.get_preset,
                    request_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetPresetRequest.FromString,
                    response_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetPresetResponse.SerializeToString,
            ),
            'list_presets': grpc.unary_unary_rpc_method_handler(
                    servicer.list_presets,
                    request_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.ListPresetsRequest.FromString,
                    response_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.ListPresetsResponse.SerializeToString,
            ),
            'check_preset': grpc.unary_unary_rpc_method_handler(
                    servicer.check_preset,
                    request_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.CheckPresetRequest.FromString,
                    response_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.CheckPresetResponse.SerializeToString,
            ),
            'get_start_protocol': grpc.unary_unary_rpc_method_handler(
                    servicer.get_start_protocol,
                    request_deserializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetStartProtocolRequest.FromString,
                    response_serializer=minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetStartProtocolResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'minknow_api.ui.sequencing_run.presets.PresetsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PresetsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def store_preset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.ui.sequencing_run.presets.PresetsService/store_preset',
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.StorePresetRequest.SerializeToString,
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.StorePresetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_preset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.ui.sequencing_run.presets.PresetsService/delete_preset',
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.DeletePresetRequest.SerializeToString,
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.DeletePresetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_preset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.ui.sequencing_run.presets.PresetsService/get_preset',
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetPresetRequest.SerializeToString,
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetPresetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list_presets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.ui.sequencing_run.presets.PresetsService/list_presets',
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.ListPresetsRequest.SerializeToString,
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.ListPresetsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def check_preset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.ui.sequencing_run.presets.PresetsService/check_preset',
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.CheckPresetRequest.SerializeToString,
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.CheckPresetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_start_protocol(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/minknow_api.ui.sequencing_run.presets.PresetsService/get_start_protocol',
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetStartProtocolRequest.SerializeToString,
            minknow__api_dot_ui_dot_sequencing__run_dot_presets__pb2.GetStartProtocolResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
