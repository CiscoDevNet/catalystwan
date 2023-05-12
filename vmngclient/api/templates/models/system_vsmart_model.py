from pathlib import Path
from typing import ClassVar

from vmngclient.api.templates.feature_template import FeatureTemplate


class SystemVsmart(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "system-vsmart"
