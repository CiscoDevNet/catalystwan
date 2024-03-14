# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.rule_set import RuleSet, RuleSetEditPayload, RuleSetGetResponse
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyRuleSetDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/ruleset")
    def create_policy_definition(self, payload: RuleSet) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/ruleset/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/ruleset/multiple/{id}
        ...

    @put("/template/policy/definition/ruleset/{id}")
    def edit_policy_definition(self, id: UUID, payload: RuleSetEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/ruleset", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/ruleset/{id}")
    def get_policy_definition(self, id: UUID) -> RuleSetGetResponse:
        ...

    @post("/template/policy/definition/ruleset/preview")
    def preview_policy_definition(self, payload: RuleSet) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/ruleset/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/ruleset/bulk
        ...
