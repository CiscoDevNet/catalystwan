# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import URLWhiteList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class URLWhiteListEditPayload(URLWhiteList, PolicyListId):
    pass


class URLWhiteListInfo(URLWhiteList, PolicyListInfo):
    pass


class ConfigurationPolicyURLWhiteList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/urlwhitelist")
    def create_policy_list(self, payload: URLWhiteList) -> PolicyListId:
        ...

    @delete("/template/policy/list/urlwhitelist/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/urlwhitelist")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/urlwhitelist/{id}")
    def edit_policy_list(self, id: UUID, payload: URLWhiteListEditPayload) -> None:
        ...

    @get("/template/policy/list/urlwhitelist/{id}")
    def get_lists_by_id(self, id: UUID) -> URLWhiteListInfo:
        ...

    @get("/template/policy/list/urlwhitelist", "data")
    def get_policy_lists(self) -> DataSequence[URLWhiteListInfo]:
        ...

    @get("/template/policy/list/urlwhitelist/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[URLWhiteListInfo]:
        ...

    @post("/template/policy/list/urlwhitelist/preview")
    def preview_policy_list(self, payload: URLWhiteList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/urlwhitelist/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
