# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, Field, field_validator, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import InterfaceType, check_fields_exclusive


class SecurityZoneListEntry(BaseModel):
    vpn: Optional[Global[str]] = Field(default=None, description="0-65530 single number")
    interface: Optional[Global[InterfaceType]] = None

    @field_validator("vpn")
    @classmethod
    def check_vpn_range(cls, vpn: Global[str]):
        assert 0 <= int(vpn.value) <= 65530
        return vpn

    @model_validator(mode="after")
    def check_vpn_xor_interface(self):
        check_fields_exclusive(self.__dict__, {"vpn", "interface"}, True)
        return self


class SecurityZoneListParcel(_ParcelBase):
    type_: Literal["security-zone"] = Field(default="security-zone", exclude=True)
    entries: List[SecurityZoneListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_interface(self, interface: InterfaceType):
        self.entries.append(
            SecurityZoneListEntry(
                interface=as_global(interface, InterfaceType),
            )
        )

    def add_vpn(self, vpn: str):
        self.entries.append(
            SecurityZoneListEntry(
                vpn=as_global(vpn),
            )
        )
