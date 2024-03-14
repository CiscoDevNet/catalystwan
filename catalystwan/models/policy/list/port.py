# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, field_validator

from catalystwan.models.common import IntRangeStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class PortListEntry(BaseModel):
    port: IntRangeStr

    @field_validator("port")
    @classmethod
    def check_port(cls, port: IntRangeStr):
        for i in port:
            if i is not None:
                assert 0 <= i <= 65_535
        return port


class PortList(PolicyListBase):
    type: Literal["port"] = "port"
    entries: List[PortListEntry] = []


class PortListEditPayload(PortList, PolicyListId):
    pass


class PortListInfo(PortList, PolicyListInfo):
    pass
