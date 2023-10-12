# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import IPv6PrefixList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class IPv6PrefixListEditPayload(IPv6PrefixList, PolicyListId):
    pass


class IPv6PrefixListInfo(IPv6PrefixList, PolicyListInfo):
    pass


class ConfigurationPolicyIPv6PrefixListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/ipv6prefix")
    def create_policy_list(self, payload: IPv6PrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/ipv6prefix/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/ipv6prefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/ipv6prefix/{id}")
    def edit_policy_list(self, id: str, payload: IPv6PrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/ipv6prefix/{id}")
    def get_lists_by_id(self, id: str) -> IPv6PrefixListInfo:
        ...

    @get("/template/policy/list/ipv6prefix", "data")
    def get_policy_lists(self) -> DataSequence[IPv6PrefixListInfo]:
        ...

    @get("/template/policy/list/ipv6prefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[IPv6PrefixListInfo]:
        ...

    @post("/template/policy/list/ipv6prefix/preview")
    def preview_policy_list(self, payload: IPv6PrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/ipv6prefix/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
