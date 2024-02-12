from enum import Enum
from ipaddress import IPv4Address
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field, PrivateAttr
from pydantic.functional_validators import AfterValidator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorType
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType

PreferenceValue = Annotated[
    Union[str, int], AfterValidator(lambda value: value if isinstance(value, str) else str(value))
]


class Encapsulation(str, Enum):
    IPSEC = "ipsec"
    GRE = "gre"


class Preference(Global):
    value: PreferenceValue = Field(ge=0, le=4_294_967_295)  # 2 ** 32 - 1


class TlocIPv4Address(Global):
    value: IPv4Address


class TlocEntry(BaseModel):
    tloc: TlocIPv4Address
    color: ColorType
    encapsulation: Encapsulation = Field(alias="encap")
    preference: Optional[Preference] = None


class TlocData(_ParcelBase):
    entries: List[TlocEntry]


class TlocPayload(BaseModel):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.TLOC)
    data: TlocData
