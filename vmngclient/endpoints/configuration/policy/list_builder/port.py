# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import PortList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class PortListEditPayload(PortList, PolicyListId):
    pass


class PortListInfo(PortList, PolicyListInfo):
    pass


class ConfigurationPolicyPortListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/port")
    def create_policy_list(self, payload: PortList) -> PolicyListId:
        ...

    @delete("/template/policy/list/port/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/port")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/port/{id}")
    def edit_policy_list(self, id: str, payload: PortListEditPayload) -> None:
        ...

    @get("/template/policy/list/port/{id}")
    def get_lists_by_id(self, id: str) -> PortListInfo:
        ...

    @get("/template/policy/list/port", "data")
    def get_policy_lists(self) -> DataSequence[PortListInfo]:
        ...

    @get("/template/policy/list/port/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PortListInfo]:
        ...

    @post("/template/policy/list/port/preview")
    def preview_policy_list(self, payload: PortList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/port/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
