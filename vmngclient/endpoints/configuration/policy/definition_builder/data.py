# mypy: disable-error-code="empty-body"
from typing import Optional

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.definitions.data import DataPolicy, DataPolicyDefinition
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionBuilder,
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class DataPolicyCreationPayload(DataPolicy):
    definition: Optional[DataPolicyDefinition] = None


class DataPolicyGetResponse(DataPolicyCreationPayload, PolicyDefinitionId):
    pass


class DataPolicyEditPayload(DataPolicyCreationPayload, PolicyDefinitionId):
    pass


class DataPolicyInfo(DataPolicy, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyDataDefinitionBuilder(APIEndpoints, PolicyDefinitionBuilder):
    @post("/template/policy/definition/data")
    def create_policy_definition(self, payload: DataPolicyCreationPayload) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/data/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/data/multiple/{id}
        ...

    @put("/template/policy/definition/data/{id}")
    def edit_policy_definition(self, id: str, payload: DataPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/data", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/data/{id}")
    def get_policy_definition(self, id: str) -> DataPolicyGetResponse:
        ...

    @post("/template/policy/definition/data/preview")
    def preview_policy_definition(self, payload: DataPolicyCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/data/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/data/bulk
        ...
