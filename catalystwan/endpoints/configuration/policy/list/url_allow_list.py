# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.url import URLAllowList, URLAllowListEditPayload, URLAllowListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyURLAllowList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/urlwhitelist")
    def create_policy_list(self, payload: URLAllowList) -> PolicyListId:
        ...

    @delete("/template/policy/list/urlwhitelist/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/urlwhitelist")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/urlwhitelist/{id}")
    def edit_policy_list(self, id: UUID, payload: URLAllowListEditPayload) -> None:
        ...

    @get("/template/policy/list/urlwhitelist/{id}")
    def get_lists_by_id(self, id: UUID) -> URLAllowListInfo:
        ...

    @get("/template/policy/list/urlwhitelist", "data")
    def get_policy_lists(self) -> DataSequence[URLAllowListInfo]:
        ...

    @get("/template/policy/list/urlwhitelist/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[URLAllowListInfo]:
        ...

    @post("/template/policy/list/urlwhitelist/preview")
    def preview_policy_list(self, payload: URLAllowList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/urlwhitelist/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
