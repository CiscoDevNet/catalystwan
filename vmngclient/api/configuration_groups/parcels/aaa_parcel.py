from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from vmngclient.api.configuration_groups.parcel import Default, Global, Parcel


class ServerAuthOrder(str, Enum):
    LOCAL = "local"
    RADIUS = "radius"
    TACACS = "tacacs"


class User(Parcel):
    name: str
    password: str
    privilege: str


class RadiusServer(Parcel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        extra = "ignore"

    address: str
    key: str
    keyType: str = Field(default="key", alias="group_name")
    acctPort: int = Field(default=1813, alias="acct_port")
    authPort: int = Field(default=1812, alias="auth_port")
    timeout: int = 5
    retransmit: int = 3


class Radius(Parcel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    groupName: str = Field(alias="group_name")
    vpn: int = 0
    sourceInterface: Optional[str] = Field(alias="source_interface")
    server: List[RadiusServer]


# TODO Get model from schema
# Created only for demo purpouses
class AAAParcel(Parcel):
    user: Optional[Global[List[User]]] = Field(default=None)
    authentication_group: Union[Global[bool], Default[bool]] = Field(
        default=Default(value=False), alias="authenticationGroup"
    )
    accounting_group: Union[Global[bool], Default[bool]] = Field(default=Default(value=False), alias="accountingGroup")
    server_auth_order: Global[List[str]] = Field(alias="serverAuthOrder")
    authorization_console: Union[Global[bool], Default[bool]] = Field(
        default=Default(value=False), alias="authorizationConsole"
    )
    authorization_config_commands: Union[Global[bool], Default[bool]] = Field(
        default=Default(value=False), alias="authorizationConfigCommands"
    )
    radius: Optional[List[Radius]]
