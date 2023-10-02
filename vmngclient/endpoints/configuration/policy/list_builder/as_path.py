# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import ASPathList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class ASPathListEditPayload(ASPathList, PolicyListId):
    pass


class ASPathListInfo(ASPathList, PolicyListInfo):
    pass


class ConfigurationPolicyASPathListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/aspath")
    def create_policy_list(self, payload: ASPathList) -> PolicyListId:
        ...

    @delete("/template/policy/list/aspath/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/aspath")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/aspath/{id}")
    def edit_policy_list(self, id: str, payload: ASPathListEditPayload) -> None:
        ...

    @get("/template/policy/list/aspath/{id}")
    def get_lists_by_id(self, id: str) -> ASPathListInfo:
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
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
