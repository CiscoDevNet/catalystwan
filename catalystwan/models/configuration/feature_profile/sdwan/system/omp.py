from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class OMPParcel(_ParcelBase):
    type_: Literal["omp"] = Field(default="omp", exclude=True)
