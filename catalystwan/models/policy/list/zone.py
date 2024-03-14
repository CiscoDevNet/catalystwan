# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Set

from pydantic import BaseModel, Field, field_validator, model_validator

from catalystwan.models.common import InterfaceType, IntRangeStr, check_fields_exclusive
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ZoneListEntry(BaseModel):
    vpn: Optional[IntRangeStr] = Field(default=None, description="0-65530 single number")
    interface: Optional[InterfaceType] = None

    @field_validator("vpn")
    @classmethod
    def check_vpn_range(cls, vpn: IntRangeStr):
        for i in vpn:
            if i is not None:
                assert 0 <= i <= 65_530
        return vpn

    @model_validator(mode="after")
    def check_vpn_xor_interface(self):
        check_fields_exclusive(self.__dict__, {"vpn", "interface"}, True)
        return self


class ZoneList(PolicyListBase):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=(vpn, None)) for vpn in vpns]

    def assign_interfaces(self, ifs: Set[InterfaceType]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]


class ZoneListEditPayload(ZoneList, PolicyListId):
    pass


class ZoneListInfo(ZoneList, PolicyListInfo):
    pass
