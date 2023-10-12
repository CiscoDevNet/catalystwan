# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import AppList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class AppListEditPayload(AppList, PolicyListId):
    pass


class AppListInfo(AppList, PolicyListInfo):
    pass


class ConfigurationPolicyApplicationListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/app")
    def create_policy_list(self, payload: AppList) -> PolicyListId:
        ...

    @delete("/template/policy/list/app/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/app")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/app/{id}")
    def edit_policy_list(self, id: str, payload: AppListEditPayload) -> None:
        ...

    @get("/template/policy/list/app/{id}")
    def get_lists_by_id(self, id: str) -> AppListInfo:
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
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
