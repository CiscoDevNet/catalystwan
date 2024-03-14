# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.control import (
    ControlPolicy,
    ControlPolicyEditPayload,
    ControlPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyControlDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/control")
    def create_policy_definition(self, payload: ControlPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/control/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/control/multiple/{id}
        ...

    @put("/template/policy/definition/control/{id}")
    def edit_policy_definition(self, id: UUID, payload: ControlPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/control", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/control/{id}")
    def get_policy_definition(self, id: UUID) -> ControlPolicyGetResponse:
        ...

    @post("/template/policy/definition/control/preview")
    def preview_policy_definition(self, payload: ControlPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/control/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/control/bulk
        ...
