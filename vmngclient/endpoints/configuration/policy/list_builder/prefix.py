# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import PrefixList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class PrefixListEditPayload(PrefixList, PolicyListId):
    pass


class PrefixListInfo(PrefixList, PolicyListInfo):
    pass


class ConfigurationPolicyPrefixListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/prefix")
    def create_policy_list(self, payload: PrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/prefix/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/prefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/prefix/{id}")
    def edit_policy_list(self, id: str, payload: PrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/prefix/{id}")
    def get_lists_by_id(self, id: str) -> PrefixListInfo:
        ...

    @get("/template/policy/list/prefix", "data")
    def get_policy_lists(self) -> DataSequence[PrefixListInfo]:
        ...

    @get("/template/policy/list/prefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PrefixListInfo]:
        ...

    @post("/template/policy/list/prefix/preview")
    def preview_policy_list(self, payload: PrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/prefix/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
