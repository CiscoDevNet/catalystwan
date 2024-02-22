from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class GlobalParcel(_ParcelBase):
    type_: Literal["global"] = Field(default="global", exclude=True)
