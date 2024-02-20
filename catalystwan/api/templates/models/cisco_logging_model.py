from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel

Version = Literal["TLSv1.1", "TLSv1.2"]
AuthType = Literal["Server", "Mutual"]
Priority = Literal["information", "debugging", "notice", "warn", "error", "critical", "alert", "emergency"]


class TlsProfile(ConvertBoolToStringModel):
    profile: str
    version: Optional[Version] = Field(default="TLSv1.1", json_schema_extra={"data_path": ["tls-version"]})
    auth_type: AuthType = Field(
        validation_alias="auth-type", serialization_alias="auth-type", json_schema_extra={"vmanage_key": "auth-type"}
    )
    ciphersuite_list: Optional[List] = Field(
        default=None,
        validation_alias="ciphersuite-list",
        serialization_alias="ciphersuite-list",
        json_schema_extra={"data_path": ["ciphersuite"], "vmanage_key": "ciphersuite-list"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Server(ConvertBoolToStringModel):
    name: str
    vpn: Optional[int] = None
    source_interface: Optional[str] = Field(
        default=None,
        serialization_alias="source-interface",
        validation_alias="source-interface",
        json_schema_extra={"vmanage_key": "source-interface"},
    )
    priority: Optional[Priority] = "information"
    enable_tls: Optional[bool] = Field(
        default=False,
        serialization_alias="enable-tls",
        validation_alias="enable-tls",
        json_schema_extra={"data_path": ["tls"], "vmanage_key": "enable-tls"},
    )
    custom_profile: Optional[bool] = Field(
        default=False,
        serialization_alias="custom-profile",
        validation_alias="custom-profile",
        json_schema_extra={"data_path": ["tls", "tls-properties"], "vmanage_key": "custom-profile"},
    )
    profile: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["tls", "tls-properties"]})
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Server(ConvertBoolToStringModel):
    name: str
    vpn: Optional[int] = None
    source_interface: Optional[str] = Field(
        default=None,
        serialization_alias="source-interface",
        validation_alias="source-interface",
        json_schema_extra={"vmanage_key": "source-interface"},
    )
    priority: Optional[Priority] = "information"
    enable_tls: Optional[bool] = Field(
        default=False,
        serialization_alias="enable-tls",
        validation_alias="enable-tls",
        json_schema_extra={"data_path": ["tls"], "vmanage_key": "enable-tls"},
    )
    custom_profile: Optional[bool] = Field(
        default=False,
        serialization_alias="custom-profile",
        validation_alias="custom-profile",
        json_schema_extra={"data_path": ["tls", "tls-properties"], "vmanage_key": "custom-profile"},
    )
    profile: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["tls", "tls-properties"]})
    model_config = ConfigDict(populate_by_name=True)


class CiscoLoggingModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    enable: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["disk"]})
    size: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["disk", "file"]})
    rotate: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["disk", "file"]})
    tls_profile: Optional[List[TlsProfile]] = Field(
        default=None,
        serialization_alias="tls-profile",
        validation_alias="tls-profile",
        json_schema_extra={"vmanage_key": "tls-profile"},
    )
    server: Optional[List[Server]] = None
    ipv6_server: Optional[List[Ipv6Server]] = Field(
        default=None,
        validation_alias="ipv6-server",
        serialization_alias="ipv6-server",
        json_schema_extra={"vmanage_key": "ipv6-server"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_logging"
