from typing import List, Literal

from catalystwan.models.common import TLOCColor
from catalystwan.models.policy.lists_entries import ColorListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ColorList(PolicyListBase):
    type: Literal["color"] = "color"
    entries: List[ColorListEntry] = []

    def add_color(self, color: TLOCColor) -> None:
        self._add_entry(ColorListEntry(color=color))


class ColorListEditPayload(ColorList, PolicyListId):
    pass


class ColorListInfo(ColorList, PolicyListInfo):
    pass
