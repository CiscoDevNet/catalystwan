# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.protocol_name import (
    ProtocolNameList,
    ProtocolNameListEditPayload,
    ProtocolNameListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyProtocolNameList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/protocolname")
    def create_policy_list(self, payload: ProtocolNameList) -> PolicyListId:
        ...

    @delete("/template/policy/list/protocolname/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/protocolname")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/protocolname/{id}")
    def edit_policy_list(self, id: UUID, payload: ProtocolNameListEditPayload) -> None:
        ...

    @get("/template/policy/list/protocolname/{id}")
    def get_lists_by_id(self, id: UUID) -> ProtocolNameListInfo:
        ...

    @get("/template/policy/list/protocolname", "data")
    def get_policy_lists(self) -> DataSequence[ProtocolNameListInfo]:
        ...

    @get("/template/policy/list/protocolname/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ProtocolNameListInfo]:
        ...

    @post("/template/policy/list/protocolname/preview")
    def preview_policy_list(self, payload: ProtocolNameList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/protocolname/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
