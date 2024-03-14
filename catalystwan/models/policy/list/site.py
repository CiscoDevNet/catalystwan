# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Set, Tuple

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class SiteListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    site_id: str = Field(serialization_alias="siteId", validation_alias="siteId")


class SiteList(PolicyListBase):
    type: Literal["site"] = "site"
    entries: List[SiteListEntry] = []

    def add_sites(self, sites: Set[int]):
        for site in sites:
            self._add_entry(SiteListEntry(site_id=str(site)))

    def add_site_range(self, site_range: Tuple[int, int]):
        entry = SiteListEntry(site_id=f"{site_range[0]}-{site_range[1]}")
        self._add_entry(entry)


class SiteListEditPayload(SiteList, PolicyListId):
    pass


class SiteListInfo(SiteList, PolicyListInfo):
    pass
