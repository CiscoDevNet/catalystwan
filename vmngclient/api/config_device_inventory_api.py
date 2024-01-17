from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.api.task_status_api import Task
from vmngclient.endpoints.configuration_device_inventory import (
    ConfigType,
    ConfigurationDeviceInventory,
    DeviceUnlockPayload,
    GenerateBoostrapConfigurationQueryParams,
    UnlockDeviceDetail,
)
from vmngclient.models.device_inventory import BoostrapConfigurationDetails


class ConfigurationDeviceInventoryAPI:
    def __init__(self, session: vManageSession):
        self.session = session
        self.endpoint = ConfigurationDeviceInventory(session)

    def unlock(self, device_uuid: str, device_type: str, device_details: list) -> Task:
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

        task_id = self.endpoint.unlock(device_uuid=device_uuid, payload=payload).parentTaskId
        return Task(self.session, task_id=task_id)

    def generate_bootstrap_cfg(
        self,
        device_uuid: str,
        configtype: ConfigType = ConfigType.CLOUDINIT,
        incl_def_root_cert: bool = False,
        version: str = "v1",
    ) -> BoostrapConfigurationDetails:
        """
        Returns handy model of generated bootstrap config
        """
        params = GenerateBoostrapConfigurationQueryParams(
            configtype=configtype, incl_def_root_cert=incl_def_root_cert, version=version
        )
        bootstrap_cfg_string = self.endpoint.generate_bootstrap_configuration(uuid=device_uuid, params=params)

        return BoostrapConfigurationDetails(bootstrapConfig=bootstrap_cfg_string.bootstrap_config)
