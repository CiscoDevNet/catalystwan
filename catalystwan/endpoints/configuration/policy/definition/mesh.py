# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.definitions.mesh import MeshPolicy
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class MeshPolicyEditPayload(MeshPolicy, PolicyDefinitionId):
    pass


class MeshPolicyGetResponse(MeshPolicy, PolicyDefinitionGetResponse):
    pass


class ConfigurationPolicyMeshDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/mesh")
    def create_policy_definition(self, payload: MeshPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/mesh/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/mesh/multiple/{id}
        ...

    @put("/template/policy/definition/mesh/{id}")
    def edit_policy_definition(self, id: UUID, payload: MeshPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/mesh", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/mesh/{id}")
    def get_policy_definition(self, id: UUID) -> MeshPolicyGetResponse:
        ...

    @post("/template/policy/definition/mesh/preview")
    def preview_policy_definition(self, payload: MeshPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/mesh/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/mesh/bulk
        ...
