# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"


from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.vpn import VPNList, VPNListEditPayload, VPNListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


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
