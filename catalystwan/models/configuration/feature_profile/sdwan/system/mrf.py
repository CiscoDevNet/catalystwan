from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class MRFParcel(_ParcelBase):
    type_: Literal["mrf"] = Field(default="mrf", exclude=True)
    
