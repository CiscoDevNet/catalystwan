from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class GlobalParcel(_ParcelBase):
    type_: Literal["global"] = Field(default="global", exclude=True)
    
