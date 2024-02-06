from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable


class StaticMacAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    mac_address: Union[Global[str], Variable] = Field(alias="macaddr")
    vlan: Union[Global[int], Variable]
    interface_name: Optional[Union[Global[str], Variable]] = Field(alias="ifName", default=None)


class SwitchportMode(str, Enum):
    ACCESS = "access"
    TRUNK = "trunk"


class Duplex(str, Enum):
    FULL = "full"
    HALF = "half"


class PortControl(str, Enum):
    AUTO = "auto"
    FORCE_UNAUTHORIZED = "force-unauthorized"
    FORCE_AUTHORIZED = "force-authorized"


class HostMode(str, Enum):
    SINGLE_HOST = "single-host"
    MULTI_AUTH = "multi-auth"
    MULTI_HOST = "multi-host"
    MULTI_DOMAIN = "multi-domain"


class ControlDirection(str, Enum):
    BOTH = "both"
    IN = "in"


class SwitchportInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Global[str], Variable] = Field(alias="ifName")
    mode: Optional[Global[SwitchportMode]] = None
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=True)
    speed: Optional[Union[Global[str], Variable, Default[None]]] = Default[None](value=None)
    duplex: Optional[Union[Global[Duplex], Variable, Default[None]]] = Default[None](value=None)
    switchport_access_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        alias="switchportAccessVlan", default=None
    )
    switchport_trunk_allowed_vlans: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        alias="switchportTrunkAllowedVlans", default=None
    )
    switchport_trunk_native_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        alias="switchportTrunkNativeVlan", default=None
    )
    port_control: Optional[Union[Global[PortControl], Variable, Default[None]]] = Field(
        alias="portControl", default=None
    )
    voice_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="voiceVlan", default=None)
    pae_enable: Optional[Union[Global[bool], Variable, Default[None]]] = Field(alias="paeEnable", default=None)
    mac_authentication_bypass: Optional[Union[Global[bool], Variable, Default[None]]] = Field(
        alias="macAuthenticationBypass", default=None
    )
    host_mode: Optional[Union[Global[HostMode], Variable, Default[None]]] = Field(alias="hostMode", default=None)
    enable_periodic_reauth: Optional[Union[Global[bool], Variable, Default[None]]] = Field(
        alias="enablePeriodicReauth", default=None
    )
    inactivity: Optional[Union[Global[int], Variable, Default[None]]] = None
    reauthentication: Optional[Union[Global[int], Variable, Default[int]]] = None
    control_direction: Optional[Union[Global[ControlDirection], Variable, Default[None]]] = Field(
        alias="controlDirection", default=None
    )
    restricted_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="restrictedVlan", default=None)
    guest_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="guestVlan", default=None)
    critical_vlan: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="criticalVlan", default=None)
    enable_voice: Optional[Union[Global[bool], Variable, Default[None]]] = Field(alias="enableVoice", default=None)


class SwitchportData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface: Optional[List[SwitchportInterface]] = None
    age_time: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="ageTime", default=Default[int](value=300)
    )
    static_mac_address: Optional[List[StaticMacAddress]] = Field(alias="staticMacAddress", default=None)


class SwitchportCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: SwitchportData
    metadata: Optional[dict] = None
