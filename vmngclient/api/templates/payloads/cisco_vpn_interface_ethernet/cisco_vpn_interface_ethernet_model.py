# vipType: ignore
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional

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


class CiscoVpnInterfaceEthernetModel(FeatureTemplate):
    payload_path: ClassVar[Path] = Path(__file__).parent / "feature/cisco_vpn_interface_ethernet.json.j2"
    interface_name: InterfaceType
    shutdown: Optional[bool]
    type_address: TypeAddress = TypeAddress.STATIC
    ip: Optional[str]

    class Config:
        arbitrary_types_allowed = True
