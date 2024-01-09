from enum import Enum


class ProfileType(str, Enum):
    TRANSPORT = "transport"
    SYSTEM = "system"
    CLI = "cli"
    SERVICE = "service"
