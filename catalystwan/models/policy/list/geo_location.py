# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from catalystwan.models.common import check_fields_exclusive
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class GeoLocationListEntry(BaseModel):
    country: Optional[str] = Field(default=None, description="ISO-3166 alpha-3 country code eg: FRA")
    continent: Optional[str] = Field(
        default=None, description="One of 2-letter continent codes: AF, NA, OC, AN, AS, EU, SA"
    )

    @model_validator(mode="after")
    def check_country_xor_continent(self):
        check_fields_exclusive(self.__dict__, {"country", "continent"}, True)
        return self


class GeoLocationList(PolicyListBase):
    type: Literal["geoLocation"] = "geoLocation"
    entries: List[GeoLocationListEntry] = []


class GeoLocationListEditPayload(GeoLocationList, PolicyListId):
    pass


class GeoLocationListInfo(GeoLocationList, PolicyListInfo):
    pass
