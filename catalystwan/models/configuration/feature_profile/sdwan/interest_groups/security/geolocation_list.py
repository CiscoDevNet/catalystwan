from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import check_fields_exclusive


class GeoLocationListEntry(BaseModel):
    country: Optional[Global[str]] = Field(default=None, description="ISO-3166 alpha-3 country code eg: FRA")
    continent: Optional[Global[str]] = Field(
        default=None, description="One of 2-letter continent codes: AF, NA, OC, AN, AS, EU, SA"
    )

    @model_validator(mode="after")
    def check_country_xor_continent(self):
        check_fields_exclusive(self.__dict__, {"country", "continent"}, True)
        return self


class GeoLocationListParcel(_ParcelBase):
    entries: List[GeoLocationListEntry] = Field(validation_alias=AliasPath("data", "entries"))
