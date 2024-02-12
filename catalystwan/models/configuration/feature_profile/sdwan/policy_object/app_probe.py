from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorType
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class Dscp(Global):
    value: int = Field(ge=0, le=63)


class MapItem(BaseModel):
    color: ColorType
    dscp: Dscp


class ForwardingClassName(Global):
    value: str = Field(description="Name of a chosen Forwarding Class")


class AppProbeEntry(BaseModel):
    map: List[MapItem]
    forwarding_class_name: ForwardingClassName = Field(alias="forwardingClass")


class AppProbeData(BaseModel):
    entries: List[AppProbeEntry]


class AppProbePayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.APP_PROBE)
    data: AppProbeData
