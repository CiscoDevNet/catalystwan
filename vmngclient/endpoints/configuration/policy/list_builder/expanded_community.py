# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import ExpandedCommunityList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class ExpandedCommunityListEditPayload(ExpandedCommunityList, PolicyListId):
    pass


class ExpandedCommunityListInfo(ExpandedCommunityList, PolicyListInfo):
    pass


class ConfigurationPolicyExpandedCommunityListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/expandedcommunity")
    def create_policy_list(self, payload: ExpandedCommunityList) -> PolicyListId:
        ...

    @delete("/template/policy/list/expandedcommunity/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/expandedcommunity")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/expandedcommunity/{id}")
    def edit_policy_list(self, id: str, payload: ExpandedCommunityListEditPayload) -> None:
        ...

    @get("/template/policy/list/expandedcommunity/{id}")
    def get_lists_by_id(self, id: str) -> ExpandedCommunityListInfo:
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
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
