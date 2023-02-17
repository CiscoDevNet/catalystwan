# vipType: ignore
from __future__ import annotations

from enum import Enum
from typing import Optional

from attr import field  # type: ignore

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
    interface_name: InterfaceType
    shutdownd: Optional[bool] = field(default=None)
    type_address: TypeAddress = field(default=TypeAddress.STATIC)
    ip: Optional[str] = field(default=None)
