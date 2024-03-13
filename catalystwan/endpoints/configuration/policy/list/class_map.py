# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.class_map import ClassMapList, ClassMapListEditPayload, ClassMapListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyForwardingClassList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/class")
    def create_policy_list(self, payload: ClassMapList) -> PolicyListId:
        ...

    @delete("/template/policy/list/class/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/class")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/class/{id}")
    def edit_policy_list(self, id: UUID, payload: ClassMapListEditPayload) -> None:
        ...

    @get("/template/policy/list/class/{id}")
    def get_lists_by_id(self, id: UUID) -> ClassMapListInfo:
        ...

    @get("/template/policy/list/class", "data")
    def get_policy_lists(self) -> DataSequence[ClassMapListInfo]:
        ...

    @get("/template/policy/list/class/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ClassMapListInfo]:
        ...

    @post("/template/policy/list/class/preview")
    def preview_policy_list(self, payload: ClassMapList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/class/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
