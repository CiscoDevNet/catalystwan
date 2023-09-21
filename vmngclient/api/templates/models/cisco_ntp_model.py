from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


class Server(ConvertBoolToStringModel):
    class Config:
        allow_population_by_field_name = True

    name: str
    key: Optional[int] = Field(default=None)
    vpn: Optional[int] = Field(default=0)
    version: Optional[int] = Field(default=4)
    source_interface: Optional[str] = Field(vmanage_key="source-interface", default=None)
    prefer: Optional[bool] = Field(default=False)


class Authentication(BaseModel):
    class Config:
        allow_population_by_field_name = True

    number: int
    md5: str


class CiscoNTPModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    server: List[Server] = Field(default=[])
    authentication: List[Authentication] = Field(default=[], data_path=["keys"])
    trusted: List[int] = Field(default=[], data_path=["keys"])
    enable: Optional[bool] = Field(default=False, data_path=["master"])
    stratum: Optional[int] = Field(default=None, data_path=["master"])
    source: Optional[str] = Field(default=None, data_path=["master"])

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ntp"
