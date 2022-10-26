import minknow_api.manager
import os
from pathlib import Path
import typing


class ProtocolPaths(typing.NamedTuple):
    output: Path
    input_fastq: typing.Optional[Path]
    input_fast5: typing.Optional[Path]
    input_bam: typing.Optional[Path]
    sample_sheet: typing.Optional[Path]


class PostProcessingProtocolConnection(object):
    """A connection to a MinKNOW basecaller via RPC.

    Basecaller service is available as a property 'basecaller' on the PostProcessingProtocolConnection
    object.
    """

    def __init__(
        self,
        protocol_id=None,
        host="127.0.0.1",
        port=None,
        credentials=None,
    ):
        if port is None:
            port = int(os.environ["MINKNOW_BASECALLER_RPC_PORT_SECURE"])

        if protocol_id is None:
            protocol_id = os.environ["POST_PROCESSING_PROTOCOL_ID"]
        self.id = protocol_id
        if not self.id:
            raise Exception("Invalid id specified for PostProcessingProtocolConnection")

        if credentials is None:
            credentials = minknow_api.grpc_credentials(host=host)
        self._basecaller = minknow_api.manager.Basecaller(
            port=port, credentials=credentials
        )
        self._protocol_directories = None
        self._protocol_id = None

    @property
    def basecaller(self):
        return self._basecaller

    @property
    def protocol_directories(self):
        if self._protocol_directories is None:
            info = None
            for resp in self.basecaller.rpc.get_info(id=self.id):
                info = resp.runs[0] if resp.runs else None

                if info:
                    break

            if not info:
                raise Exception(
                    "get_info failed to return information about protocol '%s" % self.id
                )

            if not info.HasField("start_post_processing_protocol_request"):
                raise Exception(
                    "get_info returned a protocol without a post processing protocol request"
                )

            def path_or_none(path: str) -> typing.Optional[Path]:
                if path:
                    return Path(path)
                return None

            start_request = info.start_post_processing_protocol_request
            self._protocol_directories = ProtocolPaths(
                input_fastq=path_or_none(start_request.input_fastq_directory),
                input_fast5=path_or_none(start_request.input_fast5_directory),
                input_bam=path_or_none(start_request.input_bam_directory),
                sample_sheet=path_or_none(start_request.sample_sheet_path),
                output=Path(start_request.output_directory),
            )

        return self._protocol_directories

    def set_progress(self, progress):
        if progress < 0 or progress > 1:
            raise Exception("Invalid `progress`, must be in range 0.0-1.0")

        self.basecaller.rpc.update_post_processing_protocol_progress(
            id=self.id, progress=progress
        )
