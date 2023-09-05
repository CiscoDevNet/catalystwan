# mypy: disable-error-code="empty-body"
from typing import List

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy_list import (
    InfoTag,
    PolicyList,
    PolicyListCreationPayload,
    PolicyListEditPayload,
    PolicyListId,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class SiteListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    site_id: str = Field(alias="siteId")


class SitePayload(BaseModel):
    entries: List[SiteListEntry]
    type: str = Field(default="site", const=True)


class SiteListCreationPayload(SitePayload, PolicyListCreationPayload):
    pass


class SiteListEditPayload(SitePayload, PolicyListEditPayload):
    pass


class SiteList(SitePayload, PolicyList):
    pass


class ConfigurationPolicySiteListBuilder(APIEndpoints):
    @post("/template/policy/list/site/defaultsite")
    def create_default_site_list(self, payload: SiteListCreationPayload) -> PolicyListId:
        ...

    @post("/template/policy/list/site")
    def create_policy_list(self, payload: SiteListCreationPayload) -> PolicyListId:
        ...

    @delete("/template/policy/list/site/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/site")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        # TODO: dont know how to assing tags to check if filter works
        # (it is present in GET response but cannot be added to POST, PUT payload)
        # for now it was tested with default info tag value == ""
        ...

    @put("/template/policy/list/site/{id}")
    def edit_policy_list(self, id: str, payload: SiteListEditPayload) -> None:
        ...

    @get("/template/policy/list/site/{id}")
    def get_lists_by_id(self, id: str) -> SiteList:
        ...

    @get("/template/policy/list/site", "data")
    def get_policy_lists(self) -> DataSequence[SiteList]:
        ...

    @get("/template/policy/list/site/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SiteList]:
        # TODO: dont know how to assing tags to check if filter works
        # (it is present in GET response but cannot be added to POST, PUT payload)
        # for now it was tested with default info tag value == ""
        ...

    @post("/template/policy/list/site/preview")
    def preview_policy_list(self, payload: SiteListCreationPayload) -> PolicyListPreview:
        ...

    @get("/template/policy/list/site/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
