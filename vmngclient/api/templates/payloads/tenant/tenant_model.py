# vipType: ignore
from pathlib import Path
from typing import ClassVar, List

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.dataclasses import TenantInfo, TierInfo
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass


# Tenant tier-name without tlocs
class TenantModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True

    tenants: List[TenantInfo] = []
    payload_path: ClassVar[Path] = Path(__file__).parent / "tenant.json.j2"
    tiers: List[TierInfo] = []

    def generate_payload(self, session: vManageSession) -> str:
        tiers_json = session.get_data("dataservice/device/tier")
        self.tiers = [create_dataclass(TierInfo, tier) for tier in tiers_json]
        return super().generate_payload(session)
