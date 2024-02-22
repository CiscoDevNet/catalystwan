from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class BasicParcel(_ParcelBase):
    type_: Literal["basic"] = Field(default="basic", exclude=True)
    
