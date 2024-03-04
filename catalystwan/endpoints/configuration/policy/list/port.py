# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import PortList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class PortListEditPayload(PortList, PolicyListId):
    pass


class PortListInfo(PortList, PolicyListInfo):
    pass


class ConfigurationPolicyPortList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/port")
    def create_policy_list(self, payload: PortList) -> PolicyListId:
        ...

    @delete("/template/policy/list/port/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/port")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/port/{id}")
    def edit_policy_list(self, id: UUID, payload: PortListEditPayload) -> None:
        ...

    @get("/template/policy/list/port/{id}")
    def get_lists_by_id(self, id: UUID) -> PortListInfo:
        ...

    @get("/template/policy/list/port", "data")
    def get_policy_lists(self) -> DataSequence[PortListInfo]:
        ...

    @get("/template/policy/list/port/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PortListInfo]:
        ...

    @post("/template/policy/list/port/preview")
    def preview_policy_list(self, payload: PortList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/port/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
