# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional

from attr import define, field  # type: ignore
from pydantic import ConfigDict, field_validator

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.api.templates.payloads.aaa.aaa_model import VpnType

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class GatewayType(Enum):
    NEXT_HOP = "next-hop"
    NULL_0 = "null0"
    VPN = "vpn"
    DHCP = "dhcp"


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


@define
class NextHop:
    address: str
    distance: int = 1
    en_distance: bool = False


@define
class IPv4Route:
    prefix: str
    next_hop: list[NextHop]
    gateway: GatewayType = field(default=GatewayType.NEXT_HOP)


@define
class IPv6Route:
    prefixv6: str
    next_hopv6: list[NextHop]
    gatewayv6: GatewayType = field(default=GatewayType.NEXT_HOP)


class CiscoVPNModel(FeatureTemplate):
    type: ClassVar[str] = "cisco_vpn"  # Cisco VPN
    payload_path: ClassVar[Path] = Path(__file__).parent / "feature/cisco_vpn.json.j2"
    tenant_vpn: Optional[int] = None
    tenant_org_name: Optional[str] = None
    vpn_id: int
    dns: Optional[DNS] = None
    mapping: List[Mapping] = []
    ipv4route: List[IPv4Route] = []
    ipv6route: List[IPv6Route] = []

    @field_validator("vpn_id")
    @classmethod
    def check_id(cls, v: int):
        if v not in [VpnType.VPN_TRANSPORT.value, VpnType.VPN_MANAGMENT.value]:
            if cls.tenant_org_name is None:
                raise ValueError("Must enter the name of the organization.")
        return v

    def generate_vpn_id(self, session: ManagerSession) -> None:
        self.tenant_vpn = self.vpn_id
        payload = {"resourcePoolDataType": "vpn", "tenantId": self.tenant_org_name, "tenantVpn": self.tenant_vpn}
        url = "/dataservice/resourcepool/resource/vpn"
        response = session.put(url=url, json=payload).json()
        self.vpn_id = response["deviceVpn"]

    def generate_payload(self, session: ManagerSession) -> str:
        if self.vpn_id not in [0, 512]:
            self.generate_vpn_id(session=session)
        return super().generate_payload(session)

    model_config = ConfigDict(arbitrary_types_allowed=True)
