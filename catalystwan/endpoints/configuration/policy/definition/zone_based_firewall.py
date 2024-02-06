# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.definitions.zone_based_firewall import ZoneBasedFWPolicy
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ZoneBasedFWPolicyEditPayload(ZoneBasedFWPolicy, PolicyDefinitionId):
    pass


class ZoneBasedFWPolicyGetResponse(ZoneBasedFWPolicy, PolicyDefinitionGetResponse):
    pass


class ConfigurationPolicyZoneBasedFirewallDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/zonebasedfw")
    def create_policy_definition(self, payload: ZoneBasedFWPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/zonebasedfw/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/zonebasedfw/multiple/{id}
        ...

    @put("/template/policy/definition/zonebasedfw/{id}")
    def edit_policy_definition(self, id: UUID, payload: ZoneBasedFWPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/zonebasedfw", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/zonebasedfw/{id}")
    def get_policy_definition(self, id: UUID) -> ZoneBasedFWPolicyGetResponse:
        ...

    @post("/template/policy/definition/zonebasedfw/preview")
    def preview_policy_definition(self, payload: ZoneBasedFWPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/zonebasedfw/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/zonebasedfw/bulk
        ...
