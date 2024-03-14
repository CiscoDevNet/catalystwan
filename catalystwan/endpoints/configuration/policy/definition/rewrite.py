# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.rewrite import (
    RewritePolicy,
    RewritePolicyEditPayload,
    RewritePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyRewriteRuleDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/rewriterule")
    def create_policy_definition(self, payload: RewritePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/rewriterule/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/rewriterule/multiple/{id}
        ...

    @put("/template/policy/definition/rewriterule/{id}")
    def edit_policy_definition(self, id: UUID, payload: RewritePolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/rewriterule", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/rewriterule/{id}")
    def get_policy_definition(self, id: UUID) -> RewritePolicyGetResponse:
        ...

    @post("/template/policy/definition/rewriterule/preview")
    def preview_policy_definition(self, payload: RewritePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/rewriterule/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/rewriterule/bulk
        ...
