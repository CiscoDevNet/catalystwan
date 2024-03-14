# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.preferred_color_group import (
    PreferredColorGroupList,
    PreferredColorGroupListEditPayload,
    PreferredColorGroupListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPreferredColorGroupList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/preferredcolorgroup")
    def create_policy_list(self, payload: PreferredColorGroupList) -> PolicyListId:
        ...

    @delete("/template/policy/list/preferredcolorgroup/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/preferredcolorgroup")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/preferredcolorgroup/{id}")
    def edit_policy_list(self, id: UUID, payload: PreferredColorGroupListEditPayload) -> None:
        ...

    @get("/template/policy/list/preferredcolorgroup/{id}")
    def get_lists_by_id(self, id: UUID) -> PreferredColorGroupListInfo:
        ...

    @get("/template/policy/list/preferredcolorgroup", "data")
    def get_policy_lists(self) -> DataSequence[PreferredColorGroupListInfo]:
        ...

    @get("/template/policy/list/preferredcolorgroup/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PreferredColorGroupListInfo]:
        ...

    @post("/template/policy/list/preferredcolorgroup/preview")
    def preview_policy_list(self, payload: PreferredColorGroupList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/preferredcolorgroup/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
