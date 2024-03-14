# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo

PolicerExceedAction = Literal[
    "drop",
    "remark",
]


class PolicerListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    burst: IntStr = Field(description="bytes", ge=15_000, le=10_000_000)
    exceed: PolicerExceedAction = "drop"
    rate: IntStr = Field(description="bps", ge=8, le=100_000_000_000)


class PolicerList(PolicyListBase):
    type: Literal["policer"] = "policer"
    entries: List[PolicerListEntry] = []

    def police(self, burst: int, rate: int, exceed: PolicerExceedAction = "drop") -> None:
        # Policer list must have only single entry!
        entry = PolicerListEntry(burst=burst, exceed=exceed, rate=rate)
        self._add_entry(entry, single=True)


class PolicerListEditPayload(PolicerList, PolicyListId):
    pass


class PolicerListInfo(PolicerList, PolicyListInfo):
    pass
