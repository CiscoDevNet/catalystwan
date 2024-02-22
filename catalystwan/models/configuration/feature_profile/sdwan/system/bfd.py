from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class BFDParcel(_ParcelBase):
    type_: Literal["bfd"] = Field(default="bfd", exclude=True)
