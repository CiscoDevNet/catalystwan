from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class BasicParcel(_ParcelBase):
    type_: Literal["basic"] = Field(default="basic", exclude=True)
