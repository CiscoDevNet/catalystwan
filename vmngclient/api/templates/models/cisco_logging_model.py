from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel

DEFAULT_LOGGING_SIZE = 10
DEFAULT_LOGGING_ROTATE = 10


class Version(str, Enum):
    TLSV11 = "TLSv1.1"
    TLSV12 = "TLSv1.2"


class AuthType(str, Enum):
    SERVER = "Server"
    MUTUAL = "Mutual"


class TlsProfile(ConvertBoolToStringModel):
    profile: str
    version: Optional[Version] = Version.TLSV11
    auth_type: AuthType = Field(alias="auth-type")
    ciphersuite_list: Optional[List] = Field(alias="ciphersuite-list")

    class Config:
        allow_population_by_field_name = True


class Priority(str, Enum):
    INFORMATION = "information"
    DEBUGGING = "debugging"
    NOTICE = "notice"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"
    ALERT = "alert"
    EMERGENCY = "emergency"


class Server(ConvertBoolToStringModel):
    name: str
    vpn: Optional[int]
    source_interface: Optional[str] = Field(alias="source-interface")
    priority: Optional[Priority] = Priority.INFORMATION
    enable_tls: Optional[bool] = Field(False, alias="enable-tls")
    custom_profile: Optional[bool] = Field(False, alias="custom-profile")
    profile: Optional[str]

    class Config:
        allow_population_by_field_name = True


class Ipv6Server(ConvertBoolToStringModel):
    name: str
    vpn: Optional[int]
    source_interface: Optional[str] = Field(alias="source-interface")
    priority: Optional[Priority] = Priority.INFORMATION
    enable_tls: Optional[bool] = Field(False, alias="enable-tls")
    custom_profile: Optional[bool] = Field(False, alias="custom-profile")
    profile: Optional[str]

    class Config:
        allow_population_by_field_name = True


class CiscoLoggingModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    enable: Optional[bool] = True
    size: Optional[int] = DEFAULT_LOGGING_SIZE
    rotate: Optional[int] = DEFAULT_LOGGING_ROTATE
    tls_profile: List[TlsProfile] = Field(alias="tls-profile")
    server: Optional[List[Server]]
    ipv6_server: Optional[List[Ipv6Server]] = Field(alias="ipv6-server")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_logging"
