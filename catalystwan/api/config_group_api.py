# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.endpoints.configuration_group import (
    ConfigGroupAssociatePayload,
    ConfigGroupCreationPayload,
    ConfigGroupCreationResponse,
    ConfigGroupDeployPayload,
    ConfigGroupDeployResponse,
    ConfigGroupDisassociateResponse,
    ConfigGroupEditPayload,
    ConfigGroupEditResponse,
    ConfigGroupResponsePayload,
    ConfigGroupVariablesCreatePayload,
    ConfigGroupVariablesCreateResponse,
    ConfigGroupVariablesEditPayload,
    ConfigurationGroup,
    DeviceId,
    ProfileId,
    Solution,
)


class ConfigGroupAPI:
    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = ConfigurationGroup(session)

    def associate(self, cg_id: str, device_ids: list) -> None:
        """
        Associates given config-group to specified list of devices
        """
        devices = []

        for device_id in device_ids:
            devices.append(DeviceId(id=device_id))

        payload = ConfigGroupAssociatePayload(devices=devices)

        self.endpoint.associate(config_group_id=cg_id, payload=payload)

    def create(self, name: str, description: str, solution: Solution, profile_ids: list) -> ConfigGroupCreationResponse:
        """
        Creates new config-group
        """
        profiles = []

        for profile_id in profile_ids:
            profiles.append(ProfileId(id=profile_id))
        cg_payload = ConfigGroupCreationPayload(
            name=name, description=description, solution=solution, profiles=profiles
        )

        return self.endpoint.create_config_group(cg_payload)

    def create_variables(
        self, cg_id: str, device_ids: list, suggestions: bool = True
    ) -> ConfigGroupVariablesCreateResponse:
        """
        Creates device specific variable data in given config-group
        """
        payload = ConfigGroupVariablesCreatePayload(deviceIds=device_ids, suggestions=suggestions)
        return self.endpoint.create_variables(config_group_id=cg_id, payload=payload)

    def delete(self, cg_id: str) -> None:
        """
        Deletes existing config-group with given ID
        """
        self.endpoint.delete_config_group(cg_id)

    def deploy(self, cg_id: str, device_ids: list) -> ConfigGroupDeployResponse:
        """
        Deploys specified config-group config to given list of devices
        """
        devices = []
        for device_id in device_ids:
            devices.append(DeviceId(id=device_id))

        payload = ConfigGroupDeployPayload(devices=devices)
        return self.endpoint.deploy(config_group_id=cg_id, payload=payload)

    def disassociate(self, cg_id: str, device_ids: list) -> ConfigGroupDisassociateResponse:
        """
        Disassociates given list of devices from the specified config-group
        """
        devices = []
        for device_id in device_ids:
            devices.append(DeviceId(id=device_id))

        payload = ConfigGroupAssociatePayload(devices=devices)
        return self.endpoint.disassociate(config_group_id=cg_id, payload=payload)

    def edit(
        self, cg_id: str, name: str, description: str, solution: Solution, profile_ids: list
    ) -> ConfigGroupEditResponse:
        """
        Modifies feature profiles in existing config-group
        """
        profiles = []

        for profile_id in profile_ids:
            profiles.append(ProfileId(id=profile_id))
        payload = ConfigGroupEditPayload(name=name, description=description, solution=solution, profiles=profiles)

        return self.endpoint.edit_config_group(config_group_id=cg_id, payload=payload)

    def get(self) -> ConfigGroupResponsePayload:
        """
        Gets list of existing config-groups
        """
        return self.endpoint.get()

    def update_variables(self, cg_id: str, solution: Solution, device_variables: list) -> None:
        """
        Updates device specific variable data in given config-group
        """
        payload = ConfigGroupVariablesEditPayload(solution=solution, devices=device_variables)

        self.endpoint.update_variables(config_group_id=cg_id, payload=payload)
