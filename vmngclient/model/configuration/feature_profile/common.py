from datetime import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.api.configuration_groups.parcel import Global, Variable
from vmngclient.model.common import UUID
from vmngclient.model.configuration.common import Solution

T = TypeVar("T")


class ProfileType(str, Enum):
    TRANSPORT = "transport"
    SYSTEM = "system"
    CLI = "cli"
    SERVICE = "service"


class FeatureProfileInfo(BaseModel):
    profile_id: str = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")


class FeatureProfileDetail(BaseModel):
    profile_id: str = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")
    associated_profile_parcels: List[str] = Field(alias="associatedProfileParcels")
    rid: int = Field(alias="@rid")
    profile_parcel_count: int = Field(alias="profileParcelCount")
    cached_profile: Optional[str] = Field(alias="cachedProfile")


class FromFeatureProfile(BaseModel):
    copy_: UUID = Field(alias="copy")


class FeatureProfileCreationPayload(BaseModel):
    name: str
    description: str
    from_feature_profile: Optional[FromFeatureProfile] = Field(alias="fromFeatureProfile", default=None)


class FeatureProfileEditPayload(BaseModel):
    name: str
    description: str


class FeatureProfileCreationResponse(BaseModel):
    id: UUID


class ParcelCreationResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: UUID = Field(alias="parcelId")


class ParcelType(str, Enum):
    APPQOE = "appqoe"
    LAN_VPN = "lan/vpn"
    LAN_VPN_INTERFACE_ETHERNET = "lan/vpn/interface/ethernet"
    LAN_VPN_INTERFACE_GRE = "lan/vpn/interface/gre"
    LAN_VPN_INTERFACE_IPSEC = "lan/vpn/interface/ipsec"
    LAN_VPN_INTERFACE_SVI = "lan/vpn/interface/svi"
    DHCP_SERVER = "dhcp-server"
    TRACKER = "tracker"
    TRACKER_GROUP = "trackergroup"
    ROUTING_BGP = "routing/bgp"
    ROUTING_EIGRP = "routing/eigrp"
    ROUTING_MULTICAST = "routing/multicast"
    ROUTING_OSPF = "routing/ospf"
    ROUTING_OSPFV3_IPV4 = "routing/ospfv3/ipv4"
    ROUTING_OSPFV3_IPV6 = "routing/ospfv3/ipv6"
    WIRELESSLAN = "wirelesslan"


class Parcel(BaseModel, Generic[T]):
    parcel_id: str = Field(alias="parcelId")
    parcel_type: ParcelType = Field(alias="parcelType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    created_on: int = Field(alias="createdOn")
    last_updated_on: int = Field(alias="lastUpdatedOn")
    payload: T


class Header(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    generated_on: int = Field(alias="generatedOn")


class ParcelInfo(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class ParcelAssociationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    parcel_id: str = Field(alias="parcelId")


class Prefix(BaseModel):
    address: Union[Variable, Global[str]]
    mask: Union[Variable, Global[str]]
