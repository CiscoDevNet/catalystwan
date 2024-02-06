# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.definitions.device_access import DeviceAccessPolicy
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class DeviceAccessPolicyEditPayload(DeviceAccessPolicy, PolicyDefinitionId):
    pass


class DeviceAccessPolicyGetResponse(DeviceAccessPolicy, PolicyDefinitionGetResponse):
    pass


class ConfigurationPolicyDeviceAccessDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/deviceaccesspolicy")
    def create_policy_definition(self, payload: DeviceAccessPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/deviceaccesspolicy/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/deviceaccesspolicy/multiple/{id}
        ...

    @put("/template/policy/definition/deviceaccesspolicy/{id}")
    def edit_policy_definition(self, id: UUID, payload: DeviceAccessPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/deviceaccesspolicy", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/deviceaccesspolicy/{id}")
    def get_policy_definition(self, id: UUID) -> DeviceAccessPolicyGetResponse:
        ...

    @post("/template/policy/definition/deviceaccesspolicy/preview")
    def preview_policy_definition(self, payload: DeviceAccessPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/deviceaccesspolicy/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/deviceaccesspolicy/bulk
        ...
