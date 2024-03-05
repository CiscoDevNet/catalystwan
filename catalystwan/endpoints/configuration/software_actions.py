# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.typed_list import DataSequence


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


class SoftwareImageQuery(BaseModel):
    image_type: ImageType = Field(default=ImageType.SOFTWARE, alias="imageType")
    vnf_type: Optional[ImageType] = Field(default=None, alias="vnfType")


class RemoteServerProtocol(str, Enum):
    FTP = "FTP"
    HTTP = "HTTP"
    SCP = "SCP"


class RemoteServer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    image_location_prefix: str = Field(
        default="/", serialization_alias="imageLocationPrefix", validation_alias="imageLocationPrefix"
    )
    remote_server_name: str = Field(serialization_alias="remoteServerName", validation_alias="remoteServerName")
    remote_server_password: str = Field(
        serialization_alias="remoteServerPassword", validation_alias="remoteServerPassword"
    )
    remote_server_port: int = Field(
        default=21, serialization_alias="remoteServerPort", validation_alias="remoteServerPort"
    )
    remote_server_protocol: RemoteServerProtocol = Field(
        default=RemoteServerProtocol.FTP,
        serialization_alias="remoteServerProtocol",
        validation_alias="remoteServerProtocol",
    )
    remote_server_url: str = Field(serialization_alias="remoteServerUrl", validation_alias="remoteServerUrl")
    remote_server_user: str = Field(serialization_alias="remoteServerUser", validation_alias="remoteServerUser")
    remote_server_vpn: int = Field(
        ge=0, le=65527, serialization_alias="remoteServerVPN", validation_alias="remoteServerVPN"
    )


class RemoteServerInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    image_location_prefix: Optional[str] = Field(
        default=None, serialization_alias="imageLocationPrefix", validation_alias="imageLocationPrefix"
    )
    remote_server_id: Optional[str] = Field(
        default=None, serialization_alias="remoteServerId", validation_alias="remoteServerId"
    )
    remote_server_name: Optional[str] = Field(
        default=None, serialization_alias="remoteServerName", validation_alias="remoteServerName"
    )
    remote_server_port: Optional[int] = Field(
        default=None, serialization_alias="remoteServerPort", validation_alias="remoteServerPort"
    )
    remote_server_protocol: Optional[RemoteServerProtocol] = Field(
        default=None, serialization_alias="remoteServerProtocol", validation_alias="remoteServerProtocol"
    )
    remote_server_url: Optional[str] = Field(
        default=None, serialization_alias="remoteServerUrl", validation_alias="remoteServerUrl"
    )
    remote_server_user: Optional[str] = Field(
        default=None, serialization_alias="remoteServerUser", validation_alias="remoteServerUser"
    )
    remote_server_vpn: Optional[int] = Field(
        default=None, serialization_alias="remoteServerVPN", validation_alias="remoteServerVPN"
    )
    updated_on: Optional[int] = Field(default=None, serialization_alias="updatedOn", validation_alias="updatedOn")


class SoftwareRemoteServer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    filename: str = Field(default=None, serialization_alias="fileName", validation_alias="fileName")
    remote_server_id: str = Field(default=None, serialization_alias="remoteServerId", validation_alias="remoteServerId")
    smu_defect_id: Optional[str] = Field(
        default=None, serialization_alias="smuDefectId", validation_alias="smuDefectId"
    )
    smu_type: Optional[str] = Field(default=None, serialization_alias="smuType", validation_alias="smuType")


class SoftwareImageDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    arch: Optional[str] = Field(default=None)
    available_files: Optional[str] = Field(
        default=None, serialization_alias="availableFiles", validation_alias="availableFiles"
    )
    available_smu_versions: Optional[Union[List[str], str]] = Field(
        default=None, serialization_alias="availableSmuVersions", validation_alias="availableSmuVersions"
    )
    checksum_map: Optional[str] = Field(default=None, serialization_alias="checksumMap", validation_alias="checksumMap")
    controller_version_name: Optional[str] = Field(
        default=None, serialization_alias="controllerVersionName", validation_alias="controllerVersionName"
    )
    cw_version: Optional[str] = Field(default=None, serialization_alias="cwVersion", validation_alias="cwVersion")
    file_name_map: Optional[str] = Field(
        default=None, serialization_alias="fileNameMap", validation_alias="fileNameMap"
    )
    image_properties_json: Optional[str] = Field(
        default=None, serialization_alias="imagePropertiesJson", validation_alias="imagePropertiesJson"
    )
    image_type: Optional[str] = Field(default=None, serialization_alias="imageType", validation_alias="imageType")
    network_function_type: Optional[str] = Field(
        default=None, serialization_alias="networkFunctionType", validation_alias="networkFunctionType"
    )
    platform_family: Optional[List[str]] = Field(
        default=None, serialization_alias="platformFamily", validation_alias="platformFamily"
    )
    rid: Optional[int] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")
    smu_compatible_version: Optional[str] = Field(
        default=None, serialization_alias="smuCompatibleVersion", validation_alias="smuCompatibleVersion"
    )
    system_properties_xml: Optional[str] = Field(
        default=None, serialization_alias="systemPropertiesXml", validation_alias="systemPropertiesXml"
    )
    updated_on: Optional[int] = Field(default=None, serialization_alias="updatedOn", validation_alias="updatedOn")
    vendor: Optional[str] = Field(default=None)
    version_id: Optional[str] = Field(default=None, serialization_alias="versionId", validation_alias="versionId")
    version_id_map: Optional[str] = Field(
        default=None, serialization_alias="versionIdMap", validation_alias="versionIdMap"
    )
    version_name: Optional[str] = Field(default=None, serialization_alias="versionName", validation_alias="versionName")
    version_type: Optional[str] = Field(default=None, serialization_alias="versionType", validation_alias="versionType")
    version_type_name: Optional[str] = Field(
        default=None, serialization_alias="versionTypeName", validation_alias="versionTypeName"
    )
    version_url: Optional[str] = Field(default=None, serialization_alias="versionURL", validation_alias="versionURL")
    vnf_properties_json: Optional[str] = Field(
        default=None, serialization_alias="vnfPropertiesJson", validation_alias="vnfPropertiesJson"
    )
    remote_server_id: str = Field(default=None, serialization_alias="remoteServerId", validation_alias="remoteServerId")


class ConfigurationSoftwareActions(APIEndpoints):
    @get("/device/action/remote-server", "data")
    def get_list_of_remote_servers(self) -> DataSequence[RemoteServerInfo]:
        ...

    @post("/device/action/remote-server")
    def add_new_remote_server(self, payload: RemoteServer) -> None:
        ...

    @get("/device/action/remote-server/{id}")
    def get_remote_server(self, id: UUID) -> RemoteServerInfo:
        ...

    @put("/device/action/remote-server/{id}")
    def update_remote_server(self, id: UUID, payload: SoftwareRemoteServer) -> None:
        ...

    @delete("/device/action/remote-server/{id}")
    def remove_remote_server(self, id: UUID) -> None:
        ...

    @get("/device/action/software", "data")
    def get_software_images(self) -> DataSequence[SoftwareImageDetails]:
        ...

    @post("/device/action/software")
    def upload_software_from_remote_server(self, payload: SoftwareRemoteServer) -> None:
        ...

    @delete("/device/action/software/{version_id}")
    def delete_software_from_software_repository(self, version_id: UUID) -> None:
        ...

    @get("/device/action/software/images", "data")
    def get_list_of_all_images(self, params: SoftwareImageQuery) -> DataSequence[SoftwareImageDetails]:
        ...
