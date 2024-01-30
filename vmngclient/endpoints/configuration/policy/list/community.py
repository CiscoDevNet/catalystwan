# mypy: disable-error-code="empty-body"
from uuid import UUID

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.lists import CommunityList
from vmngclient.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class CommunityListEditPayload(CommunityList, PolicyListId):
    pass


class CommunityListInfo(CommunityList, PolicyListInfo):
    pass


class ConfigurationPolicyCommunityList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/community")
    def create_policy_list(self, payload: CommunityList) -> PolicyListId:
        ...

    @delete("/template/policy/list/community/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/community")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/community/{id}")
    def edit_policy_list(self, id: UUID, payload: CommunityListEditPayload) -> None:
        ...

    @get("/template/policy/list/community/{id}")
    def get_lists_by_id(self, id: UUID) -> CommunityListInfo:
        ...

    @get("/template/policy/list/community", "data")
    def get_policy_lists(self) -> DataSequence[CommunityListInfo]:
        ...

    @get("/template/policy/list/community/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[CommunityListInfo]:
        ...

    @post("/template/policy/list/community/preview")
    def preview_policy_list(self, payload: CommunityList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/community/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
