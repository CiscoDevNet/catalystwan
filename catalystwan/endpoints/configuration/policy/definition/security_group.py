# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.security_group import (
    SecurityGroup,
    SecurityGroupEditPayload,
    SecurityGroupGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicySecurityGroupDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/securitygroup")
    def create_policy_definition(self, payload: SecurityGroup) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/securitygroup/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/securitygroup/multiple/{id}
        ...

    @put("/template/policy/definition/securitygroup/{id}")
    def edit_policy_definition(self, id: UUID, payload: SecurityGroupEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/securitygroup", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/securitygroup/{id}")
    def get_policy_definition(self, id: UUID) -> SecurityGroupGetResponse:
        ...

    @post("/template/policy/definition/securitygroup/preview")
    def preview_policy_definition(self, payload: SecurityGroup) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/securitygroup/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/securitygroup/bulk
        ...
