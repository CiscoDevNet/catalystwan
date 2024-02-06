from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId


class IkeMode(str, Enum):
    MAIN = "main"
    AGGRESIVE = "aggresive"


class IkeCiphersuite(str, Enum):
    AES256_CBC_SHA1 = "aes256-cbc-sha1"
    AES256_CBC_SHA2 = "aes256-cbc-sha2"
    AES128_CBC_SHA1 = "aes128-cbc-sha1"
    AES128_CBC_SHA2 = "aes128-cbc-sha2"


class IkeGroup(str, Enum):
    GROUP_2 = "2"
    GROUP_14 = "14"
    GROUP_15 = "15"
    GROUP_16 = "16"
    GROUP_19 = "19"
    GROUP_20 = "20"
    GROUP_21 = "21"
    GROUP_24 = "24"


class IpsecCiphersuite(str, Enum):
    AES256_CBC_SHA1 = "aes256-cbc-sha1"
    AES256_CBC_SHA384 = "aes256-cbc-sha384"
    AES256_CBC_SHA256 = "aes256-cbc-sha256"
    AES256_CBC_SHA512 = "aes256-cbc-sha512"
    AES256_GCM = "aes256-gcm"
    NULL_SHA1 = "null-sha1"
    NULL_SHA384 = "null-sha384"
    NULL_SHA256 = "null-sha256"
    NULL_SHA512 = "null-sha512"


class PfsGroup(str, Enum):
    GROUP_1 = "group-1"
    GROUP_2 = "group-2"
    GROUP_5 = "group-5"
    GROUP_14 = "group-14"
    GROUP_15 = "group-15"
    GROUP_16 = "group-16"
    GROUP_19 = "group-19"
    GROUP_20 = "group-20"
    GROUP_21 = "group-21"
    GROUP_24 = "group-24"
    NONE = "none"


class TunnelApplication(str, Enum):
    NONE = "none"
    SIG = "sig"


class Arp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_address: Union[Variable, Global[str], Default[None]]
    mac_address: Union[Global[str], Variable]


class VrrpTrackerAction(str, Enum):
    DECREMENT = "Decrement"
    SHUTDOWN = "Shutdown"


class VrrpTrackingObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tracker_id: Union[Default[None], RefId] = Field(alias="trackerId")
    tracker_action: Union[Global[VrrpTrackerAction], Variable] = Field(alias="trackerAction")
    decrement_value: Optional[Union[Variable, Global[int]]] = Field(alias="decrementValue", default=None)


class VrrpIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ipv6_link_local: Union[Global[str], Variable] = Field(alias="ipv6LinkLocal")
    prefix: Optional[Union[Global[str], Variable, Default[None]]] = None


class StaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_address: Union[Variable, Global[str], Default[None]] = Field(alias="ipAddress")
    subnet_mask: Union[Variable, Global[str], Default[None]] = Field(alias="subnetMask")


class StaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable]
