# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.app_probe import (
    AppProbeClassList,
    AppProbeClassListEditPayload,
    AppProbeClassListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyAppProbeClassList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/appprobe")
    def create_policy_list(self, payload: AppProbeClassList) -> PolicyListId:
        ...

    @delete("/template/policy/list/appprobe/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/appprobe")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/appprobe/{id}")
    def edit_policy_list(self, id: UUID, payload: AppProbeClassListEditPayload) -> None:
        ...

    @get("/template/policy/list/appprobe/{id}")
    def get_lists_by_id(self, id: UUID) -> AppProbeClassListInfo:
        ...

    @get("/template/policy/list/appprobe", "data")
    def get_policy_lists(self) -> DataSequence[AppProbeClassListInfo]:
        ...

    @get("/template/policy/list/appprobe/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[AppProbeClassListInfo]:
        ...

    @post("/template/policy/list/appprobe/preview")
    def preview_policy_list(self, payload: AppProbeClassList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/appprobe/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
