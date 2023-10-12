# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import IPSSignatureList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class IPSSignatureListEditPayload(IPSSignatureList, PolicyListId):
    pass


class IPSSignatureListInfo(IPSSignatureList, PolicyListInfo):
    pass


class ConfigurationPolicyIPSSignatureListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/ipssignature")
    def create_policy_list(self, payload: IPSSignatureList) -> PolicyListId:
        ...

    @delete("/template/policy/list/ipssignature/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/ipssignature")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/ipssignature/{id}")
    def edit_policy_list(self, id: str, payload: IPSSignatureListEditPayload) -> None:
        ...

    @get("/template/policy/list/ipssignature/{id}")
    def get_lists_by_id(self, id: str) -> IPSSignatureListInfo:
        ...

    @get("/template/policy/list/ipssignature", "data")
    def get_policy_lists(self) -> DataSequence[IPSSignatureListInfo]:
        ...

    @get("/template/policy/list/ipssignature/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[IPSSignatureListInfo]:
        ...

    @post("/template/policy/list/ipssignature/preview")
    def preview_policy_list(self, payload: IPSSignatureList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/ipssignature/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
