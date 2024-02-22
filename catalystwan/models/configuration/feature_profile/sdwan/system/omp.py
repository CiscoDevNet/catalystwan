from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class OMPParcel(_ParcelBase):
    type_: Literal["omp"] = Field(default="omp", exclude=True)
    
