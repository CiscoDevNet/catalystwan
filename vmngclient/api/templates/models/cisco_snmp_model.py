from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class Oid(BaseModel):
    id: str
    exclude: Optional[bool] = None


class View(BaseModel):
    name: str
    oid: Optional[List[Oid]] = None


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
    security_level: SecurityLevel = Field(alias="security-level")
    view: str
    model_config = ConfigDict(populate_by_name=True)


class Auth(str, Enum):
    MD5 = "md5"
    SHA = "sha"


class Priv(str, Enum):
    AES_CFB_128 = "aes-cfb-128"


class User(BaseModel):
    name: str
    auth: Optional[Auth] = None
    auth_password: Optional[str] = Field(None, alias="auth-password")
    priv: Optional[Priv] = None
    priv_password: Optional[str] = Field(None, alias="priv-password")
    group: str
    model_config = ConfigDict(populate_by_name=True)


class Target(BaseModel):
    vpn_id: int = Field(alias="vpn-id")
    ip: str
    port: int
    community_name: str = Field(alias="community-name")
    user: str
    source_interface: str = Field(alias="source-interface")
    model_config = ConfigDict(populate_by_name=True)


class CiscoSNMPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    shutdown: Optional[bool] = True
    contact: Optional[str]
    location: Optional[str]
    view: Optional[List[View]]
    community: Optional[List[Community]]
    group: Optional[List[Group]]
    user: Optional[List[User]]
    target: Optional[List[Target]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_snmp"
