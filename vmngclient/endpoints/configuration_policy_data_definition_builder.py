# mypy: disable-error-code="empty-body"
from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get, post
from vmngclient.model.policy_definition import (
    PolicyDefinition,
    PolicyDefinitionCreationPayload,
    PolicyDefinitionEditPayload,
    PolicyDefinitionId,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class Data(BaseModel):
    type: str = Field(default="data", const=True)


class DataDefinitionCreationPayload(Data, PolicyDefinitionCreationPayload):
    pass


class DataDefinitionEditPayload(Data, PolicyDefinitionEditPayload):
    pass


class DataDefinition(Data, PolicyDefinition):
    pass


class ConfigurationPolicyDataDefinitionBuilder(APIEndpoints):
    @post("/template/policy/definition/data")
    def create_policy_definition(self, payload: DataDefinitionCreationPayload) -> PolicyDefinitionId:
        ...

    def delete_policy_definition(self):
        # DELETE /template/policy/definition/data/{id}
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/data/multiple/{id}
        ...

    def edit_policy_definition(self):
        # PUT /template/policy/definition/data/{id}
        ...

    @get("/template/policy/definition/data", "data")
    def get_definitions(self) -> DataSequence[DataDefinition]:
        # GET /template/policy/definition/data
        ...

    @get("/template/policy/definition/data/{id}")
    def get_policy_definition(self, id: str) -> DataDefinition:
        ...

    @post("/template/policy/definition/data/preview")
    def preview_policy_definition(self, payload: DataDefinitionCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/data/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk15(self):
        # PUT /template/policy/definition/data/bulk
        ...
