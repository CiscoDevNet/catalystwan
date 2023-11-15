from pathlib import Path
from typing import ClassVar, Optional

from pydantic.v1 import Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class CiscoBannerModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    login_banner: Optional[str] = Field(vmanage_key="login")
    motd_banner: Optional[str] = Field(vmanage_key="motd")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_banner"
