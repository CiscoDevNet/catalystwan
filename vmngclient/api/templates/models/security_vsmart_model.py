from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional

from pydantic.v1 import Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class Protocol(str, Enum):
    DTLS: str = "dtls"
    TLS: str = "tls"


class SecurityvSmart(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    protocol: Optional[Protocol] = Field(default=None, data_path=["control"])
    tls_port: Optional[int] = Field(default=None, vmanage_key="tls-port", data_path=["control"])
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "security-vsmart"
