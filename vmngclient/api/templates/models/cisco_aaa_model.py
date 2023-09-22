from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class User(BaseModel):
    name: str
    password: str
    secret: str
    privilege: Optional[str]
    pubkey_chain: List[str] = Field(default=[], vmanage_key="pubkey-chain")


class RadiusServer(BaseModel):
    class Config:
        allow_population_by_field_name = True

    address: str
    auth_port: int = Field(vmanage_key="auth-port", default=1812)
    acct_port: int = Field(vmanage_key="acct-port", default=1813)
    timeout: int = Field(default=5)
    retransmit: int = 3
    key: str
    secret_key: Optional[str] = Field(vmanage_key="secret-key", default=None)
    key_enum: Optional[str] = Field(vmanage_key="key-enum", default=None)
    key_type: Optional[str] = Field(vmanage_key="key-type", default=None)


class RadiusGroup(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    group_name: str = Field(vmanage_key="group-name")
    vpn: Optional[int]
    source_interface: Optional[str] = Field(vmanage_key="source-interface")
    server: List[RadiusServer] = []


class DomainStripping(str, Enum):
    YES = "yes"
    NO = "no"
    RIGHT_TO_LEFT = "right-to-left"


class TacacsServer(BaseModel):
    class Config:
        allow_population_by_field_name = True

    address: str
    port: int = 49
    timeout: int = Field(default=5)
    key: str
    secret_key: Optional[str] = Field(vmanage_key="secret-key", default=None)
    key_enum: Optional[str] = Field(vmanage_key="key-enum", default=None)


class TacacsGroup(BaseModel):
    class Config:
        allow_population_by_field_name = True

    group_name: str = Field(vmanage_key="group-name")
    vpn: int = 0
    source_interface: Optional[str] = Field(vmanage_key="source-interface", default=None)
    server: List[TacacsServer] = []


class CiscoAAAModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    user: List[User] = []
    authentication_group: bool = Field(vmanage_key="authentication_group", default=False)
    accounting_group: bool = True
    radius: List[RadiusGroup] = []
    domain_stripping: Optional[DomainStripping] = Field(vmanage_key="domain-stripping", default=None)
    port: int = 1700
    tacacs: List[TacacsGroup] = []
    server_auth_order: str = Field(vmanage_key="server-auth-order", default="local")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cedge_aaa"
