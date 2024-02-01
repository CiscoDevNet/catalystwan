# mypy: disable-error-code="empty-body"
from uuid import UUID

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.definitions.hub_and_spoke import HubAndSpokePolicy
from vmngclient.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class HubAndSpokePolicyEditPayload(HubAndSpokePolicy, PolicyDefinitionId):
    pass


class HubAndSpokePolicyInfo(PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class HubAndSpokePolicyGetResponse(HubAndSpokePolicy, PolicyDefinitionId, PolicyDefinitionInfo):
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
    def get_definitions(self) -> DataSequence[HubAndSpokePolicyInfo]:
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
