# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.as_path import ASPathList, ASPathListEditPayload, ASPathListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyASPathList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/aspath")
    def create_policy_list(self, payload: ASPathList) -> PolicyListId:
        ...

    @delete("/template/policy/list/aspath/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/aspath")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/aspath/{id}")
    def edit_policy_list(self, id: UUID, payload: ASPathListEditPayload) -> None:
        ...

    @get("/template/policy/list/aspath/{id}")
    def get_lists_by_id(self, id: UUID) -> ASPathListInfo:
        ...

    @get("/template/policy/list/aspath", "data")
    def get_policy_lists(self) -> DataSequence[ASPathListInfo]:
        ...

    @get("/template/policy/list/aspath/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ASPathListInfo]:
        ...

    @post("/template/policy/list/aspath/preview")
    def preview_policy_list(self, payload: ASPathList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/aspath/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
