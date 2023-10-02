# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import FQDNList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class FQDNListEditPayload(FQDNList, PolicyListId):
    pass


class FQDNListInfo(FQDNList, PolicyListInfo):
    pass


class ConfigurationPolicyFQDNListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/fqdn")
    def create_policy_list(self, payload: FQDNList) -> PolicyListId:
        ...

    @delete("/template/policy/list/fqdn/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/fqdn")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/fqdn/{id}")
    def edit_policy_list(self, id: str, payload: FQDNListEditPayload) -> None:
        ...

    @get("/template/policy/list/fqdn/{id}")
    def get_lists_by_id(self, id: str) -> FQDNListInfo:
        ...

    @get("/template/policy/list/fqdn", "data")
    def get_policy_lists(self) -> DataSequence[FQDNListInfo]:
        ...

    @get("/template/policy/list/fqdn/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[FQDNListInfo]:
        ...

    @post("/template/policy/list/fqdn/preview")
    def preview_policy_list(self, payload: FQDNList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/fqdn/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
