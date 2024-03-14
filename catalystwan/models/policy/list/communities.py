from typing import List, Literal

from catalystwan.models.common import WellKnownBGPCommunities
from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import CommunityListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class CommunityListBase(PolicyListBase):
    entries: List[CommunityListEntry] = []

    def add_well_known_community(self, community: WellKnownBGPCommunities) -> None:
        self._add_entry(CommunityListEntry(community=community))

    def add_community(self, as_number: int, community_number: int) -> None:
        self._add_entry(CommunityListEntry(community=f"{as_number}:{community_number}"))


class CommunityList(CommunityListBase):
    type: Literal["community"] = "community"


class CommunityListEditPayload(CommunityList, PolicyListId):
    pass


class CommunityListInfo(CommunityList, PolicyListInfo):
    pass


class ExpandedCommunityList(CommunityListBase):
    type: Literal["expandedCommunity"] = "expandedCommunity"


class ExpandedCommunityListEditPayload(ExpandedCommunityList, PolicyListId):
    pass


class ExpandedCommunityListInfo(ExpandedCommunityList, PolicyListInfo):
    pass
