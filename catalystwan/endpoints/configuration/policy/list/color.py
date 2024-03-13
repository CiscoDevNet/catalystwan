# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.color import ColorList, ColorListEditPayload, ColorListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyColorList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/color")
    def create_policy_list(self, payload: ColorList) -> PolicyListId:
        ...

    @delete("/template/policy/list/color/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/color")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/color/{id}")
    def edit_policy_list(self, id: UUID, payload: ColorListEditPayload) -> None:
        ...

    @get("/template/policy/list/color/{id}")
    def get_lists_by_id(self, id: UUID) -> ColorListInfo:
        ...

    @get("/template/policy/list/color", "data")
    def get_policy_lists(self) -> DataSequence[ColorListInfo]:
        ...

    @get("/template/policy/list/color/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ColorListInfo]:
        ...

    @post("/template/policy/list/color/preview")
    def preview_policy_list(self, payload: ColorList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/color/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
