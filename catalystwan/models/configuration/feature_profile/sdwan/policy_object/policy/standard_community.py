# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import WellKnownBGPCommunities


class StandardCommunityEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    standard_community: Global[WellKnownBGPCommunities] = Field(
        serialization_alias="standardCommunity", validation_alias="standardCommunity"
    )


class StandardCommunityParcel(_ParcelBase):
    entries: List[StandardCommunityEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_community(self, standard_community: WellKnownBGPCommunities):
        self.entries.append(
            StandardCommunityEntry(standard_community=as_global(standard_community, WellKnownBGPCommunities))
        )
