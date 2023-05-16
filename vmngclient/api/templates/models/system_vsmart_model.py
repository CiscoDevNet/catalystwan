from pathlib import Path
from typing import ClassVar, Dict, List, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class SystemVsmart(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    key: Optional[str]
    details: Optional[str]
    option_type: Optional[List[str]] = Field(default=None, alias="optionType")
    default_option: Optional[str] = Field(default=None, alias="defaultOption")
    data_type: Optional[Dict] = Field(default=None, alias="dataType")
    data_path: Optional[List[str]] = Field(default=None, alias="dataPath")
    object_type: Optional[str] = Field(default=None, alias="objectType")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "system-vsmart"
