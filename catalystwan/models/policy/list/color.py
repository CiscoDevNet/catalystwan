# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel

from catalystwan.models.common import TLOCColor
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ColorListEntry(BaseModel):
    color: TLOCColor


class ColorList(PolicyListBase):
    type: Literal["color"] = "color"
    entries: List[ColorListEntry] = []

    def add_color(self, color: TLOCColor) -> None:
        self._add_entry(ColorListEntry(color=color))


class ColorListEditPayload(ColorList, PolicyListId):
    pass


class ColorListInfo(ColorList, PolicyListInfo):
    pass
