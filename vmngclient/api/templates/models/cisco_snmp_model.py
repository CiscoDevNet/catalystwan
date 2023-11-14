from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


class Oid(ConvertBoolToStringModel):
    id: str
    exclude: Optional[bool]


class View(BaseModel):
    name: str
    oid: Optional[List[Oid]]


class Authorization(str, Enum):
    READ_ONLY = "read-only"


class Community(BaseModel):
    name: str
    view: str
    authorization: Authorization


class SecurityLevel(str, Enum):
    NOAUTHNOPRIV = "no-auth-no-priv"
    AUTHNOPRIV = "auth-no-priv"
    AUTHPRIV = "auth-priv"


class Group(BaseModel):
    name: str
    security_level: SecurityLevel = Field(vmanage_key="security-level")
    view: str

    class Config:
        allow_population_by_field_name = True


class Auth(str, Enum):
    MD5 = "md5"
    SHA = "sha"


class Priv(str, Enum):
    AES_CFB_128 = "aes-cfb-128"


class User(BaseModel):
    name: str
    auth: Optional[Auth]
    auth_password: Optional[str] = Field(vmanage_key="auth-password")
    priv: Optional[Priv]
    priv_password: Optional[str] = Field(vmanage_key="priv-password")
    group: str

    class Config:
        allow_population_by_field_name = True


class Target(BaseModel):
    vpn_id: int = Field(vmanage_key="vpn-id")
    ip: str
    port: int
    community_name: str = Field(vmanage_key="community-name")
    user: Optional[str]
    source_interface: str = Field(vmanage_key="source-interface")

    class Config:
        allow_population_by_field_name = True


class CiscoSNMPModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    shutdown: Optional[bool] = True
    contact: Optional[str]
    location: Optional[str]
    view: Optional[List[View]]
    community: Optional[List[Community]]
    group: Optional[List[Group]]
    user: Optional[List[User]]
    target: Optional[List[Target]] = Field(data_path=["trap"])

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_snmp"
