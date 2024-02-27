# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"


from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import VPNList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class VPNListEditPayload(VPNList, PolicyListId):
    pass


class VPNListInfo(VPNList, PolicyListInfo):
    pass


class ConfigurationPolicyVPNList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/vpn")
    def create_policy_list(self, payload: VPNList) -> PolicyListId:
        ...

    @delete("/template/policy/list/vpn/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/vpn")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/vpn/{id}")
    def edit_policy_list(self, id: UUID, payload: VPNListEditPayload) -> None:
        ...

    @get("/template/policy/list/vpn/{id}")
    def get_lists_by_id(self, id: UUID) -> VPNListInfo:
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
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
