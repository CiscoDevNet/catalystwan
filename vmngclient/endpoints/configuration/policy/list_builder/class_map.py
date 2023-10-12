# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import ClassMapList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class ClassMapListEditPayload(ClassMapList, PolicyListId):
    pass


class ClassMapListInfo(ClassMapList, PolicyListInfo):
    pass


class ConfigurationPolicyForwardingClassListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/class")
    def create_policy_list(self, payload: ClassMapList) -> PolicyListId:
        ...

    @delete("/template/policy/list/class/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/class")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/class/{id}")
    def edit_policy_list(self, id: str, payload: ClassMapListEditPayload) -> None:
        ...

    @get("/template/policy/list/class/{id}")
    def get_lists_by_id(self, id: str) -> ClassMapListInfo:
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
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
