# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Set, Tuple

from pydantic import BaseModel, Field, field_validator

from catalystwan.models.common import IntRangeStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class VPNListEntry(BaseModel):
    vpn: IntRangeStr = Field(description="0-65530 range or single number")

    @field_validator("vpn")
    @classmethod
    def check_vpn_range(cls, vpn: IntRangeStr):
        for i in vpn:
            if i is not None:
                assert 0 <= i <= 65_530
        return vpn


class VPNList(PolicyListBase):
    type: Literal["vpn"] = "vpn"
    entries: List[VPNListEntry] = []

    def add_vpns(self, vpns: Set[int]):
        for vpn in vpns:
            self._add_entry(VPNListEntry(vpn=(vpn, None)))

    def add_vpn_range(self, vpn_range: Tuple[int, int]):
        self._add_entry(VPNListEntry(vpn=vpn_range))


class VPNListEditPayload(VPNList, PolicyListId):
    pass


class VPNListInfo(VPNList, PolicyListInfo):
    pass
