# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.api.task_status_api import Task
from catalystwan.endpoints.configuration_device_inventory import (
    ConfigType,
    ConfigurationDeviceInventory,
    DeviceUnlockPayload,
    GenerateBoostrapConfigurationQueryParams,
    UnlockDeviceDetail,
)
from catalystwan.models.device_inventory import BoostrapConfigurationDetails


class ConfigurationDeviceInventoryAPI:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = ConfigurationDeviceInventory(session)

    def unlock(self, device_uuid: str, device_type: str, device_details: list) -> Task:
        """
        Unlocks device from config-group
        """
        devices = []
        for device_detail in device_details:
            unlock_device_detail = UnlockDeviceDetail(
                device_id=device_detail["deviceId"], device_ip=device_detail["deviceIP"]
            )
            devices.append(unlock_device_detail)

        payload = DeviceUnlockPayload(device_type=device_type, devices=devices)

        task_id = self.endpoint.unlock(device_uuid=device_uuid, payload=payload).parentTaskId
        return Task(self.session, task_id=task_id)

    def generate_bootstrap_cfg(
        self,
        device_uuid: UUID,
        configtype: ConfigType = "cloudinit",
        incl_def_root_cert: bool = False,
        version: str = "v1",
    ) -> BoostrapConfigurationDetails:
        """
        Returns handy model of generated bootstrap config
        """
        params = GenerateBoostrapConfigurationQueryParams(
            configtype=configtype, incl_def_root_cert=incl_def_root_cert, version=version
        )
        reponse = self.endpoint.generate_bootstrap_configuration(uuid=device_uuid, params=params)

        return BoostrapConfigurationDetails(bootstrap_config=reponse.bootstrap_config)
