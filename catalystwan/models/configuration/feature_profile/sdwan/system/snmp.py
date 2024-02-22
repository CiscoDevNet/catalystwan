from typing import Literal
from catalystwan.api.configuration_groups.parcel import _ParcelBase
from pydantic import Field


class SNMPParcel(_ParcelBase):
    type_: Literal["snmp"] = Field(default="snmp", exclude=True)
