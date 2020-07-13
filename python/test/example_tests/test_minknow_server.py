"""Test grpc server for minknow_api"""

from collections import namedtuple
from concurrent import futures
from contextlib import closing
import logging
import socket
import typing

import grpc
from minknow_api import device_pb2, device_pb2_grpc
from minknow_api import instance_pb2, instance_pb2_grpc
from minknow_api import manager_pb2, manager_pb2_grpc
from minknow_api import protocol_pb2, protocol_pb2_grpc

LOGGER = logging.getLogger(__name__)

PositionInfo = namedtuple("PositionInfo", ["position_name",])
FlowCellInfo = namedtuple("PositionInfo", ["flow_cell_id", "has_flow_cell"])


class DeviceService(device_pb2_grpc.DeviceServiceServicer):
    def __init__(self, position_info):
        self.position_info = position_info
        self.flow_cell_info = FlowCellInfo(flow_cell_id="", has_flow_cell=False)

    def get_flow_cell_info(
        self, _request: device_pb2.GetFlowCellInfoRequest, _context
    ) -> device_pb2.GetFlowCellInfoResponse:
        """Find the version information for the connected flow cell"""
        return device_pb2.GetFlowCellInfoResponse(
            channel_count=512,
            wells_per_channel=4,
            has_flow_cell=self.flow_cell_info.has_flow_cell,
            flow_cell_id=self.flow_cell_info.flow_cell_id,
            has_adapter=False,
        )


class InstanceService(instance_pb2_grpc.InstanceServiceServicer):
    def __init__(self, position_info):
        self.position_info = position_info

    def get_version_info(
        self, _request: instance_pb2.GetVersionInfoRequest, _context
    ) -> instance_pb2.GetVersionInfoResponse:
        """Find the version information for the instance"""
        return instance_pb2.GetVersionInfoResponse(
            minknow=instance_pb2.GetVersionInfoResponse.MinknowVersion(
                major=4, minor=0, patch=0, full="4.0.0"
            )
        )


class ManagerService(manager_pb2_grpc.ManagerServiceServicer):
    """
    Test server implementation of ManagerService.
    """

    def __init__(self, positions: typing.List[manager_pb2.FlowCellPosition] = None):
        self.positions = positions if positions else []

    def get_version_info(
        self, _request: manager_pb2.GetVersionInfoRequest, _context
    ) -> manager_pb2.GetVersionInfoResponse:
        """Find the version information for the manager"""
        return manager_pb2.GetVersionInfoResponse(
            minknow=instance_pb2.GetVersionInfoResponse.MinknowVersion(
                major=4, minor=0, patch=0, full="4.0.0"
            )
        )

    def flow_cell_positions(
        self, _request: manager_pb2.FlowCellPositionsRequest, _context
    ):
        """Find which positions are connected to the host"""
        yield manager_pb2.FlowCellPositionsResponse(
            positions=self.positions, total_count=len(self.positions)
        )

    def watch_flow_cell_positions(
        self, _request: manager_pb2.FlowCellPositionsRequest, _context
    ):
        """Find which positions are connected to the host - streams additions once, then nothing"""
        yield manager_pb2.WatchFlowCellPositionsResponse(additions=self.positions)


class ProtocolService(protocol_pb2_grpc.ProtocolServiceServicer):
    def __init__(self, position_info):
        self.position_info = position_info
        self.protocol_list = []
        self.started_protocols = []

    def list_protocols(
        self, _request: protocol_pb2.ListProtocolsRequest, _context
    ) -> protocol_pb2.ListProtocolsResponse:
        """Find the version information for the connected flow cell"""
        return protocol_pb2.ListProtocolsResponse(protocols=self.protocol_list)

    def start_protocol(
        self, request: protocol_pb2.StartProtocolRequest, _context
    ) -> protocol_pb2.StartProtocolResponse:
        self.started_protocols.append(request)
        return protocol_pb2.StartProtocolResponse(
            run_id=str(len(self.started_protocols))
        )


def get_free_network_port() -> int:
    """Find a free port number"""
    with closing(socket.socket()) as temp_socket:
        temp_socket.bind(("", 0))
        return temp_socket.getsockname()[1]


class ManagerTestServer:
    """
    Test server runs grpc manager service on a port.
    """

    def __init__(self, port=None, positions=None):
        self.port = port
        if not self.port:
            self.port = get_free_network_port()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        self.manager_service = ManagerService(positions)
        manager_pb2_grpc.add_ManagerServiceServicer_to_server(
            self.manager_service, self.server
        )

        LOGGER.info("Starting server. Listening on port %s.", self.port)
        self.server.add_insecure_port("[::]:%s" % self.port)
        self.server.start()

    def stop(self):
        """Stop grpc server"""
        self.server.stop(0)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop()


class SequencingPositionTestServer:
    """
    Test server runs grpc manager service on a port.
    """

    def __init__(self, position_info, port=None):
        self.port = port
        if not self.port:
            self.port = get_free_network_port()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        self.device_service = DeviceService(position_info)
        device_pb2_grpc.add_DeviceServiceServicer_to_server(
            self.device_service, self.server
        )
        self.instance_service = InstanceService(position_info)
        instance_pb2_grpc.add_InstanceServiceServicer_to_server(
            self.instance_service, self.server
        )

        self.protocol_service = ProtocolService(position_info)
        protocol_pb2_grpc.add_ProtocolServiceServicer_to_server(
            self.protocol_service, self.server
        )

        LOGGER.info("Starting server. Listening on port %s.", self.port)
        self.server.add_insecure_port("[::]:%s" % self.port)
        self.server.start()

    def set_flow_cell_info(self, flow_cell_info):
        """Set connected flow cell info"""
        self.device_service.flow_cell_info = flow_cell_info

    def set_protocol_list(self, protocol_list):
        """Set available protocols on the position"""
        self.protocol_service.protocol_list = protocol_list

    def stop(self):
        """Stop grpc server"""
        self.server.stop(0)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop()
