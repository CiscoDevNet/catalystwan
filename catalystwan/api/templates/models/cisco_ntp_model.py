from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel


class Server(ConvertBoolToStringModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    key: Optional[int]
    vpn: Optional[int]
    version: Optional[int]
    source_interface: Optional[str] = Field(default=None, json_schema_extra={'vmanage_key': 'source-interface'})
    prefer: Optional[bool]


class Authentication(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    number: int
    md5: str


class CiscoNTPModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    server: List[Server] = Field(default=[])
    authentication: Optional[List[Authentication]] = Field(json_schema_extra={'data_path': ['keys']})
    trusted: Optional[List[int]] = Field(json_schema_extra={'data_path': ['keys']})
    enable: Optional[bool] = Field(json_schema_extra={'data_path': ['master']})
    stratum: Optional[int] = Field(json_schema_extra={'data_path': ['master']})
    source: Optional[str] = Field(json_schema_extra={'data_path': ['master']})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ntp"
