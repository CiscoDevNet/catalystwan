# mypy: disable-error-code="empty-body"


from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import VPNList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class VPNListEditPayload(VPNList, PolicyListId):
    pass


class VPNListInfo(VPNList, PolicyListInfo):
    pass


class ConfigurationPolicyVPNListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/vpn")
    def create_policy_list(self, payload: VPNList) -> PolicyListId:
        ...

    @delete("/template/policy/list/vpn/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/vpn")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/vpn/{id}")
    def edit_policy_list(self, id: str, payload: VPNListEditPayload) -> None:
        ...

    @get("/template/policy/list/vpn/{id}")
    def get_lists_by_id(self, id: str) -> VPNListInfo:
        ...

    @get("/template/policy/list/vpn", "data")
    def get_policy_lists(self) -> DataSequence[VPNListInfo]:
        ...

    @get("/template/policy/list/vpn/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[VPNListInfo]:
        ...

    @post("/template/policy/list/vpn/preview")
    def preview_policy_list(self, payload: VPNList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/vpn/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
