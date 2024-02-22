from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class LoggingParcel(_ParcelBase):
    type_: Literal["logging"] = Field(default="logging", exclude=True)
