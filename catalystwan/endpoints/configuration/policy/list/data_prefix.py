# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.data_prefix import DataPrefixList, DataPrefixListEditPayload, DataPrefixListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyDataPrefixList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/dataprefix")
    def create_policy_list(self, payload: DataPrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/dataprefix/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/dataprefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/dataprefix/{id}")
    def edit_policy_list(self, id: UUID, payload: DataPrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/dataprefix/{id}")
    def get_lists_by_id(self, id: UUID) -> DataPrefixListInfo:
        ...

    @get("/template/policy/list/dataprefix", "data")
    def get_policy_lists(self) -> DataSequence[DataPrefixListInfo]:
        ...

    @get("/template/policy/list/dataprefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[DataPrefixListInfo]:
        ...

    @post("/template/policy/list/dataprefix/preview")
    def preview_policy_list(self, payload: DataPrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/dataprefix/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
