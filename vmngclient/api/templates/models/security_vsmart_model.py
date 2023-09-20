from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class Protocol(Enum):
    DTLS: str = "DTLS"
    TLS: str = "TLS"


class SecurityvSmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Optional[Protocol] = Field(default=None, converter=Protocol)
    tls_port: Optional[int] = Field(default=None, alias="tls-port")
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "security-vsmart"
