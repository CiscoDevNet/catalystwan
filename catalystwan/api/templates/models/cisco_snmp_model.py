from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel


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
    security_level: SecurityLevel = Field(json_schema_extra={'vmanage_key': 'security-level'})
    view: str
    model_config = ConfigDict(populate_by_name=True)


class Auth(str, Enum):
    MD5 = "md5"
    SHA = "sha"


class Priv(str, Enum):
    AES_CFB_128 = "aes-cfb-128"


class User(BaseModel):
    name: str
    auth: Optional[Auth]
    auth_password: Optional[str] = Field(json_schema_extra={'vmanage_key': 'auth-password'})
    priv: Optional[Priv]
    priv_password: Optional[str] = Field(json_schema_extra={'vmanage_key': 'priv-password'})
    group: str
    model_config = ConfigDict(populate_by_name=True)


class Target(BaseModel):
    vpn_id: int = Field(json_schema_extra={'vmanage_key': 'vpn-id'})
    ip: str
    port: int
    community_name: str = Field(json_schema_extra={'vmanage_key': 'community-name'})
    user: Optional[str]
    source_interface: str = Field(json_schema_extra={'vmanage_key': 'source-interface'})
    model_config = ConfigDict(populate_by_name=True)


class CiscoSNMPModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    shutdown: Optional[bool] = True
    contact: Optional[str]
    location: Optional[str]
    view: Optional[List[View]]
    community: Optional[List[Community]]
    group: Optional[List[Group]]
    user: Optional[List[User]]
    target: Optional[List[Target]] = Field(json_schema_extra={'data_path': ['trap']})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_snmp"
