from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class NTPParcel(_ParcelBase):
    type_: Literal["ntp"] = Field(default="ntp", exclude=True)
