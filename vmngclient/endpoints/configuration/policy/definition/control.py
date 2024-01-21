# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.definitions.control import ControlPolicy
from vmngclient.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class ControlPolicyEditPayload(ControlPolicy, PolicyDefinitionId):
    pass


class ControlPolicyInfo(ControlPolicy, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyControlDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/control")
    def create_policy_definition(self, payload: ControlPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/control/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/control/multiple/{id}
        ...

    @put("/template/policy/definition/control/{id}")
    def edit_policy_definition(self, id: str, payload: ControlPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/control", "data")
    def get_definitions(self) -> DataSequence[ControlPolicyInfo]:
        ...

    @get("/template/policy/definition/control/{id}")
    def get_policy_definition(self, id: str) -> ControlPolicyInfo:
        ...

    @post("/template/policy/definition/control/preview")
    def preview_policy_definition(self, payload: ControlPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/control/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/control/bulk
        ...
