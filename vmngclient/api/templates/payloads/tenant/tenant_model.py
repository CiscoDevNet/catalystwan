from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List

from pydantic import BaseModel

from vmngclient.api.templates.feature_template import FeatureTemplate

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class Tenant(BaseModel):
    """Tenant definition without TLOCs."""

    organization_name: str
    tier_name: str


class TenantModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True

    type: ClassVar[str] = "tenant"  # Tenant
    payload_path: ClassVar[Path] = Path(__file__).parent / "tenant.json.j2"

    tenants: List[Tenant] = []

    def generate_payload(self, session: vManageSession) -> str:
        tenant_infos = session.primitives.tenant_management.get_all_tenants()
        tier_infos = session.primitives.monitoring_device_details.get_tiers()

        for tenant in self.tenants:
            tier_info = tier_infos.filter(name=tenant.tier_name).single_or_default()
            tenant_info = tenant_infos.filter(org_name=tenant.organization_name).single_or_default()
            # TODO Very, very ugly way...
            tenant.__dict__["tier"] = tier_info
            tenant.__dict__["info"] = tenant_info

        return super().generate_payload(session)
