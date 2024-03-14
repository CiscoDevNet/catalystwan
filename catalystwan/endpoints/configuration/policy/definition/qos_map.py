# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.qos_map import QoSMapPolicy, QoSMapPolicyEditPayload, QoSMapPolicyGetResponse
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyQoSMapDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/qosmap")
    def create_policy_definition(self, payload: QoSMapPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/qosmap/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/qosmap/multiple/{id}
        ...

    @put("/template/policy/definition/qosmap/{id}")
    def edit_policy_definition(self, id: UUID, payload: QoSMapPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/qosmap", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/qosmap/{id}")
    def get_policy_definition(self, id: UUID) -> QoSMapPolicyGetResponse:
        ...

    @post("/template/policy/definition/qosmap/preview")
    def preview_policy_definition(self, payload: QoSMapPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/qosmap/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/qosmap/bulk
        ...
