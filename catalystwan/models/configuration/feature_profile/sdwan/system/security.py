from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class SecurityParcel(_ParcelBase):
    type_: Literal["security"] = Field(default="security", exclude=True)
