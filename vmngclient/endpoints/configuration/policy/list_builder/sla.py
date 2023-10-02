# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import SLAClassList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class SLAClassListEditPayload(SLAClassList, PolicyListId):
    pass


class SLAClassListInfo(SLAClassList, PolicyListInfo):
    pass


class ConfigurationPolicySLAClassListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/sla")
    def create_policy_list(self, payload: SLAClassList) -> PolicyListId:
        ...

    @delete("/template/policy/list/sla/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/sla")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/sla/{id}")
    def edit_policy_list(self, id: str, payload: SLAClassListEditPayload) -> None:
        ...

    @get("/template/policy/list/sla/{id}")
    def get_lists_by_id(self, id: str) -> SLAClassListInfo:
        ...

    @get("/template/policy/list/sla", "data")
    def get_policy_lists(self) -> DataSequence[SLAClassListInfo]:
        ...

    @get("/template/policy/list/sla/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SLAClassListInfo]:
        ...

    @post("/template/policy/list/sla/preview")
    def preview_policy_list(self, payload: SLAClassList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/sla/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
