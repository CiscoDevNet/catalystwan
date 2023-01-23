from functools import lru_cache
from pathlib import Path
from typing import ClassVar, List

from pydantic import BaseModel  # type: ignore

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.api.tenant_api import TenantsAPI
from vmngclient.dataclasses import TenantInfo, TierInfo
from vmngclient.session import vManageSession


@lru_cache
def get_tenants(session: vManageSession) -> List[TenantInfo]:
    tenants_api = TenantsAPI(session)
    return tenants_api.get_tenants()


@lru_cache
def get_tiers(session: vManageSession) -> List[TierInfo]:
    tenants_api = TenantsAPI(session)
    return tenants_api.get_tiers()


class Tenant(BaseModel):
    """Tenant definition without TLOCs."""

    organization_name: str
    tier_name: str


class TenantModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True

    payload_path: ClassVar[Path] = Path(__file__).parent / "tenant.json.j2"

    tenants: List[Tenant] = []

    def generate_payload(self, session: vManageSession) -> str:
        tenants_api = TenantsAPI(session)

        for tenant in self.tenants:
            tier_info = tenants_api.get_tier(tenant.tier_name)
            tenant_info = tenants_api.get_tenant(organization_name=tenant.organization_name)
            # TODO Very, very ugly way...
            tenant.__dict__["tier"] = tier_info
            tenant.__dict__["info"] = tenant_info

        return super().generate_payload(session)
