# mypy: disable-error-code="empty-body"
from typing import List

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, post, versions


class UnlockDeviceDetail(BaseModel):
    device_id: str = Field(alias="deviceId")
    device_ip: str = Field(alias="deviceIP")


class DeviceUnlockPayload(BaseModel):
    device_type: str = Field(alias="deviceType")
    devices: List[UnlockDeviceDetail]


class DeviceUnlockResponse(BaseModel):
    parentTaskId: str


class ConfigurationDeviceInventory(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/system/device/{device_uuid}/unlock")
    def unlock(self, device_uuid: str, payload: DeviceUnlockPayload) -> DeviceUnlockResponse:
        ...
