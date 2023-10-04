# mypy: disable-error-code="empty-body"
from typing import List

from pydantic import BaseModel

from vmngclient.endpoints import APIEndpoints, post, versions


class UnlockDeviceDetail(BaseModel):
    deviceId: str
    deviceIP: str


class DeviceUnlockPayload(BaseModel):
    deviceType: str
    devices: List[UnlockDeviceDetail]


class DeviceUnlockResponse(BaseModel):
    parentTaskId: str


class Device(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/system/device/{device_uuid}/unlock")
    def unlock(self, device_uuid: str, payload: DeviceUnlockPayload) -> DeviceUnlockResponse:
        ...
