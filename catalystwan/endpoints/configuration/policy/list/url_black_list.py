# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import URLBlackList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class URLBlackListEditPayload(URLBlackList, PolicyListId):
    pass


class URLBlackListInfo(URLBlackList, PolicyListInfo):
    pass


class ConfigurationPolicyURLBlackList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/urlblacklist")
    def create_policy_list(self, payload: URLBlackList) -> PolicyListId:
        ...

    @delete("/template/policy/list/urlblacklist/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/urlblacklist")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/urlblacklist/{id}")
    def edit_policy_list(self, id: UUID, payload: URLBlackListEditPayload) -> None:
        ...

    @get("/template/policy/list/urlblacklist/{id}")
    def get_lists_by_id(self, id: UUID) -> URLBlackListInfo:
        ...

    @get("/template/policy/list/urlblacklist", "data")
    def get_policy_lists(self) -> DataSequence[URLBlackListInfo]:
        ...

    @get("/template/policy/list/urlblacklist/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[URLBlackListInfo]:
        ...

    @post("/template/policy/list/urlblacklist/preview")
    def preview_policy_list(self, payload: URLBlackList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/urlblacklist/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
