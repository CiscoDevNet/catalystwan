# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.communities import (
    ExpandedCommunityList,
    ExpandedCommunityListEditPayload,
    ExpandedCommunityListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyExpandedCommunityList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/expandedcommunity")
    def create_policy_list(self, payload: ExpandedCommunityList) -> PolicyListId:
        ...

    @delete("/template/policy/list/expandedcommunity/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/expandedcommunity")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/expandedcommunity/{id}")
    def edit_policy_list(self, id: UUID, payload: ExpandedCommunityListEditPayload) -> None:
        ...

    @get("/template/policy/list/expandedcommunity/{id}")
    def get_lists_by_id(self, id: UUID) -> ExpandedCommunityListInfo:
        ...

    @get("/template/policy/list/expandedcommunity", "data")
    def get_policy_lists(self) -> DataSequence[ExpandedCommunityListInfo]:
        ...

    @get("/template/policy/list/expandedcommunity/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ExpandedCommunityListInfo]:
        ...

    @post("/template/policy/list/expandedcommunity/preview")
    def preview_policy_list(self, payload: ExpandedCommunityList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/expandedcommunity/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
