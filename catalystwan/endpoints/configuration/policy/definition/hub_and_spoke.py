# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.hub_and_spoke import (
    HubAndSpokePolicy,
    HubAndSpokePolicyEditPayload,
    HubAndSpokePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


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
