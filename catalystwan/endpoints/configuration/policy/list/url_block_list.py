# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.url import URLBlockList, URLBlockListEditPayload, URLBlockListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyURLBlockList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/urlblacklist")
    def create_policy_list(self, payload: URLBlockList) -> PolicyListId:
        ...

    @delete("/template/policy/list/urlblacklist/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/urlblacklist")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/urlblacklist/{id}")
    def edit_policy_list(self, id: UUID, payload: URLBlockListEditPayload) -> None:
        ...

    @get("/template/policy/list/urlblacklist/{id}")
    def get_lists_by_id(self, id: UUID) -> URLBlockListInfo:
        ...

    @get("/template/policy/list/urlblacklist", "data")
    def get_policy_lists(self) -> DataSequence[URLBlockListInfo]:
        ...

    @get("/template/policy/list/urlblacklist/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[URLBlockListInfo]:
        ...

    @post("/template/policy/list/urlblacklist/preview")
    def preview_policy_list(self, payload: URLBlockList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/urlblacklist/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
