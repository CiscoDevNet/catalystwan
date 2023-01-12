# vipType: ignore
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from attr import define, field

from vmngclient.api.templates.feature_template import FeatureTemplate


@define
class Mapping:
    name: str
    ips: List[str] = field(factory=list)


@define
class DNS:
    primary: str
    secondary: Optional[str] = None
    primaryv6: Optional[str] = None
    secondaryv6: Optional[str] = None


class CiscoVPNModel(FeatureTemplate):
    payload_path: Path = Path(__file__).parent / "feature/cisco_vpn.json.j2"
    id: int
    tenant_vpn: Optional[int] = None
    tenant_org_name: Optional[str] = None
    dns: Optional[DNS] = None
    mapping: List[Mapping] = []

    class Config:
        arbitrary_types_allowed = True
