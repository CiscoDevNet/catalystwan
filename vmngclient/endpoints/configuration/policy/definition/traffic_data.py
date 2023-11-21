# mypy: disable-error-code="empty-body"

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.definitions.traffic_data import TrafficDataPolicy, TrafficDataPolicyHeader
from vmngclient.model.policy.policy import PolicyId
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class TrafficDataPolicyGetResponse(TrafficDataPolicy, PolicyDefinitionId):
    pass


class TrafficDataPolicyEditPayload(TrafficDataPolicy, PolicyDefinitionId):
    pass


class TrafficDataPolicyInfo(TrafficDataPolicyHeader, PolicyDefinitionInfo, PolicyId):
    pass


class ConfigurationPolicyDataDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/data")
    def create_policy_definition(self, payload: TrafficDataPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/data/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/data/multiple/{id}
        ...

    @put("/template/policy/definition/data/{id}")
    def edit_policy_definition(self, id: str, payload: TrafficDataPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/data", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/data/{id}")
    def get_policy_definition(self, id: str) -> TrafficDataPolicyGetResponse:
        ...

    @post("/template/policy/definition/data/preview")
    def preview_policy_definition(self, payload: TrafficDataPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/data/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/data/bulk
        ...
