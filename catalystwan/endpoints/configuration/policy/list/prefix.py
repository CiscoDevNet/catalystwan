# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import PrefixList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class PrefixListEditPayload(PrefixList, PolicyListId):
    pass


class PrefixListInfo(PrefixList, PolicyListInfo):
    pass


class ConfigurationPolicyPrefixList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/prefix")
    def create_policy_list(self, payload: PrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/prefix/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/prefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/prefix/{id}")
    def edit_policy_list(self, id: UUID, payload: PrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/prefix/{id}")
    def get_lists_by_id(self, id: UUID) -> PrefixListInfo:
        ...

    @get("/template/policy/list/prefix", "data")
    def get_policy_lists(self) -> DataSequence[PrefixListInfo]:
        ...

    @get("/template/policy/list/prefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PrefixListInfo]:
        ...

    @post("/template/policy/list/prefix/preview")
    def preview_policy_list(self, payload: PrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/prefix/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
