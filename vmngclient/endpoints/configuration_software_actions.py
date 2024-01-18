# mypy: disable-error-code="empty-body"

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.typed_list import DataSequence


class ImageType(str, Enum):
    SOFTWARE = "software"
    CONTAINER = "container"
    LXC = "lxc"
    VIRTUALMACHINE = "virtualmachine"
    VIRTUALMACHINE_DISKIMG = "virtualmachine-diskimg"
    VIRTUALMACHINE_SCAFFOLD = "virtualmachine-scaffold"
    UTDSIGNATURE = "utdsignature"
    UTDSIGNATUREIPS = "utdsignatureips"
    UTDSIGNATURECUSTOM = "utdsignaturecustom"
    WAAS = "waas"
    DOCKERTYPE = "dockertype"
    FIRMWARE = "firmware"
    RUMREPORT = "rumreport"
    LICENSEFILE = "licensefile"
    ACKFILE = "ackfile"
    NA = "na"


class RemoteServerProtocol(str, Enum):
    FTP = "FTP"
    HTTP = "HTTP"
    SCP = "SCP"


class RemoteServer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    remote_server_name: str = Field(alias="remoteServerName")
    remote_server_url: str = Field(alias="remoteServerUrl")
    remote_server_protocol: RemoteServerProtocol = Field(default=RemoteServerProtocol.FTP, alias="remoteServerProtocol")
    remote_server_port: int = Field(default=21, alias="remoteServerPort")
    remote_server_vpn: int = Field(ge=0, le=65527, alias="remoteServerVPN")
    remote_server_user: str = Field(alias="remoteServerUser")
    remote_server_password: str = Field(alias="remoteServerPassword")
    image_location_prefix: str = Field(default="/", alias="imageLocationPrefix")


class RemoteServerInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    image_location_prefix: Optional[str] = Field(default=None, alias="imageLocationPrefix")
    remote_server_protocol: Optional[RemoteServerProtocol] = Field(default=None, alias="remoteServerProtocol")
    remote_server_port: Optional[int] = Field(default=None, alias="remoteServerPort")
    remote_server_id: Optional[str] = Field(default=None, alias="remoteServerId")
    remote_server_name: Optional[str] = Field(default=None, alias="remoteServerName")
    remote_server_vpn: Optional[int] = Field(default=None, alias="remoteServerVPN")
    remote_server_url: Optional[str] = Field(default=None, alias="remoteServerUrl")
    updated_on: Optional[int] = Field(default=None, alias="updatedOn")
    remote_server_user: Optional[str] = Field(default=None, alias="remoteServerUser")


class AddSoftwarePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    remote_server_id: str = Field(default=None, alias="remoteServerId")
    filename: str = Field(default=None, alias="fileName")


class SoftwareImageDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    available_files: Optional[str] = Field(default=None, alias="availableFiles")
    version_type_name: Optional[str] = Field(default=None, alias="versionTypeName")
    version_name: Optional[str] = Field(default=None, alias="versionName")
    platform_family: Optional[List[str]] = Field(default=None, alias="platformFamily")
    smu_compatible_version: Optional[str] = Field(default=None, alias="smuCompatibleVersion")
    rid: Optional[int] = Field(default=None, alias="@rid")
    cw_version: Optional[str] = Field(default=None, alias="cwVersion")
    vnf_properties_json: Optional[str] = Field(default=None, alias="vnfPropertiesJson")
    image_properties_json: Optional[str] = Field(default=None, alias="imagePropertiesJson")
    vendor: Optional[str] = Field(default=None, alias="vendor")
    image_type: Optional[str] = Field(default=None, alias="imageType")
    version_type: Optional[str] = Field(default=None, alias="versionType")
    network_function_type: Optional[str] = Field(default=None, alias="networkFunctionType")
    updated_on: Optional[int] = Field(default=None, alias="updatedOn")
    checksum_map: Optional[str] = Field(default=None, alias="checksumMap")
    version_id_map: Optional[str] = Field(default=None, alias="versionIdMap")
    version_id: Optional[str] = Field(default=None, alias="versionId")
    system_properties_xml: Optional[str] = Field(default=None, alias="systemPropertiesXml")
    available_smu_versions: Optional[Union[List[str], str]] = Field(default=None, alias="availableSmuVersions")
    controller_version_name: Optional[str] = Field(default=None, alias="controllerVersionName")
    file_name_map: Optional[str] = Field(default=None, alias="fileNameMap")
    arch: Optional[str] = Field(default=None, alias="arch")
    version_url: Optional[str] = Field(default=None, alias="versionURL")


class SoftwareRemoteServer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    remote_server_id: str = Field(alias="remoteServerId")
    filename: str = Field(alias="fileName")


class ConfigurationSoftwareActions(APIEndpoints):
    @get("/device/action/remote-server", "data")
    def get_list_of_remote_servers(self) -> DataSequence[RemoteServerInfo]:
        ...

    @post("/device/action/remote-server")
    def add_new_remote_server(self, payload: RemoteServer) -> None:
        ...

    @get("/device/action/remote-server/{id}", "data")
    def get_remote_server(self, id: str) -> RemoteServerInfo:
        ...

    @put("/device/action/remote-server/{id}")
    def update_remote_server(self, id: str) -> None:
        ...

    @delete("/device/action/remote-server/{id}")
    def remove_remote_server(self, id: str) -> None:
        ...

    @get("/device/action/software", "data")
    def get_software_images(self) -> DataSequence[SoftwareImageDetails]:
        ...

    @post("/device/action/software")
    def add_new_software_from_remote_server(self, payload: SoftwareRemoteServer) -> None:
        ...

    @delete("/device/action/software/{id}")
    def delete_software_from_software_repository(self, id: str) -> None:
        ...

    @get("/device/action/software/images?imageType={image_type}", "data")
    def get_list_of_all_images(self, image_type: str = ImageType.SOFTWARE) -> DataSequence[SoftwareImageDetails]:
        ...
