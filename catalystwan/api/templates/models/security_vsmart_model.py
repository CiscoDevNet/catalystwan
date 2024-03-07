# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate


class Protocol(str, Enum):
    DTLS: str = "dtls"
    TLS: str = "tls"


class SecurityvSmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Optional[Protocol] = Field(default=None, json_schema_extra={"data_path": ["control"]})
    tls_port: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "tls-port", "data_path": ["control"]}
    )
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "security-vsmart"
