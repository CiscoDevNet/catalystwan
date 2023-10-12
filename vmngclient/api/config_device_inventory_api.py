from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.endpoints.configuration_device_inventory import (
    ConfigurationDeviceInventory,
    DeviceUnlockPayload,
    DeviceUnlockResponse,
    UnlockDeviceDetail,
)


class ConfigurationDeviceInventoryAPI:
    def __init__(self, session: vManageSession):
        self.session = session
        self.endpoint = ConfigurationDeviceInventory(session)

    def unlock(self, device_uuid: str, device_type: str, device_details: list) -> DeviceUnlockResponse:
        """
        Unlocks device from config-group
        """
        devices = []
        for device_detail in device_details:
            unlock_device_detail = UnlockDeviceDetail(
                deviceId=device_detail["deviceId"], deviceIP=device_detail["deviceIP"]
            )
            devices.append(unlock_device_detail)

        payload = DeviceUnlockPayload(deviceType=device_type, devices=devices)

        return self.endpoint.unlock(device_uuid=device_uuid, payload=payload)