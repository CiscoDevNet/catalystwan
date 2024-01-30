# mypy: disable-error-code="empty-body"
from uuid import UUID

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.definitions.device_access_ipv6 import DeviceAccessIPv6Policy
from vmngclient.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class DeviceAccessIPv6PolicyEditPayload(DeviceAccessIPv6Policy, PolicyDefinitionId):
    pass


class DeviceAccessIPv6PolicyInfo(DeviceAccessIPv6Policy, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class DeviceAccessIPv6PolicyGetResponse(DeviceAccessIPv6Policy, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyDeviceAccessIPv6Definition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/deviceaccesspolicyv6")
    def create_policy_definition(self, payload: DeviceAccessIPv6Policy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/deviceaccesspolicyv6/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/deviceaccesspolicyv6/multiple/{id}
        ...

    @put("/template/policy/definition/deviceaccesspolicyv6/{id}")
    def edit_policy_definition(
        self, id: UUID, payload: DeviceAccessIPv6PolicyEditPayload
    ) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/deviceaccesspolicyv6", "data")
    def get_definitions(self) -> DataSequence[DeviceAccessIPv6PolicyInfo]:
        ...

    @get("/template/policy/definition/deviceaccesspolicyv6/{id}")
    def get_policy_definition(self, id: UUID) -> DeviceAccessIPv6PolicyGetResponse:
        ...

    @post("/template/policy/definition/deviceaccesspolicyv6/preview")
    def preview_policy_definition(self, payload: DeviceAccessIPv6Policy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/deviceaccesspolicyv6/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/deviceaccesspolicyv6/bulk
        ...
