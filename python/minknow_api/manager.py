"""
Helpers for accessing the manager
=================================

If you are connecting to MinKNOW externally (rather than from a protocol script), you will need to
go via the manager. This listens on a known port, and can enumerate the available flow cell
positions. There may only be one position (eg: on a Mk1C), or there may be many (PromethIONs can
have 24 or 48, for example).

This can be done with the `Manager` class in this module. The other classes this module provides are
usually constructing using methods on ``Manager``.

"""


from google.protobuf import timestamp_pb2
import grpc
import logging
import typing
import minknow_api
import minknow_api.basecaller_service
import minknow_api.manager_service
import minknow_api.keystore_service

__all__ = [
    "Basecaller",
    "FlowCellPosition",
    "Manager",
    "get_local_authentication_token_file",
]


def get_local_authentication_token_file(host="127.0.0.1", port=None):
    """Starts an isolated manager instance to retrieve the path
    of the local authentication token file, which can then
    be read to extract the local authentication token"""
    if not port:
        port = 9502

    try:
        ssl_creds = grpc.ssl_channel_credentials(minknow_api.read_ssl_certificate())

        channel = grpc.secure_channel(
            host + ":" + str(port),
            ssl_creds,
            # we need the ssl target name override
            options=minknow_api.GRPC_CHANNEL_OPTIONS,
        )

        service = minknow_api.manager_service.ManagerService(channel)
        return service.local_authentication_token_path().path
    except grpc.RpcError:
        logging.debug(
            "Unable to connect to manager on port '{}' to retrieve local auth token path".format(
                port
            ),
            exc_info=True,
        )
        return None


class ServiceBase(object):
    """Implementation detail for Manager and Basecaller - do not use directly."""

    def __init__(self, serviceclass, host, port, credentials=None):
        self.host = host
        self.port = port
        self.credentials = credentials
        self.channel = grpc.secure_channel(
            host + ":" + str(port),
            self.credentials,
            options=minknow_api.GRPC_CHANNEL_OPTIONS,
        )
        self.rpc = serviceclass(self.channel)
        self.stub = self.rpc._stub

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.channel is not None:
            self.channel.close()
        self.rpc = None
        self.stub = None
        self.channel = None


GuppyConnectionInfo = typing.NamedTuple(
    "GuppyConnectionInfo",
    [
        ("port", typing.Optional[int]),
        ("ipc_path", typing.Optional[str]),
    ],
)


class Manager(ServiceBase):
    """A connection to the manager gRPC interface.

    Args:
        host (str, optional): The hostname to connect to (IP address will not work due to TLS).
        port (int, optional): Override the port to connect to.
        developer_api_token (str, optional): A token to use for auth when connecting
            using a developer token (ignored if `credentials` is provided).
        credentials (grpc.ChannelCredentials, optional): Provide the credentials to use
            for the connection. If it is not provided, one will be constructed using
            minknow.credentials().

    Attributes:
        bream_version (str): The version of Bream that is installed.
        config_version (str): The version of ont-configuration (Wanda) that is installed.
        channel (grpc.Channel): The gRPC channel used for communication.
        core_version (str): The running version of MinKNOW Core.
        core_version_components (tuple): A tuple of three integers describing the major, minor and
            patch parts of the core version. Useful for version comparisions.
        credentials (grpc.ChannelCredentials): The credentials used for the gRPC
            connection. Can used to connect to other MinKNOW interfaces. Changing this
            will not affect the connection to the manager, but will affect connections
            made to other MinKNOW services (like the basecaller).
        guppy_version (str): The version of Guppy that is running.
        host (str): The hostname used to connect.
        port (int): The port used to connect.
        rpc (minknow_api.manager_service.ManagerService): The auto-generated API wrapper.
        stub (minknow_api.manager_grpc_pb2.ManagerServiceStub): The gRPC-generated stub.
        version (str): The version of the MinKNOW distribution
        version_status (str): The status of the installed distribution ("unknown", "stable",
            "unstable" or "modified").
    """

    # The thread that handles some of these RPCs can block for a second or two in an operating
    # system call to start a process, especially on Windows. 5 seconds gives plenty of margin for
    # interference from antivirus hooks, for example, while still not blocking forever if something
    # has gone wrong with the manager.
    DEFAULT_TIMEOUT = 5

    def __init__(
        self,
        host="127.0.0.1",
        port=None,
        developer_api_token=None,
        credentials=None,
    ):
        if port is None:
            port = 9502

        credentials = None
        if credentials is None:
            credentials = minknow_api.grpc_credentials(
                manager_port=port, developer_api_token=developer_api_token, host=host
            )
        super(Manager, self).__init__(
            minknow_api.manager_service.ManagerService,
            host=host,
            port=port,
            credentials=credentials,  # saved as self.credentials
        )
        self._developer_api_token = developer_api_token

        version_info = self.rpc.get_version_info()
        self.bream_version = version_info.bream
        self.config_version = version_info.protocol_configuration
        self.core_version = version_info.minknow.full
        self.core_version_components = (
            version_info.minknow.major,
            version_info.minknow.minor,
            version_info.minknow.patch,
        )
        self.guppy_version = version_info.guppy_connected_version
        self.version = version_info.distribution_version
        DistributionStatus = (
            minknow_api.instance_pb2.GetVersionInfoResponse.DistributionStatus
        )
        self.version_status = DistributionStatus.Name(
            version_info.distribution_status
        ).lower()

    def __repr__(self):
        return "Manager({!r}, {!r})".format(self.host, self.port)

    def keystore(self):
        """
        Find the keystore service running for this manager.

        Returns:
            KeyStore: The gRPC service for the manager level keystore.
        """
        return minknow_api.keystore_service.KeyStoreService(self.channel)

    def basecaller(self, timeout=DEFAULT_TIMEOUT):
        """Connect to the basecalling interface.

        Args:
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            minknow_api.manager.Basecaller: The wrapper for the Basecaller service, or None if the
                connection couldn't be made.
        """
        bc_api = self.rpc.basecaller_api(
            minknow_api.manager_service.BasecallerApiRequest(), timeout=timeout
        )
        if bc_api.secure == 0:
            return None
        return Basecaller(self.host, bc_api.secure, credentials=self.credentials)

    def create_directory(self, name, parent_path="", timeout=DEFAULT_TIMEOUT):
        """Create a directory on the host.

        Args:
            name (str): The name of the directory to be created.
            parent_path (str, optional): The name of the directory to be created.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            str: the name of the created directory
        """
        request = minknow_api.manager_service.CreateDirectoryRequest(
            parent_path=parent_path, name=name
        )
        return self.rpc.create_directory(request, _timeout=timeout).path

    def guppy_port(self, timeout=DEFAULT_TIMEOUT):
        """Get the port that Guppy is listening on.

        This can be used to directly connect to the Guppy server using the pyguppy client.

        Args:
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            int: The port Guppy is listening on
        """
        return self.rpc.get_guppy_info(_timeout=timeout).port

    def get_guppy_connection_info(self, timeout=DEFAULT_TIMEOUT):
        """Get the port and ipc_path that Guppy is listening to.

        This can be used to directly connect to the Guppy server using the pyguppy client.

        Guppy only listens on either a port or the ipc path. The default changes based on OS.
        Calling code should change its behaviour based on which tuple field is not None.

        Args:
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            GuppyConnectionInfo: Either the port or path guppy is listening on.
        """
        guppy_info = self.rpc.get_guppy_info(_timeout=timeout)
        port = None
        ipc_path = None
        if guppy_info.port != 0:
            port = guppy_info.port
        else:
            ipc_path = guppy_info.ipc_path
        return GuppyConnectionInfo(port, ipc_path)

    def describe_host(self, timeout=DEFAULT_TIMEOUT):
        """Get information about the machine running MinKNOW.

        Args:
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            minknow_api.manager_service.DescribeHostResponse: The information about the host.
        """
        return self.rpc.describe_host(_timeout=timeout)

    def reset_position(self, position, force=False, timeout=DEFAULT_TIMEOUT):
        """Reset a flow cell position.

        Args:
            position (str): The name of the position to reset.
            force (bool, optional): Restart the position even if it seems to be running fine.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        self.reset_positions([position], force=force, timeout=timeout)

    def reset_positions(self, positions, force=False, timeout=DEFAULT_TIMEOUT):
        """Reset flow-cell positions

        Args:
            positions (list of strings): The names of the positions to reset.
            force (bool, optional): Restart the position even if it seems to be running fine.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        self.rpc.reset_position(_timeout=timeout, positions=positions, force=force)

    def flow_cell_positions(self, timeout=DEFAULT_TIMEOUT):
        """Get a list of flow cell positions.

        Args:
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Yields:
            FlowCellPosition: A flow cell position. Ordering is not guaranteed.
        """
        call = self.rpc.flow_cell_positions(_timeout=timeout)
        # avoid holding open the call for longer than necessary by consuming all the results up
        # front
        messages = [msg for msg in call]
        for msg in messages:
            for position in msg.positions:
                yield FlowCellPosition(
                    position,
                    self.host,
                    developer_api_token=self._developer_api_token,
                    credentials=self.credentials,
                )

    def add_simulated_device(self, name, type, timeout=DEFAULT_TIMEOUT):
        """Dynamically create a simulated device

        Args:
            name (string): name of simulated device to create. Should not exist already.
                The format depends on the type of device being created,
                For MinIONs and MinION-mk1Cs, "MS" followed by five digits, eg: "MS12345".
                For GridIONs, "GS" followed by five digits, eg: "GS12345".
                PromethIONs position-names have no format restriction
            type (minknow_api.manager_pb2.SimulatedDeviceType): Type of device to create.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
            usually be left at the default.
        """
        self.rpc.add_simulated_device(_timeout=timeout, name=name, type=type)

    def remove_simulated_device(self, name, timeout=DEFAULT_TIMEOUT):
        """Dynamically remove a simulated device

        Args:
            name (string): name of device to remove. It should exist and be simulated.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
            usually be left at the default.
        """
        self.rpc.remove_simulated_device(_timeout=timeout, name=name)

    def get_alignment_reference_information(self, path, timeout=DEFAULT_TIMEOUT):
        """Query alignment reference information from a file path.

        Args:
            path (string): Path of the alignment reference file.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
            usually be left at the default.
        """
        return self.rpc.get_alignment_reference_information(_timeout=timeout, path=path)

    def create_developer_api_token(self, name, expiry=None, timeout=DEFAULT_TIMEOUT):
        """Create a new developer api token, which expires at [expiry].

        Can not be invoked when using a developer token as authorisation method.

        Args:
            name (string): Readable name of the token.
            expiry (datetime, optional): Expiry time of the token.
            timeout (float, optional): The maximum time to wait for the call to complete. Should
            usually be left at the default.
        """

        kwargs = {}
        if expiry:
            ts = timestamp_pb2.Timestamp()
            ts.FromDatetime(dt=expiry)
            kwargs["expiry"] = ts
        return self.rpc.create_developer_api_token(
            _timeout=timeout, name=name, **kwargs
        )

    def revoke_developer_api_token(self, id, timeout=DEFAULT_TIMEOUT):
        """Revoke an existing developer api tokens.

        Args:
            id (string): The identification of the token (available from list_developer_api_tokens).
            timeout (float, optional): The maximum time to wait for the call to complete. Should
            usually be left at the default.
        """
        return self.rpc.revoke_developer_api_token(id=id, _timeout=timeout)

    def list_developer_api_tokens(self, timeout=DEFAULT_TIMEOUT):
        """List existing developer api tokens.

        Args:
            timeout (float, optional): The maximum time to wait for the call to complete. Should
            usually be left at the default.
        """
        return self.rpc.list_developer_api_tokens(_timeout=timeout)

    def find_protocols(
        self,
        experiment_type,
        flow_cell_product_code=None,
        sequencing_kit=None,
        timeout=DEFAULT_TIMEOUT,
    ):
        """List existing developer api tokens.

        Args:
            experiment_type (manager.ExperimentType): Type of experiment to search for.
            flow_cell_product_code (str, optional): Find only protocols compatible with the given flow cell code.
                Default 'None' will return protocols matching any (including protocols without a flow_cell_product_code).
            sequencing_kit (str, optional): Find only protocols compatible with the given sequencing kit.
                Default 'None' will return protocols matching any (including protocols without a sequencing_kit).
            timeout (float, optional): The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        kwargs = {}
        if flow_cell_product_code is not None:
            kwargs["flow_cell_product_code"] = flow_cell_product_code
        if sequencing_kit is not None:
            kwargs["sequencing_kit"] = sequencing_kit

        return self.rpc.find_protocols(experiment_type=experiment_type, **kwargs)


class FlowCellPosition(object):
    """A flow cell position.

    You should not normally construct this directly, but instead call
    `Manager.flow_cell_positions`. The constructor arguments may change between minor
    releases.

    Args:
        description (minknow_api.manager_service.FlowCellPosition): A description of a flow cell
            position returned from a call to ``flow_cell_positions`` or
            ``watch_flow_cell_positions`` on the manager.
        host (string, optional): The hostname of the manager API (see Manager.host). This will be
            used by the `connect` method. Defauls to localhost.
        developer_api_token (str, optional): A token to use for auth when connecting
            using a developer token (ignored if `credentials` is provided).
        credentials (grpc.ChannelCredentials, optional): Provide the credentials to use
            for the connection. If it is not provided, one will be constructed using
            minknow.credentials().

    Attributes:
        description (minknow_api.manager_service.FlowCellPosition): The description of
            the flow cell position as returned from a call to ``flow_cell_positions``
            on the manger.
        credentials (grpc.ChannelCredentials): The credentials used for the gRPC
            connection. Can used to connect to other MinKNOW interfaces. Changing this
            will affect future calls to connect().
        host (string): The hostname of the machine the position is running on.
    """

    def __init__(
        self,
        description,
        host="127.0.0.1",
        developer_api_token=None,
        credentials=None,
    ):
        self.host = host
        self.description = description
        self._developer_api_token = developer_api_token
        self._device = None
        self.credentials = credentials

    def __repr__(self):
        return "FlowCellPosition({!r}, {{{!r}}})".format(self.host, self.description)

    def __str__(self):
        return "{} ({})".format(self.name, self.state)

    @property
    def name(self):
        """str: The name of the position."""
        return self.description.name

    @property
    def location(self):
        """minknow_api.manager_service.FlowCellPosition.Location: The location of the position.

        Returns None if no location information is available. Location information should always be
        available for integrated positions.
        """
        if self.description.HasField("location"):
            return self.description.location
        else:
            return None

    @property
    def shared_hardware_group(self):
        """minknow_api.manager_service.FlowCellPosition.SharedHardwareGroup: The information about
        shared hardware (if built-in, otherwise None).
        """
        if self.description.HasField("shared_hardware_group"):
            return self.description.shared_hardware_group
        else:
            return None

    @property
    def state(self):
        """str: The state of the position.

        One of "initialising", "running", "resetting", "hardware_removed", "hardware_error",
        "software_error" or "needs_association".
        """
        State = minknow_api.manager_service.FlowCellPosition.State
        return State.Name(self.description.state)[6:].lower()

    @property
    def running(self):
        """bool: Whether the software for the position is running.

        Note that this is not directly equivalent to the "running" value of `state`: even when there
        are hardware errors, the software may still be running.
        """
        return self.description.HasField("rpc_ports")

    @property
    def is_integrated(self):
        """bool: Whether the position is integrated.

        For example, the X1 through X5 positions on a GridION are integrated positions: they are
        part of the GridION itself. A MinION Mk1B is not integrated.
        """
        return self.description.is_integrated

    @property
    def is_simulated(self):
        return self.description.is_simulated

    @property
    def device_type(self):
        device_type_value = self.description.device_type
        return minknow_api.device_pb2.GetDeviceInfoResponse.DeviceType.Name(
            device_type_value
        )

    def connect(self, credentials=None, developer_api_token=None):
        """Connect to the position.

        Only valid to do if `running` is True.

        Returns:
            minknow_api.Connection: A connection to the RPC interface.
        """
        port = self.description.rpc_ports.secure
        if credentials is None:
            credentials = self.credentials
        if not developer_api_token:
            developer_api_token = self._developer_api_token
        if port == 0:
            raise RuntimeError(
                "Invalid port for connection to '%s': '%s'" % (self.description, port)
            )
        return minknow_api.Connection(
            host=self.host,
            port=port,
            credentials=credentials,
            developer_api_token=developer_api_token,
        )


class Basecaller(ServiceBase):
    """A connection to the basecalling gRPC interface.

    You should not normally construct this directly - use `Manager.basecaller` instead.
    The constructor arguments may change between minor releases.

    Note that

    Args:
        host (str, optional): The hostname to connect to (IP address will not work due to TLS).
        port (int, optional): Override the port to connect to.
        credentials (grpc.ChannelCredentials): Provide the credentials to use
            for the connection.

    Attributes:
        channel (grpc.Channel): the gRPC channel used for communication
        credentials (grpc.ChannelCredentials): The credentials used for the gRPC
            connection. Can used to connect to other MinKNOW interfaces. Note that
            changing this will not affect the connection to the basecaller service.
        host (str): the hostname used to connect
        port (int): the port used to connect
        rpc (minknow_api.manager_service.ManagerService): the auto-generated API wrapper
        stub (minknow_api.manager_grpc_pb2.ManagerServiceStub): the gRPC-generated stub
    """

    def __init__(self, host="127.0.0.1", port=None, credentials=None):
        if not credentials:
            raise TypeError("Expected credentials to be specified")

        super(Basecaller, self).__init__(
            minknow_api.basecaller_service.Basecaller,
            host=host,
            port=port,
            credentials=credentials,
        )

    def __repr__(self):
        return "Basecaller({!r}, {!r})".format(self.host, self.port)
