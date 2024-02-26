from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class BannerParcel(_ParcelBase):
    type_: Literal["banner"] = Field(default="banner", exclude=True)
