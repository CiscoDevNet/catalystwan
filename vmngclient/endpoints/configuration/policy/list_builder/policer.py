# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import PolicerList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class PolicerListEditPayload(PolicerList, PolicyListId):
    pass


class PolicerListInfo(PolicerList, PolicyListInfo):
    pass


class ConfigurationPolicyPolicerClassListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/policer")
    def create_policy_list(self, payload: PolicerList) -> PolicyListId:
        ...

    @delete("/template/policy/list/policer/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/policer")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/policer/{id}")
    def edit_policy_list(self, id: str, payload: PolicerListEditPayload) -> None:
        ...

    @get("/template/policy/list/policer/{id}")
    def get_lists_by_id(self, id: str) -> PolicerListInfo:
        ...

    @get("/template/policy/list/policer", "data")
    def get_policy_lists(self) -> DataSequence[PolicerListInfo]:
        ...

    @get("/template/policy/list/policer/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PolicerListInfo]:
        ...

    @post("/template/policy/list/policer/preview")
    def preview_policy_list(self, payload: PolicerList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/policer/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
