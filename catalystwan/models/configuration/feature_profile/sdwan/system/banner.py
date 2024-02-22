from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class BannerParcel(_ParcelBase):
    type_: Literal["banner"] = Field(default="banner", exclude=True)
    
