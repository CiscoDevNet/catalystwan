# vipType: ignore
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional

from attr import define  # type: ignore

from vmngclient.api.templates.feature_template import FeatureTemplate


class InterfaceType(Enum):
    ETHERNET = "Ethernet"
    FAST_ETHERNET = "FastEthernet"
    FIVE_GIGABIT_ETHERNET = "FiveGigabitEthernet"
    FORTY_GIGABIT_ETHERNET = "FortyGigabitEthernet"
    GIGABIT_ETHERNET = "GigabitEthernet"
    HUNDRED_GIG_E = "HundredGigE"
    LOOPBACK = "Loopback"
    TEN_GIGABIT_ETHERNET = "TenGigabitEthernet"
    TUNNEL = "Tunnel"
    TWENTY_FIVE_GIG_ET = "TwentyFiveGigE"
    TWENTY_FIVE_GIGABIT_ETHERNET = "TwentyFiveGigabitEthernet"
    TWO_GIGABIT_ETHERNET = "TwoGigabitEthernet"
    VIRTUAL_PORT_GROU = "VirtualPortGroup"
    VLAN = "Vlan"


class TypeAddress(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"


class ColorType(Enum):
    G3 = "3g"
    BIZ_INTERNET = "biz-internet"
    BLUE = "blue"
    BRONZE = "bronze"
    CUSTOM_1 = "custom1"
    CUSTOM_2 = "custom2"
    CUSTOM_3 = "custom3"
    DEFAULT = "default"
    GOLD = "gold"
    GREEN = "green"
    LTE = "lte"
    METRO_ETHERNET = "metro-ethernet"
    MPLS = "mpls"
    PRIVATE_1 = "private1"
    PRIVATE_2 = "private2"
    PRIVATE_3 = "private3"
    PRIVATE_4 = "private4"
    PRIVATE_5 = "private5"
    PRIVATE_6 = "private6"
    PUBLIC_INTERNET = "public-internet"
    RED = "red"
    SILVER = "silver"


class EncapType(Enum):
    GRE = "gre"
    IPSEC = "ipsec"


@define
class InterfaceName:
    type: InterfaceType
    number: Optional[str] = None


@define
class Encapsulation:
    type: EncapType
    preference: Optional[int] = None
    weight: Optional[int] = None


@define
class Tunnel:
    color: Optional[ColorType] = None
    all: Optional[bool] = None
    bgp: Optional[bool] = None
    dhcp: Optional[bool] = None
    dns: Optional[bool] = None
    icmp: Optional[bool] = None
    netconf: Optional[bool] = None
    ntp: Optional[bool] = None
    ospf: Optional[bool] = None
    ssh: Optional[bool] = None
    stun: Optional[bool] = None
    https: Optional[bool] = None
    snmp: Optional[bool] = None
    encapsulation: list[Encapsulation] = []


class CiscoVpnInterfaceEthernetModel(FeatureTemplate):
    type: ClassVar[str] = "cisco_vpn_interface"  # Cisco VPN Interface Ethernet
    payload_path: ClassVar[Path] = Path(__file__).parent / "feature/cisco_vpn_interface_ethernet.json.j2"
    interface_name: InterfaceName
    shutdown: Optional[bool]
    type_address: TypeAddress = TypeAddress.STATIC
    ip: Optional[str]
    tunnel: Optional[Tunnel]
    mtu: Optional[int]
    autonegotiate: Optional[bool]

    class Config:
        arbitrary_types_allowed = True
