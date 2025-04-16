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

import datetime
import os
import warnings
from typing import Dict, Iterator, Optional, NamedTuple, Sequence, Union

import grpc
from google.protobuf import timestamp_pb2

import minknow_api
import minknow_api.basecaller_service
import minknow_api.keystore_service
import minknow_api.log_service
import minknow_api.ui.sequencing_run.presets_service
import minknow_api.hardware_check_service
import minknow_api.manager_pb2 as manager_pb2
import minknow_api.device_pb2 as device_pb2
import minknow_api.manager_service
import minknow_api.v2.protocols_service
import minknow_api.protocol_settings_pb2 as protocol_settings_pb2

from minknow_api import Connection, get_local_authentication_token_file

__all__ = [
    "Basecaller",
    "FlowCellPosition",
    "Manager",
    "get_local_authentication_token_file",  # Moved to minknow_api.__init__, but we export here for backwards compat for now
]


class ServiceBase(object):
    """Implementation detail for Manager and Basecaller - do not use directly."""

    def __init__(
        self,
        serviceclass: type,
        host: str,
        port: int,
        credentials: Optional[grpc.ChannelCredentials] = None,
    ):
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

    def close(self) -> None:
        """Close the RPC connection."""
        if self.channel is not None:
            self.channel.close()
        self.rpc = None
        self.stub = None
        self.channel = None


GuppyConnectionInfo = NamedTuple(
    "GuppyConnectionInfo",
    [
        ("port", Optional[int]),
        ("ipc_path", Optional[str]),
    ],
)


class FlowCellPosition(object):
    """A flow cell position.

    You should not normally construct this directly, but instead call
    `Manager.flow_cell_positions`. The constructor arguments may change between minor
    releases.

    Args:
        description: A description of a flow cell
            position returned from a call to ``flow_cell_positions`` or
            ``watch_flow_cell_positions`` on the manager.
        host: The hostname of the manager API (see Manager.host). This will be
            used by the `connect` method.
        credentials: Provide the credentials to use
            for the connection.

    Attributes:
        description (minknow_api.manager_pb2.FlowCellPosition): The description of
            the flow cell position as returned from a call to ``flow_cell_positions``
            on the manager.
        credentials (grpc.ChannelCredentials): The credentials used for the gRPC
            connection. Can used to connect to other MinKNOW interfaces. Changing this
            will affect future calls to connect().
        host (string): The hostname of the machine the position is running on.

    Attributes on minknow_api.manager_pb2.FlowCellPosition (the protobuf message) will be
    available as attributes here as well.
    """

    def __init__(
        self,
        description: manager_pb2.FlowCellPosition,
        host: str,
        credentials: grpc.ChannelCredentials,
    ):
        self.host = host
        self.description = description
        self._device = None
        self.credentials = credentials

    def __repr__(self) -> str:
        return "FlowCellPosition({!r}, {{{!r}}})".format(self.host, self.description)

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.state)

    def __getattr__(self, name):
        info = self.description.DESCRIPTOR.fields_by_name.get(name)
        if not info:
            raise AttributeError(name)
        if info.message_type:
            # returning None for missing messages is more pythonic
            if not self.description.HasField(name):
                return None
        return getattr(self.description, name)

    @property
    def state(self) -> str:
        """The state of the position.

        One of "initialising", "running", "resetting", "hardware_removed", "hardware_error",
        "software_error" or "needs_association".
        """
        State = manager_pb2.FlowCellPosition.State
        return State.Name(self.description.state)[6:].lower()

    @property
    def protocol_state(self) -> str:
        """The simplified state of the protocol

        One of "no_protocol_state", "protocol_running", "protocol_finished_successfully",
        "protocol_finished_with_error", "workflow_running", "workflow_finished_successfully",
        "workflow_finished_with_error"
        """
        ProtocolState = manager_pb2.SimpleProtocolState
        return ProtocolState.Name(self.description.protocol_state).lower()

    @property
    def running(self) -> bool:
        """Whether the software for the position is running.

        Note that this is not directly equivalent to the "running" value of `state`: even when there
        are hardware errors, the software may still be running.
        """
        return self.description.HasField("rpc_ports")

    @property
    def device_type(self) -> str:
        device_type_value = self.description.device_type
        return minknow_api.device_pb2.GetDeviceInfoResponse.DeviceType.Name(
            device_type_value
        )

    def connect(
        self, credentials: Optional[grpc.ChannelCredentials] = None
    ) -> Connection:
        """Connect to the position.

        Only valid to do if `running` is True.

        Args:
            credentials: Override the credentials to be used for this particular
                connection.

        Returns:
            A connection to the RPC interface.
        """
        port = self.description.rpc_ports.secure
        if credentials is None:
            credentials = self.credentials

        if port == 0:
            raise RuntimeError(
                "Invalid port for connection to '%s': '%s'" % (self.description, port)
            )
        return minknow_api.Connection(
            host=self.host,
            port=port,
            credentials=credentials,
        )


class Basecaller(ServiceBase):
    """A connection to the basecalling gRPC interface.

    You should not normally construct this directly - use `Manager.basecaller` instead.
    The constructor arguments may change between minor releases.

    Args:
        host: The hostname to connect to.
        port: The port to connect to.
        credentials: The credentials to use for the connection.

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

    def __init__(self, host: str, port: int, credentials: grpc.ChannelCredentials):
        super(Basecaller, self).__init__(
            minknow_api.basecaller_service.Basecaller,
            host=host,
            port=port,
            credentials=credentials,
        )

    def __repr__(self) -> str:
        return "Basecaller({!r}, {!r})".format(self.host, self.port)


class Manager(ServiceBase):
    """A connection to the manager gRPC interface.

    Args:
        host: The host MinKNOW is running on.
        port: The port to connect to.
        developer_api_token: A token obtained from the MinKNOW UI. Will be used to
            authorise to MinKNOW if provided. It is recommended to use
            `client_certificate_chain` and `client_private_key` instead. Note: if
            `credentials` is provided, this parameter is ignored.
        credentials: gRPC credentials to use. If None, then
            minknow_api.grpc_credentials() is called (using the other arguments) to
            obtain credentials.
        client_certificate_chain: The (PEM-encoded) certificate chain linking
            `client_private_key` to a certificate in ``conf/rpc-client-certs`` in
            the MinKNOW installation directory. Note: if `credentials` is provided,
            this parameter is ignored.
        client_private_key: The (PEM-encoded) private key for the first certificate
            in `client_cert_chain`. Note: if `credentials` is provided, this
            parameter is ignored.
        ca_certificate: The (PEM-encoded) root CA certificate. Note: if `credentials`
            is provided, this parameter is ignored.

    Attributes:
        bream_version (str): The version of Bream that is installed.
        config_version (str): The version of ont-configuration (Wanda) that is installed.
        channel (grpc.Channel): The gRPC channel used for communication.
        core_version (str): The running version of MinKNOW Core.
        core_version_components (tuple): A tuple of three integers describing the major, minor and
            patch parts of the core version. Useful for version comparisons.
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
        host: str = "127.0.0.1",
        port: Optional[int] = None,
        developer_api_token: Optional[str] = None,
        credentials: Optional[grpc.ChannelCredentials] = None,
        client_certificate_chain: Optional[bytes] = None,
        client_private_key: Optional[bytes] = None,
        ca_certificate: Optional[bytes] = None,
        environ: Union[Dict[str, str], os._Environ] = os.environ,
    ):
        if port is None:
            if (
                client_certificate_chain is not None
                or "MINKNOW_API_CLIENT_CERTIFICATE_CHAIN" in environ
            ):
                # client certificates won't work on 9502
                port = 9501
            else:
                # pre-5.5 versions of MinKNOW Core don't listen on 9501
                port = 9502

        if credentials is not None:
            if developer_api_token is not None:
                warnings.warn(
                    "`developer_api_token` ignored as `credentials` was provided"
                )
            if client_certificate_chain is not None or client_private_key is not None:
                warnings.warn(
                    "`client_certificate_chain` and `client_private_key` ignored as `credentials` was provided"
                )
            if ca_certificate is not None:
                warnings.warn("`ca_certificate` ignored as `credentials` was provided")

        if credentials is None:
            credentials = minknow_api.grpc_credentials(
                manager_port=port,
                developer_api_token=developer_api_token,
                host=host,
                client_certificate_chain=client_certificate_chain,
                client_private_key=client_private_key,
                ca_certificate=ca_certificate,
                _warning_stacklevel=1,
                environ=environ,
            )
        super(Manager, self).__init__(
            minknow_api.manager_service.ManagerService,
            host=host,
            port=port,
            credentials=credentials,  # saved as self.credentials
        )

        self.analysis_workflows = (
            minknow_api.analysis_workflows_service.AnalysisWorkflowsService(
                self.channel
            )
        )

        version_info = self.rpc.get_version_info()
        self.bream_version = version_info.bream
        self.config_version = version_info.protocol_configuration
        self.core_version = version_info.minknow.full
        self.core_version_components = (
            version_info.minknow.major,
            version_info.minknow.minor,
            version_info.minknow.patch,
        )
        self.guppy_version = version_info.basecaller_connected_version
        self.version = version_info.distribution_version
        DistributionStatus = (
            minknow_api.instance_pb2.GetVersionInfoResponse.DistributionStatus
        )
        self.version_status = DistributionStatus.Name(
            version_info.distribution_status
        ).lower()

    def __repr__(self) -> str:
        return "Manager({!r}, {!r})".format(self.host, self.port)

    def hardware_check(self) -> minknow_api.hardware_check_service.HardwareCheckService:
        """
        Find the hardware check service running for this manager.

        Returns:
            HardwareCheck: The gRPC service for the manager level hardware check.
        """
        return minknow_api.hardware_check_service.HardwareCheckService(self.channel)

    def keystore(self) -> minknow_api.keystore_service.KeyStoreService:
        """
        Find the keystore service running for this manager.

        Returns:
            KeyStore: The gRPC service for the manager level keystore.
        """
        return minknow_api.keystore_service.KeyStoreService(self.channel)

    def log(self) -> minknow_api.log_service.LogService:
        """
        Find the log service running for this manager.

        Returns:
            LogService: The gRPC service for the manager level log service.
        """
        return minknow_api.log_service.LogService(self.channel)

    def basecaller(self, timeout: float = DEFAULT_TIMEOUT) -> Optional[Basecaller]:
        """Connect to the basecalling interface.

        Args:
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            The wrapper for the Basecaller service, or None if the connection couldn't
            be made.
        """
        bc_api = self.rpc.basecaller_api(
            minknow_api.manager_service.BasecallerApiRequest(), timeout=timeout
        )
        if bc_api.secure == 0:
            return None
        return Basecaller(
            host=self.host, port=bc_api.secure, credentials=self.credentials
        )

    def protocols(self) -> minknow_api.v2.protocols_service.ProtocolsService:
        """
        Get the v2 Protocols service running on this manager.

        Returns:
            The wrapper for the Protocols gRPC service.
        """
        return minknow_api.v2.protocols_service.ProtocolsService(self.channel)

    def presets(self) -> minknow_api.ui.sequencing_run.presets_service.PresetsService:
        """
        Find the presets service running for this manager.

        Returns:
            PresetsService: The gRPC service for the manager level presets service.
        """
        return minknow_api.ui.sequencing_run.presets_service.PresetsService(
            self.channel
        )

    def connect_to(self, position: str) -> Connection:
        """Connects to a position on the host

        Args:
            position: The name of the position to connect to

        Returns:
            The Connection object associated with the named position

        Raises:
            RuntimeError if the position cannot be found
        """
        for conn in self.flow_cell_positions():
            if conn.name == position:
                return conn.connect()
        return RuntimeError(f"Cannot find position with name '{position}'")

    def create_directory(
        self, name: str, parent_path: str = "", timeout: float = DEFAULT_TIMEOUT
    ) -> str:
        """Create a directory on the host.

        Args:
            name: The name of the directory to be created.
            parent_path: The name of the directory to be created.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            The name of the created directory.
        """
        request = minknow_api.manager_service.CreateDirectoryRequest(
            parent_path=parent_path, name=name
        )
        return self.rpc.create_directory(request, _timeout=timeout).path

    def guppy_port(self, timeout: float = DEFAULT_TIMEOUT) -> int:
        """Get the port that Guppy is listening on.

        This can be used to directly connect to the Guppy server using the pyguppy client.

        Args:
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            The port Guppy is listening on
        """
        return self.rpc.get_guppy_info(_timeout=timeout).port

    def get_guppy_connection_info(
        self, timeout: float = DEFAULT_TIMEOUT
    ) -> GuppyConnectionInfo:
        """Get the port and ipc_path that Guppy is listening to.

        This can be used to directly connect to the Guppy server using the pyguppy client.

        Guppy only listens on either a port or the ipc path. The default changes based on OS.
        Calling code should change its behaviour based on which tuple field is not None.

        Args:
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            Either the port or path guppy is listening on.
        """
        guppy_info = self.rpc.get_guppy_info(_timeout=timeout)
        port = None
        ipc_path = None
        if guppy_info.port != 0:
            port = guppy_info.port
        else:
            ipc_path = guppy_info.ipc_path
        return GuppyConnectionInfo(port, ipc_path)

    def describe_host(
        self, timeout: float = DEFAULT_TIMEOUT
    ) -> minknow_api.manager_service.DescribeHostResponse:
        """Get information about the machine running MinKNOW.

        Args:
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Returns:
            minknow_api.manager_service.DescribeHostResponse: The information about the host.
        """
        return self.rpc.describe_host(_timeout=timeout)

    def reset_position(
        self, position: str, force: bool = False, timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        """Reset a flow cell position.

        Args:
            position: The name of the position to reset.
            force: Restart the position even if it seems to be running fine.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        self.reset_positions([position], force=force, timeout=timeout)

    def reset_positions(
        self,
        positions: Sequence[str],
        force: bool = False,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Reset flow-cell positions

        Args:
            positions: The names of the positions to reset.
            force: Restart the position even if it seems to be running fine.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        self.rpc.reset_position(_timeout=timeout, positions=positions, force=force)

    def flow_cell_positions(
        self, timeout: float = DEFAULT_TIMEOUT
    ) -> Iterator[FlowCellPosition]:
        """Get a list of flow cell positions.

        Args:
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.

        Yields:
            A flow cell position. Ordering is not guaranteed.
        """
        call = self.rpc.flow_cell_positions(_timeout=timeout)
        # avoid holding open the call for longer than necessary by consuming all the results up
        # front
        messages = [msg for msg in call]
        for msg in messages:
            for position in msg.positions:
                yield FlowCellPosition(
                    position,
                    host=self.host,
                    credentials=self.credentials,
                )

    def add_simulated_device(
        self,
        name: str,
        type: manager_pb2.SimulatedDeviceType,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Dynamically create a simulated device

        Args:
            name: name of simulated device to create. Should not exist already.
                The format depends on the type of device being created,
                For MinIONs and MinION-mk1Cs, "MS" followed by five digits, eg: "MS12345".
                For GridIONs, "GS" followed by five digits, eg: "GS12345".
                PromethIONs position-names have no format restriction
            type: Type of device to create.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        self.rpc.add_simulated_device(_timeout=timeout, name=name, type=type)

    def remove_simulated_device(
        self, name: str, timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        """Dynamically remove a simulated device

        Args:
            name: name of device to remove. It should exist and be simulated.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        self.rpc.remove_simulated_device(_timeout=timeout, name=name)

    def get_alignment_reference_information(
        self, path: str, timeout: float = DEFAULT_TIMEOUT
    ) -> manager_pb2.GetAlignmentReferenceInformationResponse:
        """Query alignment reference information from a file path.

        Args:
            path: Path of the alignment reference file.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        return self.rpc.get_alignment_reference_information(_timeout=timeout, path=path)

    def create_developer_api_token(
        self,
        name: str,
        expiry: Optional[datetime.datetime] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> manager_pb2.CreateDeveloperApiTokenResponse:
        """Create a new developer api token, which expires at [expiry].

        DEPRECATED: use client certificates instead.

        Can not be invoked when using a developer token as authorisation method.

        Args:
            name: Readable name of the token.
            expiry: Expiry time of the token.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        warnings.warn(
            "Developer API tokens are deprecated: use client certificates instead",
            DeprecationWarning,
        )

        kwargs = {}
        if expiry:
            ts = timestamp_pb2.Timestamp()
            ts.FromDatetime(dt=expiry)
            kwargs["expiry"] = ts
        return self.rpc.create_developer_api_token(
            _timeout=timeout, name=name, **kwargs
        )

    def revoke_developer_api_token(self, id, timeout=DEFAULT_TIMEOUT) -> None:
        """Revoke an existing developer api tokens.

        DEPRECATED: use client certificates instead.

        Args:
            id: The identification of the token (available from list_developer_api_tokens).
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        warnings.warn(
            "Developer API tokens are deprecated: use client certificates instead",
            DeprecationWarning,
        )

        self.rpc.revoke_developer_api_token(id=id, _timeout=timeout)

    def list_developer_api_tokens(
        self, timeout=DEFAULT_TIMEOUT
    ) -> manager_pb2.ListDeveloperApiTokensResponse:
        """List existing developer api tokens.

        DEPRECATED: use client certificates instead.

        Args:
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        warnings.warn(
            "Developer API tokens are deprecated: use client certificates instead",
            DeprecationWarning,
        )

        return self.rpc.list_developer_api_tokens(_timeout=timeout)

    def find_protocols(
        self,
        experiment_type: manager_pb2.ExperimentType,
        flow_cell_product_code: Optional[str] = None,
        sequencing_kit: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> manager_pb2.FindProtocolsResponse:
        """List existing developer api tokens.

        Args:
            experiment_type: Type of experiment to search for.
            flow_cell_product_code: Find only protocols compatible with the given flow cell code.
                Default 'None' will return protocols matching any (including protocols without a flow_cell_product_code).
            sequencing_kit: Find only protocols compatible with the given sequencing kit.
                Default 'None' will return protocols matching any (including protocols without a sequencing_kit).
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        kwargs = {}
        if flow_cell_product_code is not None:
            kwargs["flow_cell_product_code"] = flow_cell_product_code
        if sequencing_kit is not None:
            kwargs["sequencing_kit"] = sequencing_kit

        return self.rpc.find_protocols(experiment_type=experiment_type, **kwargs)

    def get_sequencing_kits(
        self,
        flow_cell_product_code: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> manager_pb2.GetSequencingKitsResponse:
        """List all known sequencing kits.

        The intention is to provide a list of sequencing kits for a user to select from, plus extra
        information that can be used to filter that list.

        Args:
            flow_cell_product_code (str, optional): The product code of the flow cell that will be used for sequencing.

                Only kits compatible with this flow cell type will be returned (currently, this means that
                there is at least one (sequencing or control) protocol that is compatible with both the kit
                and this flow cell product code).

                This may also affect the returned information about the kit. For example, if it isn't
                possible to basecall on the flow cell, none of the kits will claim to be barcoding capable
                (or compatible with any barcoding expansion kits).
        """
        kwargs = {}
        if flow_cell_product_code is not None:
            kwargs["flow_cell_product_code"] = flow_cell_product_code

        return self.rpc.get_sequencing_kits(**kwargs)

    def list_settings_for_protocol(
        self,
        flow_cell_connector: device_pb2.FlowCellConnectorType,
        identifier: Optional[str] = None,
        components: Optional[protocol_settings_pb2.ProtocolIdentifierComponents] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> manager_pb2.ListSettingsForProtocolResponse:
        """List existing developer api tokens.

        Args:
            identifier (str, optional): specify the protocol with a string containing all the protocol's identifying components, eg:
                "sequencing/sequencing_MIN106_DNA:FLO-MIN106:SQK-RPB004"
            components (minknow_api.protocol_settings_pb2.ProtocolIdentifierComponents, optional): specify the protocol providing the identifying components individually. All components are optional, if more
                than one protocol matches given strings, information about the first will be returned.
            flow_cell_connector (minknow_api.device_pb2.FlowCellConnectorType): The flow-cell connector type identifies the type of hardware and is used
                to identify the correct protocol.
                The flow-cell connector types applicable to the device are listed by
                the get_flow_cell_types rpc in this service and the get_device_state rpc
                in the device service.
            timeout: The maximum time to wait for the call to complete. Should
                usually be left at the default.
        """
        kwargs = {}
        if flow_cell_connector is not None:
            kwargs["flow_cell_connector"] = flow_cell_connector
        if identifier is not None:
            kwargs["identifier"] = identifier
        if components is not None:
            kwargs["components"] = components

        return self.rpc.list_settings_for_protocol(**kwargs)

    def find_basecall_configurations(
        self,
        flow_cell_product_code: Optional[str] = None,
        sequencing_kit: Optional[str] = None,
        sampling_rate: Optional[int] = None,
        include_remote_configurations: bool = False,
        include_outdated: bool = True,
    ) -> Sequence[manager_pb2.FindBasecallConfigurationsResponse.BasecallConfiguration]:
        kwargs = {}
        if flow_cell_product_code is not None:
            kwargs["flow_cell_product_code"] = flow_cell_product_code
        if sequencing_kit is not None:
            kwargs["sequencing_kit"] = sequencing_kit
        if sampling_rate is not None:
            kwargs["sampling_rate"] = sampling_rate

        return self.rpc.find_basecall_configurations(
            include_remote_configurations=include_remote_configurations,
            include_outdated=include_outdated,
            **kwargs,
        ).configurations
