# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.policy.lists_entries import PolicerExceedAction


class PolicierEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    burst: Global[int]
    exceed: Global[PolicerExceedAction]
    rate: Global[int]

    @field_validator("burst")
    @classmethod
    def check_burst(cls, burst_str: Global):
        assert 15000 <= burst_str.value <= 10_000_000
        return burst_str

    @field_validator("rate")
    @classmethod
    def check_rate(cls, rate_str: Global):
        assert 8 <= rate_str.value <= 100_000_000_000
        return rate_str


class PolicierParcel(_ParcelBase):
    entries: List[PolicierEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_entry(self, burst: int, exceed: PolicerExceedAction, rate: int):
        self.entries.append(
            PolicierEntry(
                burst=as_global(burst),
                exceed=as_global(exceed, PolicerExceedAction),
                rate=as_global(rate),
            )
        )
