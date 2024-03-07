# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.definitions.traffic_data import TrafficDataPolicy
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class TrafficDataPolicyEditPayload(TrafficDataPolicy, PolicyDefinitionId):
    pass


class TrafficDataPolicyGetResponse(TrafficDataPolicy, PolicyDefinitionGetResponse):
    pass


class ConfigurationPolicyDataDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/data")
    def create_policy_definition(self, payload: TrafficDataPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/data/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/data/multiple/{id}
        ...

    @put("/template/policy/definition/data/{id}")
    def edit_policy_definition(self, id: UUID, payload: TrafficDataPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/data", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/data/{id}")
    def get_policy_definition(self, id: UUID) -> TrafficDataPolicyGetResponse:
        ...

    @post("/template/policy/definition/data/preview")
    def preview_policy_definition(self, payload: TrafficDataPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/data/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/data/bulk
        ...
