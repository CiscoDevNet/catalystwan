from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class SecurityParcel(_ParcelBase):
    type_: Literal["security"] = Field(default="security", exclude=True)
    
