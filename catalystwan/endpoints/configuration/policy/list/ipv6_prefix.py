# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import IPv6PrefixList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class IPv6PrefixListEditPayload(IPv6PrefixList, PolicyListId):
    pass


class IPv6PrefixListInfo(IPv6PrefixList, PolicyListInfo):
    pass


class ConfigurationPolicyIPv6PrefixList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/ipv6prefix")
    def create_policy_list(self, payload: IPv6PrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/ipv6prefix/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/ipv6prefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/ipv6prefix/{id}")
    def edit_policy_list(self, id: UUID, payload: IPv6PrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/ipv6prefix/{id}")
    def get_lists_by_id(self, id: UUID) -> IPv6PrefixListInfo:
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
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
