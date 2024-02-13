from typing import List

from pydantic import AliasPath, BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import TLOCColorEnum
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class ColorEntry(BaseModel):
    color: Global[TLOCColorEnum]


class ColorParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.COLOR)
    entries: List[ColorEntry] = Field(validation_alias=AliasPath("data", "entries"))
