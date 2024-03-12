# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import WellKnownBGPCommunities


class StandardCommunityEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    standard_community: Global[str] = Field(
        serialization_alias="standardCommunity", validation_alias="standardCommunity"
    )


class StandardCommunityParcel(_ParcelBase):
    type_: Literal["standard-community"] = Field(default="standard-community", exclude=True)
    entries: List[StandardCommunityEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def _add_community(self, standard_community: str):
        self.entries.append(StandardCommunityEntry(standard_community=as_global(standard_community)))

    def add_well_known_community(self, standard_community: WellKnownBGPCommunities):
        self._add_community(standard_community)

    def add_community(self, as_number: int, community_number: int) -> None:
        self._add_community(f"{as_number}:{community_number}")
