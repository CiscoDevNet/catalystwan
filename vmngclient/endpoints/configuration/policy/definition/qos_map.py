# mypy: disable-error-code="empty-body"
from uuid import UUID

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.definitions.qos_map import QoSMap
from vmngclient.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class QoSMapEditPayload(QoSMap, PolicyDefinitionId):
    pass


class QoSMapInfo(QoSMap, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyQoSMapDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/qosmap")
    def create_policy_definition(self, payload: QoSMap) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/qosmap/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/qosmap/multiple/{id}
        ...

    @put("/template/policy/definition/qosmap/{id}")
    def edit_policy_definition(self, id: UUID, payload: QoSMapEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/qosmap", "data")
    def get_definitions(self) -> DataSequence[QoSMapInfo]:
        ...

    @get("/template/policy/definition/qosmap/{id}")
    def get_policy_definition(self, id: UUID) -> QoSMapInfo:
        ...

    @post("/template/policy/definition/qosmap/preview")
    def preview_policy_definition(self, payload: QoSMap) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/qosmap/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/qosmap/bulk
        ...
