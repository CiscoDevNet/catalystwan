# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.definitions.rewrite import RewritePolicy
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class RewritePolicyEditPayload(RewritePolicy, PolicyDefinitionId):
    pass


class RewritePolicyInfo(RewritePolicy, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyRewriteRuleDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/rewriterule")
    def create_policy_definition(self, payload: RewritePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/rewriterule/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/rewriterule/multiple/{id}
        ...

    @put("/template/policy/definition/rewriterule/{id}")
    def edit_policy_definition(self, id: str, payload: RewritePolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/rewriterule", "data")
    def get_definitions(self) -> DataSequence[RewritePolicyInfo]:
        ...

    @get("/template/policy/definition/rewriterule/{id}")
    def get_policy_definition(self, id: str) -> RewritePolicyInfo:
        ...

    @post("/template/policy/definition/rewriterule/preview")
    def preview_policy_definition(self, payload: RewritePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/rewriterule/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/rewriterule/bulk
        ...
