# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.access_control_list_ipv6 import (
    AclIPv6Policy,
    AclIPv6PolicyEditPayload,
    AclIPv6PolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyAclIPv6Definition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/aclv6")
    def create_policy_definition(self, payload: AclIPv6Policy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/aclv6/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/aclv6/multiple/{id}
        ...

    @put("/template/policy/definition/aclv6/{id}")
    def edit_policy_definition(self, id: UUID, payload: AclIPv6PolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/aclv6", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/aclv6/{id}")
    def get_policy_definition(self, id: UUID) -> AclIPv6PolicyGetResponse:
        ...

    @post("/template/policy/definition/aclv6/preview")
    def preview_policy_definition(self, payload: AclIPv6Policy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/aclv6/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/aclv6/bulk
        ...
