# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import WellKnownBGPCommunities
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class CommunityListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    community: str = Field(examples=["1000:10000", "internet", "local-AS"])


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
