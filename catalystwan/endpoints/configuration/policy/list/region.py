# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.list.region import RegionList, RegionListEditPayload, RegionListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyRegionList(APIEndpoints):
    @post("/template/policy/list/region")
    def create_policy_list(self, payload: RegionList) -> PolicyListId:
        ...

    @delete("/template/policy/list/region/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/region")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/region/{id}")
    def edit_policy_list(self, id: UUID, payload: RegionListEditPayload) -> None:
        ...

    @get("/template/policy/list/region/{id}")
    def get_lists_by_id(self, id: UUID) -> RegionListInfo:
        ...

    @get("/template/policy/list/region", "data")
    def get_policy_lists(self) -> DataSequence[RegionListInfo]:
        ...

    @get("/template/policy/list/region/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[RegionListInfo]:
        ...

    @post("/template/policy/list/region/preview")
    def preview_policy_list(self, payload: RegionList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/region/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
