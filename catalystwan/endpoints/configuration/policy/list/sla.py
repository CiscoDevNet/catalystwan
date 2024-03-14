# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.sla import SLAClassList, SLAClassListEditPayload, SLAClassListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicySLAClassList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/sla")
    def create_policy_list(self, payload: SLAClassList) -> PolicyListId:
        ...

    @delete("/template/policy/list/sla/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/sla")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/sla/{id}")
    def edit_policy_list(self, id: UUID, payload: SLAClassListEditPayload) -> None:
        ...

    @get("/template/policy/list/sla/{id}")
    def get_lists_by_id(self, id: UUID) -> SLAClassListInfo:
        ...

    @get("/template/policy/list/sla", "data")
    def get_policy_lists(self) -> DataSequence[SLAClassListInfo]:
        ...

    @get("/template/policy/list/sla/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SLAClassListInfo]:
        ...

    @post("/template/policy/list/sla/preview")
    def preview_policy_list(self, payload: SLAClassList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/sla/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
