from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class NTPParcel(_ParcelBase):
    type_: Literal["ntp"] = Field(default="ntp", exclude=True)
    
