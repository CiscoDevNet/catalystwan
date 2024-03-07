# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class Version(str, Enum):
    TLSV11 = "TLSv1.1"
    TLSV12 = "TLSv1.2"


class AuthType(str, Enum):
    SERVER = "Server"
    MUTUAL = "Mutual"


class TlsProfile(FeatureTemplateValidator):
    profile: str
    version: Optional[Version] = Field(Version.TLSV11, json_schema_extra={"data_path": ["tls-version"]})
    auth_type: AuthType = Field(json_schema_extra={"vmanage_key": "auth-type"})
    ciphersuite_list: Optional[List] = Field(
        default=None, json_schema_extra={"data_path": ["ciphersuite"], "vmanage_key": "ciphersuite-list"}
    )
    model_config = ConfigDict(populate_by_name=True)


class Priority(str, Enum):
    INFORMATION = "information"
    DEBUGGING = "debugging"
    NOTICE = "notice"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"
    ALERT = "alert"
    EMERGENCY = "emergency"


class Server(FeatureTemplateValidator):
    name: str
    vpn: Optional[int] = None
    source_interface: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "source-interface"})
    priority: Optional[Priority] = Priority.INFORMATION
    enable_tls: Optional[BoolStr] = Field(
        default=False, json_schema_extra={"data_path": ["tls"], "vmanage_key": "enable-tls"}
    )
    custom_profile: Optional[BoolStr] = Field(
        default=False, json_schema_extra={"data_path": ["tls", "tls-properties"], "vmanage_key": "custom-profile"}
    )
    profile: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["tls", "tls-properties"]})
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Server(FeatureTemplateValidator):
    name: str
    vpn: Optional[int] = None
    source_interface: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "source-interface"})
    priority: Optional[Priority] = Priority.INFORMATION
    enable_tls: Optional[BoolStr] = Field(
        default=False, json_schema_extra={"data_path": ["tls"], "vmanage_key": "enable-tls"}
    )
    custom_profile: Optional[BoolStr] = Field(
        default=False, json_schema_extra={"data_path": ["tls", "tls-properties"], "vmanage_key": "custom-profile"}
    )
    profile: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["tls", "tls-properties"]})
    model_config = ConfigDict(populate_by_name=True)


class CiscoLoggingModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    enable: Optional[BoolStr] = Field(default=None, json_schema_extra={"data_path": ["disk"]})
    size: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["disk", "file"]})
    rotate: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["disk", "file"]})
    tls_profile: Optional[List[TlsProfile]] = Field(default=None, json_schema_extra={"vmanage_key": "tls-profile"})
    server: Optional[List[Server]] = None
    ipv6_server: Optional[List[Ipv6Server]] = Field(default=None, json_schema_extra={"vmanage_key": "ipv6-server"})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_logging"
