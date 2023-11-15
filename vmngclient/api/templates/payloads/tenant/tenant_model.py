from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional

from pydantic.v1 import BaseModel

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.endpoints.monitoring_device_details import Tier as TierInfo
from vmngclient.model.tenant import Tenant as TenantInfo

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class Tenant(BaseModel):
    """Tenant definition without TLOCs."""

    organization_name: str
    tier_name: str
    tenant_info: Optional[TenantInfo]
    tier_info: Optional[TierInfo]


class TenantModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True

    type: ClassVar[str] = "tenant"  # Tenant
    payload_path: ClassVar[Path] = Path(__file__).parent / "tenant.json.j2"

    tenants: List[Tenant] = []

    def generate_payload(self, session: vManageSession) -> str:
        tenant_infos = session.endpoints.tenant_management.get_all_tenants()
        tier_infos = session.endpoints.monitoring_device_details.get_tiers()

        for tenant in self.tenants:
            tenant.tier_info = tier_infos.filter(name=tenant.tier_name).single_or_default()
            tenant.tenant_info = tenant_infos.filter(org_name=tenant.organization_name).single_or_default()

        return super().generate_payload(session)
