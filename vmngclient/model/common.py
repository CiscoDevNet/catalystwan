from enum import Enum


class InterfaceTypeEnum(str, Enum):
    ETHERNET = "Ethernet"
    FAST_ETHERNET = "FastEthernet"
    FIVE_GIGABIT_ETHERNET = "FiveGigabitEthernet"
    FORTY_GIGABIT_ETHERNET = "FortyGigabitEthernet"
    GIGABIT_ETHERNET = "GigabitEthernet"
    HUNDRED_GIG_ETHERNET = "HundredGigE"
    LOOPBACK = "Loopback"
    TEN_GIGABIT_ETHERNET = "TenGigabitEthernet"
    TUNNEL = "Tunnel"
    TWENTY_FIVEGIGABIT_ETHERNET = "TwentyFiveGigabitEthernet"
    TWENTY_FIVE_GIG_ETHERNET = "TwentyFiveGigE"
    TWO_GIGABIT_ETHERNET = "TwoGigabitEthernet"
    VIRTUAL_PORT_GROUP = "VirtualPortGroup"
    VLAN = "Vlan"
