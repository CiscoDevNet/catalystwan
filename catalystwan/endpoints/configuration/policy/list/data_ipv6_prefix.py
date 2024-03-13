# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.data_ipv6_prefix import (
    DataIPv6PrefixList,
    DataIPv6PrefixListEditPayload,
    DataIPv6PrefixListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyDataIPv6PrefixList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/dataipv6prefix")
    def create_policy_list(self, payload: DataIPv6PrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/dataipv6prefix/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/dataipv6prefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/dataipv6prefix/{id}")
    def edit_policy_list(self, id: UUID, payload: DataIPv6PrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/dataipv6prefix/{id}")
    def get_lists_by_id(self, id: UUID) -> DataIPv6PrefixListInfo:
        ...

    @get("/template/policy/list/dataipv6prefix", "data")
    def get_policy_lists(self) -> DataSequence[DataIPv6PrefixListInfo]:
        ...

    @get("/template/policy/list/dataipv6prefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[DataIPv6PrefixListInfo]:
        ...

    @post("/template/policy/list/dataipv6prefix/preview")
    def preview_policy_list(self, payload: DataIPv6PrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/dataipv6prefix/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
