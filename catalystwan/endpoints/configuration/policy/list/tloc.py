# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.tloc import TLOCList, TLOCListEditPayload, TLOCListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyTLOCList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/tloc")
    def create_policy_list(self, payload: TLOCList) -> PolicyListId:
        ...

    @delete("/template/policy/list/tloc/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/tloc")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/tloc/{id}")
    def edit_policy_list(self, id: UUID, payload: TLOCListEditPayload) -> None:
        ...

    @get("/template/policy/list/tloc/{id}")
    def get_lists_by_id(self, id: UUID) -> TLOCListInfo:
        ...

    @get("/template/policy/list/tloc", "data")
    def get_policy_lists(self) -> DataSequence[TLOCListInfo]:
        ...

    @get("/template/policy/list/tloc/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[TLOCListInfo]:
        ...

    @post("/template/policy/list/tloc/preview")
    def preview_policy_list(self, payload: TLOCList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/tloc/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
