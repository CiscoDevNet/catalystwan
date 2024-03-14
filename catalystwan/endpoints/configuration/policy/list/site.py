# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.site import SiteList, SiteListEditPayload, SiteListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicySiteList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/site/defaultsite")
    def create_default_site_list(self, payload: SiteList) -> PolicyListId:
        ...

    @post("/template/policy/list/site")
    def create_policy_list(self, payload: SiteList) -> PolicyListId:
        ...

    @delete("/template/policy/list/site/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/site")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/site/{id}")
    def edit_policy_list(self, id: UUID, payload: SiteListEditPayload) -> None:
        ...

    @get("/template/policy/list/site/{id}")
    def get_lists_by_id(self, id: UUID) -> SiteListInfo:
        ...

    @get("/template/policy/list/site", "data")
    def get_policy_lists(self) -> DataSequence[SiteListInfo]:
        ...

    @get("/template/policy/list/site/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SiteListInfo]:
        ...

    @post("/template/policy/list/site/preview")
    def preview_policy_list(self, payload: SiteList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/site/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
