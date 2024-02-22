from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class MRFParcel(_ParcelBase):
    type_: Literal["mrf"] = Field(default="mrf", exclude=True)
