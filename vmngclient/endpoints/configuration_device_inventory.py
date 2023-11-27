# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, delete, post, versions
from vmngclient.utils.personality import Personality


class UnlockDeviceDetail(BaseModel):
    device_id: str = Field(alias="deviceId")
    device_ip: str = Field(alias="deviceIP")


class DeviceUnlockPayload(BaseModel):
    device_type: str = Field(alias="deviceType")
    devices: List[UnlockDeviceDetail]


class DeviceUnlockResponse(BaseModel):
    parentTaskId: str


class Protocol(str, Enum):
    DTLS = "DTLS"
    TLS = "TLS"


class DeviceCreationPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_ip: str = Field(alias="deviceIP")
    generate_csr: bool = Field(alias="generateCSR")
    password: str
    personality: Personality
    port: Optional[str]
    protocol: Protocol = Protocol.DTLS
    username: str


class DeviceDeletionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    local_delete_from_db: bool = Field(alias="localDeleteFromDB")
    id: str


class ConfigurationDeviceInventory(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/system/device/{device_uuid}/unlock")
    def unlock(self, device_uuid: str, payload: DeviceUnlockPayload) -> DeviceUnlockResponse:
        ...

    @post("/system/device")
    def create_device(self, payload: DeviceCreationPayload) -> None:
        ...

    @delete("/system/device/{uuid}")
    def delete_device(self, uuid: str) -> DeviceDeletionResponse:
        ...
