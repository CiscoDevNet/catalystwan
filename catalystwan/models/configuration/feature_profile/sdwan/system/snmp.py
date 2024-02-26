from typing import Literal

from pydantic import Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class SNMPParcel(_ParcelBase):
    type_: Literal["snmp"] = Field(default="snmp", exclude=True)
