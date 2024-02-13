from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field, PrivateAttr, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorType
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class PathPreferenceEnum(str, Enum):
    DIRECT_PATH = "direct-path"
    MULTI_HOP_PATH = "multi-hop-path"
    ALL_PATHS = "all-paths"


class ColorPreference(Global):
    value: List[ColorType]


class PathPreference(Global):
    value: PathPreferenceEnum


class Preference(BaseModel):
    color_preference: ColorPreference = Field(alias="colorPreference")
    path_preference: PathPreference = Field(alias="pathPreference")


class PreferredColorGroupEntry(BaseModel):
    primary_preference: Preference = Field(alias="primaryPreference")
    secondary_preference: Union[Preference, dict] = Field(default_factory=dict, alias="secondaryPreference")
    tertiary_preference: Union[Preference, dict] = Field(default_factory=dict, alias="tertiaryPreference")

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PreferredColorGroupEntry":
        if not self.secondary_preference and self.tertiary_preference:
            raise ValueError("Preference Entry has to have a secondary prefrence when assigning tertiary preference.")
        return self


class PreferredColorGroupData(BaseModel):
    entries: List[PreferredColorGroupEntry]


class PreferredColorGroupPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.PREFERRED_COLOR_GROUP)
    data: PreferredColorGroupData
