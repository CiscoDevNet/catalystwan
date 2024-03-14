# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Set, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.models.common import IntRangeStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class RegionListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    region_id: IntRangeStr = Field(
        serialization_alias="regionId", validation_alias="regionId", description="Number in range 0-63"
    )

    @field_validator("region_id")
    @classmethod
    def check_region_range(cls, region_ids: IntRangeStr):
        for i in region_ids:
            if i is not None:
                assert 0 <= i <= 63
        return region_ids


class RegionList(PolicyListBase):
    type: Literal["region"] = "region"
    entries: List[RegionListEntry] = []

    def add_regions(self, regions: Set[int]):
        for region in regions:
            self._add_entry(RegionListEntry(region_id=(region, None)))

    def add_region_range(self, region_range: Tuple[int, int]):
        entry = RegionListEntry(region_id=region_range)
        self._add_entry(entry)


class RegionListEditPayload(RegionList, PolicyListId):
    pass


class RegionListInfo(RegionList, PolicyListInfo):
    pass
