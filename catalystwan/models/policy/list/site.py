from typing import List, Literal, Set, Tuple

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import SiteListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


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
