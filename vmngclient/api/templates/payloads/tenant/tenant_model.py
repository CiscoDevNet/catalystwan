# vipType: ignore
from pathlib import Path
from typing import List

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.dataclasses import TenantInfo


class TenantModel(FeatureTemplate):
    tenants: List[TenantInfo] = []
    payload_path: Path = Path(__file__).parent / "tenant.json.j2"

    class Config:
        arbitrary_types_allowed = True
