from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class Server(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    key: Optional[int] = Field(default=None)
    vpn: Optional[int] = Field(default=0)
    version: Optional[int] = Field(default=4)
    source_interface: Optional[str] = Field(alias="source-interface", default=None)
    prefer: Optional[bool] = Field(default=False)


class Authentication(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    number: int
    md5: str


class CiscoNTPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    server: List[Server] = Field(default=[])
    authentication: List[Authentication] = Field(default=[])
    trusted: List[int] = Field(default=[])
    enable: Optional[bool] = Field(default=False)
    stratum: Optional[int] = Field(default=None)
    source: Optional[str] = Field(default=None)

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ntp"
