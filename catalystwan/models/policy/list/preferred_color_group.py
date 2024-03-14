# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Set, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from catalystwan.models.common import TLOCColor, str_as_str_list
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo

PathPreference = Literal[
    "direct-path",
    "multi-hop-path",
    "all-paths",
]


class ColorGroupPreference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    color_preference: Set[TLOCColor] = Field(serialization_alias="colorPreference", validation_alias="colorPreference")
    path_preference: PathPreference = Field(serialization_alias="pathPreference", validation_alias="pathPreference")

    _color_pref = field_validator("color_preference", mode="before")(str_as_str_list)

    @staticmethod
    def from_color_set_and_path(
        color_preference: Set[TLOCColor], path_preference: PathPreference
    ) -> "ColorGroupPreference":
        return ColorGroupPreference(color_preference=color_preference, path_preference=path_preference)


class PreferredColorGroupListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    primary_preference: ColorGroupPreference = Field(
        serialization_alias="primaryPreference", validation_alias="primaryPreference"
    )
    secondary_preference: Optional[ColorGroupPreference] = Field(
        default=None, serialization_alias="secondaryPreference", validation_alias="secondaryPreference"
    )
    tertiary_preference: Optional[ColorGroupPreference] = Field(
        default=None, serialization_alias="tertiaryPreference", validation_alias="tertiaryPreference"
    )

    @model_validator(mode="after")
    def check_optional_preferences_order(self):
        assert not (self.secondary_preference is None and self.tertiary_preference is not None)
        return self


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
