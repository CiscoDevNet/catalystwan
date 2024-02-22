
from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class LoggingParcel(_ParcelBase):
    type_: Literal["logging"] = Field(default="logging", exclude=True)
    
