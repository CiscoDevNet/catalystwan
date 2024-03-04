# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.definitions.access_control_list import AclPolicy
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class AclPolicyEditPayload(AclPolicy, PolicyDefinitionId):
    pass


class AclPolicyGetResponse(AclPolicy, PolicyDefinitionGetResponse):
    pass


class ConfigurationPolicyAclDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/acl")
    def create_policy_definition(self, payload: AclPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/acl/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/acl/multiple/{id}
        ...

    @put("/template/policy/definition/acl/{id}")
    def edit_policy_definition(self, id: UUID, payload: AclPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/acl", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/acl/{id}")
    def get_policy_definition(self, id: UUID) -> AclPolicyGetResponse:
        ...

    @post("/template/policy/definition/acl/preview")
    def preview_policy_definition(self, payload: AclPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/acl/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/acl/bulk
        ...
