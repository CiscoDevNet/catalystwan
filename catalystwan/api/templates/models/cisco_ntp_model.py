# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class Server(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    key: Optional[int] = None
    vpn: Optional[int] = None
    version: Optional[int] = None
    source_interface: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "source-interface"})
    prefer: Optional[BoolStr] = None


class Authentication(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    number: int
    md5: str


class CiscoNTPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    server: List[Server] = Field(default=[])
    authentication: Optional[List[Authentication]] = Field(default=None, json_schema_extra={"data_path": ["keys"]})
    trusted: Optional[List[int]] = Field(default=None, json_schema_extra={"data_path": ["keys"]})
    enable: Optional[BoolStr] = Field(default=None, json_schema_extra={"data_path": ["master"]})
    stratum: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["master"]})
    source: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["master"]})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ntp"
