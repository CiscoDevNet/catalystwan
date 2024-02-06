# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.definitions.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class HubAndSpokePolicyEditPayload(HubAndSpokePolicy, PolicyDefinitionId):
    pass


class HubAndSpokePolicyGetResponse(HubAndSpokePolicy, PolicyDefinitionGetResponse):
    pass


class ConfigurationPolicyHubAndSpokeDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/hubandspoke")
    def create_policy_definition(self, payload: HubAndSpokePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/hubandspoke/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/hubandspoke/multiple/{id}
        ...

    @put("/template/policy/definition/hubandspoke/{id}")
    def edit_policy_definition(self, id: UUID, payload: HubAndSpokePolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/hubandspoke", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/hubandspoke/{id}")
    def get_policy_definition(self, id: UUID) -> HubAndSpokePolicyGetResponse:
        ...

    @post("/template/policy/definition/hubandspoke/preview")
    def preview_policy_definition(self, payload: HubAndSpokePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/hubandspoke/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/hubandspoke/bulk
        ...
