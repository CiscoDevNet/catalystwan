from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class BFDParcel(_ParcelBase):
    type_: Literal["bfd"] = Field(default="bfd", exclude=True)
    
