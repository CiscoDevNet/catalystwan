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
    pubkey_chain: List[str] = Field(default=[], alias="pubkey-chain")


class RadiusServer(BaseModel):
    class Config:
        allow_population_by_field_name = True

    address: str
    auth_port: int = Field(alias="auth-port", default=1812)
    acct_port: int = Field(alias="acct-port", default=1813)
    timeout: int = Field(default=5)
    retransmit: int = 3
    key: str
    secret_key: Optional[str] = Field(alias="secret-key", default=None)
    key_enum: Optional[str] = Field(alias="key-enum", default=None)
    key_type: Optional[str] = Field(alias="key-type", default=None)


class RadiusGroup(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    group_name: str = Field(alias="group-name")
    vpn: Optional[int]
    source_interface: Optional[str] = Field(alias="source-interface")
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
    secret_key: Optional[str] = Field(alias="secret-key", default=None)
    key_enum: Optional[str] = Field(alias="key-enum", default=None)


class TacacsGroup(BaseModel):
    group_name: str = Field(alias="group-name")
    vpn: int = 0
    source_interface: Optional[str] = Field(alias="source-interface", default=None)
    server: List[TacacsServer] = []


class CiscoAAAModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    user: List[User] = []
    authentication_group: bool = Field(alias="authentication_group", default=False)
    accounting_group: bool = True
    radius: List[RadiusGroup] = []
    domain_stripping: Optional[DomainStripping] = Field(alias="domain-stripping", default=None)
    port: int = 1700
    tacacs: List[TacacsGroup] = []

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cedge_aaa"
