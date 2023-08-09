import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import mock_server
from mock_server import Server

from minknow_api import device_pb2, manager_pb2

LIST_POSITIONS_SOURCE = (
    Path(__file__).parent.parent.parent
    / "minknow_api"
    / "examples"
    / "manage_simulated_devices.py"
)

MS00000 = manager_pb2.FlowCellPosition(
    name="MS00000",
    state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
    rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(secure=420),
    device_type=device_pb2.GetDeviceInfoResponse.DeviceType.MINION,
    is_simulated=True,
    is_integrated=False,
)


class ManagerServicer(mock_server.ManagerServicer):
    """
    Adds add_simulated_device() and remove_simulated_device() to
    mock_server.ManagerServicer().
    """

    def __init__(self, positions: Optional[List[manager_pb2.FlowCellPosition]] = None):
        super().__init__(positions=positions)

    def add_simulated_device(
        self, request: manager_pb2.AddSimulatedDeviceRequest, context
    ):
        if request.type == manager_pb2.SimulatedDeviceType.SIMULATED_MINION:
            device_type = device_pb2.GetDeviceInfoResponse.DeviceType.MINION
        elif request.type == manager_pb2.SimulatedDeviceType.SIMULATED_P2:
            device_type = device_pb2.GetDeviceInfoResponse.DeviceType.P2_SOLO
        elif request.type == manager_pb2.SimulatedDeviceType.SIMULATED_PROMETHION:
            device_type = device_pb2.GetDeviceInfoResponse.DeviceType.PROMETHION
        else:
            raise RuntimeError(f"Unknown device type {request.type}")
        pos = manager_pb2.FlowCellPosition(
            name=request.name,
            state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
            rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(secure=420),
            device_type=device_type,
            is_simulated=True,
            is_integrated=False,
        )
        self.positions.append(pos)
        return manager_pb2.AddSimulatedDeviceResponse()

    def remove_simulated_device(
        self, request: manager_pb2.RemoveSimulatedDeviceRequest, context
    ):
        self.positions = [pos for pos in self.positions if pos.name != request.name]
        return manager_pb2.RemoveSimulatedDeviceResponse()


def normalize_new_lines(val):
    return val.replace("\r\n", "\n").replace("\r", "\n")


def test_list_simulated_positions_no_positions():
    """Verify no positions are listed when nothing available."""

    manager_servicer = ManagerServicer()
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--list",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = "Connected simulated positions on MinKNOW at 127.0.0.1:\n"

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )


def test_list_one_simulated_position():
    """List a present simulated position"""
    manager_servicer = ManagerServicer(positions=[MS00000])
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--list",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = "Connected simulated positions on MinKNOW at 127.0.0.1:\n\tMS00000: MINION\n"

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )


def test_add_one_simulated_device():
    """Add one simulated position"""
    manager_servicer = ManagerServicer()
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--add",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Added simulated device MS00000.\n"""

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )
        assert (
            manager_servicer.positions[0].device_type
            == device_pb2.GetDeviceInfoResponse.DeviceType.MINION
        )


def test_add_multiple_simulated_devices():
    """Add multiple simulated positions"""
    manager_servicer = ManagerServicer()
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--add",
                "MS00000",
                "MS00001",
                "MS00002",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Added simulated device MS00000.\nAdded simulated device MS00001.\nAdded simulated device MS00002.\n"""

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )


def test_add_promethion_device():
    """Add a simulated promethion flow cell"""
    manager_servicer = ManagerServicer()
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--prom",
                "--add",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Added simulated device 1A.\n"""

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )

        assert (
            manager_servicer.positions[0].device_type
            == device_pb2.GetDeviceInfoResponse.DeviceType.PROMETHION
        )


def test_add_multi_promethion_device():
    """Add a simulated promethion flow cell"""
    manager_servicer = ManagerServicer()
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--prom",
                "--add",
                "1A",
                "2B",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Added simulated device 1A.\nAdded simulated device 2B.\n"""

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )

        assert (
            manager_servicer.positions[0].device_type
            == device_pb2.GetDeviceInfoResponse.DeviceType.PROMETHION
        )


def test_add_p2_device():
    """Add a simulated promethion flow cell"""
    manager_servicer = ManagerServicer()
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--p2",
                "--add",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Added simulated device PS2_000000-A.\n"""

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )

        assert (
            manager_servicer.positions[0].device_type
            == device_pb2.GetDeviceInfoResponse.DeviceType.P2_SOLO
        )


def test_remove_simulated_device():
    """Remove an already present simulated device"""
    manager_servicer = ManagerServicer(positions=[MS00000])
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--remove",
                "MS00000",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Removed device MS00000.\n"""

        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )


def test_remove_all_simulated_devices():
    """Remove all already present simulated devices"""
    manager_servicer = ManagerServicer(
        positions=[
            MS00000,
            manager_pb2.FlowCellPosition(
                name="MS00001",
                state=manager_pb2.FlowCellPosition.State.STATE_RUNNING,
                rpc_ports=manager_pb2.FlowCellPosition.RpcPorts(secure=421),
                device_type=device_pb2.GetDeviceInfoResponse.DeviceType.MINION,
                is_simulated=True,
                is_integrated=False,
            ),
        ]
    )
    with Server([manager_servicer]) as server:
        p = subprocess.run(
            [
                sys.executable,
                str(LIST_POSITIONS_SOURCE),
                "--host=127.0.0.1",
                "--port",
                str(server.port),
                "--remove-all",
            ],
            check=True,
            stdout=subprocess.PIPE,
        )

        expected_output = """Removing all simulated devices.\nRemoved device MS00000.\nRemoved device MS00001.\nFinished removing devices.\n"""
        assert normalize_new_lines(p.stdout.decode("utf-8")) == normalize_new_lines(
            expected_output
        )
