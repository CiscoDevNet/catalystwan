# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.endpoints.monitoring_device_details import Tier as TierInfo
from catalystwan.models.tenant import Tenant as TenantInfo

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class Tenant(BaseModel):
    """Tenant definition without TLOCs."""

    organization_name: str
    tier_name: str
    tenant_info: Optional[TenantInfo]
    tier_info: Optional[TierInfo]


class TenantModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: ClassVar[str] = "tenant"  # Tenant
    payload_path: ClassVar[Path] = Path(__file__).parent / "tenant.json.j2"

    tenants: List[Tenant] = []

    def generate_payload(self, session: ManagerSession) -> str:
        tenant_infos = session.endpoints.tenant_management.get_all_tenants()
        tier_infos = session.endpoints.monitoring_device_details.get_tiers()

        for tenant in self.tenants:
            tenant.tier_info = tier_infos.filter(name=tenant.tier_name).single_or_default()
            tenant.tenant_info = tenant_infos.filter(org_name=tenant.organization_name).single_or_default()

        return super().generate_payload(session)
