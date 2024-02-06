# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import AppList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class AppListEditPayload(AppList, PolicyListId):
    pass


class AppListInfo(AppList, PolicyListInfo):
    pass


class ConfigurationPolicyApplicationList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/app")
    def create_policy_list(self, payload: AppList) -> PolicyListId:
        ...

    @delete("/template/policy/list/app/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/app")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/app/{id}")
    def edit_policy_list(self, id: UUID, payload: AppListEditPayload) -> None:
        ...

    @get("/template/policy/list/app/{id}")
    def get_lists_by_id(self, id: UUID) -> AppListInfo:
        ...

    @get("/template/policy/list/app", "data")
    def get_policy_lists(self) -> DataSequence[AppListInfo]:
        ...

    @get("/template/policy/list/app/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[AppListInfo]:
        ...

    @post("/template/policy/list/app/preview")
    def preview_policy_list(self, payload: AppList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/app/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
