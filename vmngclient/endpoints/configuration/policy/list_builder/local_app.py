# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import LocalAppList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class LocalAppListEditPayload(LocalAppList, PolicyListId):
    pass


class LocalAppListInfo(LocalAppList, PolicyListInfo):
    pass


class ConfigurationPolicyLocalAppListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/localapp")
    def create_policy_list(self, payload: LocalAppList) -> PolicyListId:
        ...

    @delete("/template/policy/list/localapp/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/localapp")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/localapp/{id}")
    def edit_policy_list(self, id: str, payload: LocalAppListEditPayload) -> None:
        ...

    @get("/template/policy/list/localapp/{id}")
    def get_lists_by_id(self, id: str) -> LocalAppListInfo:
        ...

    @get("/template/policy/list/localapp", "data")
    def get_policy_lists(self) -> DataSequence[LocalAppListInfo]:
        ...

    @get("/template/policy/list/localapp/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[LocalAppListInfo]:
        ...

    @post("/template/policy/list/localapp/preview")
    def preview_policy_list(self, payload: LocalAppList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/localapp/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
