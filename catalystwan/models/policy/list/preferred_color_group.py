from typing import List, Literal, Optional, Set, Tuple

from catalystwan.models.common import TLOCColor
from catalystwan.models.policy.lists_entries import ColorGroupPreference, PathPreference, PreferredColorGroupListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class PreferredColorGroupList(PolicyListBase):
    type: Literal["preferredColorGroup"] = "preferredColorGroup"
    entries: List[PreferredColorGroupListEntry] = []

    def assign_color_groups(
        self,
        primary: Tuple[Set[TLOCColor], PathPreference],
        secondary: Optional[Tuple[Set[TLOCColor], PathPreference]] = None,
        tertiary: Optional[Tuple[Set[TLOCColor], PathPreference]] = None,
    ) -> PreferredColorGroupListEntry:
        primary_preference = ColorGroupPreference.from_color_set_and_path(*primary)
        secondary_preference = (
            ColorGroupPreference.from_color_set_and_path(*secondary) if secondary is not None else None
        )
        tertiary_preference = ColorGroupPreference.from_color_set_and_path(*tertiary) if tertiary is not None else None
        entry = PreferredColorGroupListEntry(
            primary_preference=primary_preference,
            secondary_preference=secondary_preference,
            tertiary_preference=tertiary_preference,
        )
        self._add_entry(entry=entry, single=True)
        return entry


class PreferredColorGroupListEditPayload(PreferredColorGroupList, PolicyListId):
    pass


class PreferredColorGroupListInfo(PreferredColorGroupList, PolicyListInfo):
    pass
