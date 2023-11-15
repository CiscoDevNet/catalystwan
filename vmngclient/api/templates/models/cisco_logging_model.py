from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic.v1 import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


class Version(str, Enum):
    TLSV11 = "TLSv1.1"
    TLSV12 = "TLSv1.2"


class AuthType(str, Enum):
    SERVER = "Server"
    MUTUAL = "Mutual"


class TlsProfile(ConvertBoolToStringModel):
    profile: str
    version: Optional[Version] = Field(Version.TLSV11, data_path=["tls-version"])
    auth_type: AuthType = Field(vmanage_key="auth-type")
    ciphersuite_list: Optional[List] = Field(data_path=["ciphersuite"], vmanage_key="ciphersuite-list")

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
    source_interface: Optional[str] = Field(vmanage_key="source-interface")
    priority: Optional[Priority] = Priority.INFORMATION
    enable_tls: Optional[bool] = Field(False, data_path=["tls"], vmanage_key="enable-tls")
    custom_profile: Optional[bool] = Field(False, data_path=["tls", "tls-properties"], vmanage_key="custom-profile")
    profile: Optional[str] = Field(data_path=["tls", "tls-properties"])

    class Config:
        allow_population_by_field_name = True


class Ipv6Server(ConvertBoolToStringModel):
    name: str
    vpn: Optional[int]
    source_interface: Optional[str] = Field(vmanage_key="source-interface")
    priority: Optional[Priority] = Priority.INFORMATION
    enable_tls: Optional[bool] = Field(False, data_path=["tls"], vmanage_key="enable-tls")
    custom_profile: Optional[bool] = Field(False, data_path=["tls", "tls-properties"], vmanage_key="custom-profile")
    profile: Optional[str] = Field(data_path=["tls", "tls-properties"])

    class Config:
        allow_population_by_field_name = True


class CiscoLoggingModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    enable: Optional[bool] = Field(data_path=["disk"])
    size: Optional[int] = Field(data_path=["disk", "file"])
    rotate: Optional[int] = Field(data_path=["disk", "file"])
    tls_profile: Optional[List[TlsProfile]] = Field(vmanage_key="tls-profile")
    server: Optional[List[Server]]
    ipv6_server: Optional[List[Ipv6Server]] = Field(vmanage_key="ipv6-server")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_logging"
