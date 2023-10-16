# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.definitions.security_group import SecurityGroup
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionBuilder,
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class SecurityGroupEditPayload(SecurityGroup, PolicyDefinitionId):
    pass


class SecurityGroupInfo(SecurityGroup, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicySecurityGroupDefinitionBuilder(APIEndpoints, PolicyDefinitionBuilder):
    @post("/template/policy/definition/securitygroup")
    def create_policy_definition(self, payload: SecurityGroup) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/securitygroup/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/securitygroup/multiple/{id}
        ...

    @put("/template/policy/definition/securitygroup/{id}")
    def edit_policy_definition(self, id: str, payload: SecurityGroupEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/securitygroup", "data")
    def get_definitions(self) -> DataSequence[SecurityGroupInfo]:
        ...

    @get("/template/policy/definition/securitygroup/{id}")
    def get_policy_definition(self, id: str) -> SecurityGroupInfo:
        ...

    @post("/template/policy/definition/securitygroup/preview")
    def preview_policy_definition(self, payload: SecurityGroup) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/securitygroup/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/securitygroup/bulk
        ...
