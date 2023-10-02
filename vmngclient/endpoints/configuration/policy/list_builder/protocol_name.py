# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import ProtocolNameList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class ProtocolNameListEditPayload(ProtocolNameList, PolicyListId):
    pass


class ProtocolNameListInfo(ProtocolNameList, PolicyListInfo):
    pass


class ConfigurationPolicyProtocolNameListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/protocolname")
    def create_policy_list(self, payload: ProtocolNameList) -> PolicyListId:
        ...

    @delete("/template/policy/list/protocolname/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/protocolname")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/protocolname/{id}")
    def edit_policy_list(self, id: str, payload: ProtocolNameListEditPayload) -> None:
        ...

    @get("/template/policy/list/protocolname/{id}")
    def get_lists_by_id(self, id: str) -> ProtocolNameListInfo:
        ...

    @get("/template/policy/list/protocolname", "data")
    def get_policy_lists(self) -> DataSequence[ProtocolNameListInfo]:
        ...

    @get("/template/policy/list/protocolname/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ProtocolNameListInfo]:
        ...

    @post("/template/policy/list/protocolname/preview")
    def preview_policy_list(self, payload: ProtocolNameList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/protocolname/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
