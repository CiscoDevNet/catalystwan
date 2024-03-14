from typing import List, Literal, Set, Tuple

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import RegionListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class RegionList(PolicyListBase):
    type: Literal["region"] = "region"
    entries: List[RegionListEntry] = []

    def add_regions(self, regions: Set[int]):
        for region in regions:
            self._add_entry(RegionListEntry(region_id=str(region)))

    def add_region_range(self, region_range: Tuple[int, int]):
        entry = RegionListEntry(region_id=f"{region_range[0]}-{region_range[1]}")
        self._add_entry(entry)


class RegionListEditPayload(RegionList, PolicyListId):
    pass


class RegionListInfo(RegionList, PolicyListInfo):
    pass
