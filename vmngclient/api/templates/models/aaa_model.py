from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class AuthOrder(str, Enum):
    LOCAL = "local"
    RADIUS = "radius"
    TACACS = "tacacs"



class Accept(BaseModel):
    command: str


class Deny(BaseModel):
    command: str


class DefaultAction(str, Enum):
    ACCEPT = "accept"
    DENY = "deny"


class Task(BaseModel):
    name: str
    accept: Optional[List[Accept]]
    deny: Optional[List[Deny]]
    default_action: DefaultAction = Field(alias="default-action")
    accept: Optional[List[Accept]]
    deny: Optional[List[Deny]]
    default_action: DefaultAction = Field(alias="default-action")

    class Config:
        allow_population_by_field_name = True


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"


class Task(BaseModel):
    mode: str
    permission: List[Permission]


class Usergroup(BaseModel):
    name: str
    task: List[Task]


class PubkeyChain(BaseModel):
    usertag: str
    key_string: str = Field(alias="key-string")
    key_type: str = Field(alias="key-type")

    class Config:
        allow_population_by_field_name = True


class User(BaseModel):
    name: str
    password: str
    secret: str
    description: Optional[str]
    group: List[str]
    pubkey_chain: Optional[List[PubkeyChain]] = Field(alias="pubkey-chain")

    class Config:
        allow_population_by_field_name = True


class Authentication(str, Enum):
    ASCII = "ascii"
    PAP = "pap"


class Server(BaseModel):
    address: str
    auth_port: Optional[int] = Field(49, alias="auth-port")
    vpn: Optional[int]
    source_interface: Optional[str] = Field(alias="source-interface")
    key: Optional[str]
    secret_key: Optional[str] = Field(alias="secret-key")
    priority: Optional[int]

    class Config:
        allow_population_by_field_name = True


class Server(BaseModel):
    address: str
    tag: Optional[str]
    auth_port: Optional[int] = Field(1812, alias="auth-port")
    acct_port: Optional[int] = Field(1813, alias="acct-port")
    vpn: Optional[int]
    source_interface: Optional[str] = Field(alias="source-interface")
    key: Optional[str]
    secret_key: Optional[str] = Field(alias="secret-key")
    priority: Optional[int]

    class Config:
        allow_population_by_field_name = True


class AAAModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    auth_order: List[AuthOrder] = Field(
        default=[
            AuthOrder.LOCAL,
            AuthOrder.RADIUS, 
            AuthOrder.TACACS
        ],
        alias="auth-order"
    )
    radius_servers: Optional[List[str]] = Field(alias="radius-servers")
    auth_fallback: Optional[bool] = Field(alias="auth-fallback")
    admin_auth_order: Optional[bool] = Field(alias="admin-auth-order")
    audit_disable: Optional[bool] = Field(alias="audit-disable")
    netconf_disable: Optional[bool] = Field(alias="netconf-disable")
    task: Optional[List[Task]]
    accounting: Optional[bool]
    usergroup: Optional[List[Usergroup]]
    user: Optional[List[User]]
    ciscotacro_user: Optional[bool] = Field(True, alias="ciscotacro-user")
    ciscotacrw_user: Optional[bool] = Field(True, alias="ciscotacrw-user")
    timeout: Optional[int] = 5
    authentication: Optional[Authentication]
    server: Optional[List[Server]]
    timeout: Optional[int]
    retransmit: Optional[int]
    server: Optional[List[Server]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "aaa"
