# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate


class CiscoBannerModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    login_banner: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "login"})
    motd_banner: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "motd"})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_banner"
