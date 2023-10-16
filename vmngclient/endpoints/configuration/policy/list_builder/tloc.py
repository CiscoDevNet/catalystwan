# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import TLOCList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class TLOCListEditPayload(TLOCList, PolicyListId):
    pass


class TLOCListInfo(TLOCList, PolicyListInfo):
    pass


class ConfigurationPolicyTLOCListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/tloc")
    def create_policy_list(self, payload: TLOCList) -> PolicyListId:
        ...

    @delete("/template/policy/list/tloc/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/tloc")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/tloc/{id}")
    def edit_policy_list(self, id: str, payload: TLOCListEditPayload) -> None:
        ...

    @get("/template/policy/list/tloc/{id}")
    def get_lists_by_id(self, id: str) -> TLOCListInfo:
        ...

    @get("/template/policy/list/tloc", "data")
    def get_policy_lists(self) -> DataSequence[TLOCListInfo]:
        ...

    @get("/template/policy/list/tloc/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[TLOCListInfo]:
        ...

    @post("/template/policy/list/tloc/preview")
    def preview_policy_list(self, payload: TLOCList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/tloc/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
