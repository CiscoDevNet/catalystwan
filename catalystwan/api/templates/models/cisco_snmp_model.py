# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class Oid(FeatureTemplateValidator):
    id: str
    exclude: Optional[BoolStr] = None


class View(FeatureTemplateValidator):
    name: str
    oid: Optional[List[Oid]] = None


class Authorization(str, Enum):
    READ_ONLY = "read-only"


class Community(FeatureTemplateValidator):
    name: str
    view: str
    authorization: Authorization


class SecurityLevel(str, Enum):
    NOAUTHNOPRIV = "no-auth-no-priv"
    AUTHNOPRIV = "auth-no-priv"
    AUTHPRIV = "auth-priv"


class Group(FeatureTemplateValidator):
    name: str
    security_level: SecurityLevel = Field(json_schema_extra={"vmanage_key": "security-level"})
    view: str
    model_config = ConfigDict(populate_by_name=True)


class Auth(str, Enum):
    MD5 = "md5"
    SHA = "sha"


class Priv(str, Enum):
    AES_CFB_128 = "aes-cfb-128"


class User(FeatureTemplateValidator):
    name: str
    auth: Optional[Auth] = None
    auth_password: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "auth-password"})
    priv: Optional[Priv] = None
    priv_password: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "priv-password"})
    group: str
    model_config = ConfigDict(populate_by_name=True)


class Target(FeatureTemplateValidator):
    vpn_id: int = Field(json_schema_extra={"vmanage_key": "vpn-id"})
    ip: str
    port: int
    community_name: str = Field(default=None, json_schema_extra={"vmanage_key": "community-name"})
    user: Optional[str] = None
    source_interface: str = Field(default=None, json_schema_extra={"vmanage_key": "source-interface"})
    model_config = ConfigDict(populate_by_name=True)


class CiscoSNMPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    shutdown: Optional[BoolStr] = True
    contact: Optional[str] = None
    location: Optional[str] = None
    view: Optional[List[View]] = None
    community: Optional[List[Community]] = None
    group: Optional[List[Group]] = None
    user: Optional[List[User]] = None
    target: Optional[List[Target]] = Field(default=None, json_schema_extra={"data_path": ["trap"]})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_snmp"
