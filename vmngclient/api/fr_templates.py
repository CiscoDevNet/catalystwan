from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional

import urllib3
from attr import define, field

from vmngclient.api.templates import DNS, Mapping, VPNModel
from vmngclient.dataclasses import User
from vmngclient.session import create_vManageSession
from vmngclient.utils.creation_tools import AttrsInstance, asdict


class AuthenticationOrder(Enum):
    LOCAL = "local"
    RADIUS = "radius"
    TACACS = "tacacs"


class TacacsAuthenticationMethod(Enum):
    PAP = "pap"


class Action(Enum):
    ACCEPT = "accept"
    DENY = "deny"


class VpnType(Enum):
    VPN_TRANSPORT = 0
    VPN_MANAGMENT = 512


# from vmngclient.third_parties
@define
class TacacsServer:
    """Default values from documentations."""

    address: str
    auth_port: int = field(default=49)
    secret_key: Optional[str] = field(default=None)
    source_interface: Optional[str] = field(default=None)
    vpn: int = field(default=0)
    priority: int = field(default=0)


@define
class RadiusServer:
    """Default values from documentations."""

    address: str
    secret_key: Optional[str] = field(default=None)
    source_interface: Optional[str] = field(default=None)
    acct_port: int = field(default=1813)
    auth_port: int = field(default=1812)
    tag: Optional[str] = field(default=None)
    timeout: int = field(default=5)
    vpn: int = field(default=0)
    priority: int = field(default=0)


@define
class AuthTask:
    name: str
    default_action: Action = field(default=Action.ACCEPT)


@define
class aaaConfig:
    template_name: str
    template_description: str

    auth_order: List[AuthenticationOrder]
    auth_fallback: bool
    auth_disable_audit_logs: bool
    auth_admin_order: bool
    auth_disable_netconf_logs: bool
    auth_radius_servers: List[str] = field(factory=list)

    local_users: List[User] = field(factory=list)

    accounting: bool = field(default=True)

    tacacs_authentication: TacacsAuthenticationMethod = field(default=TacacsAuthenticationMethod.PAP)
    tacacs_timeout: int = field(default=5)
    tacacs_servers: List[TacacsServer] = field(factory=list)
    radius_retransmit: int = field(default=3)
    radius_timeout: int = field(default=5)
    radius_servers: List[RadiusServer] = field(factory=list)


# @define
# class vpnConfig:
#     template_name: str
#     template_description: str

#     vpn_id: VpnType
#     tenant_vpn: Optional[int] = field(default=None)
#     org_name: Optional[str] = field(default=None)
#     dns: Optional[Dns] = field(default=None)
#     mapping: List[Mapping] = field(factory=list)


# @define
# class Dns:
#     primary: str
#     secondary: Optional[str] = field(default=None)
#     primaryv6: Optional[str] = field(default=None)
#     secondaryv6: Optional[str] = field(default=None)


# @define
# class Mapping:
#     name: str
#     ips: List[str] = field(factory=list)


def prepare(dataclass: AttrsInstance) -> Dict[str, Any]:
    d = asdict(dataclass)
    for key, value in d.items():
        if isinstance(value, bool):
            d[key] = str(value).lower()
    return d


class FeatureTemplateType(Enum):
    aaa = aaaConfig
    vpn = VPNModel


def create_feature_template(output, session, **kwargs) -> bool:

    config = json.loads(output)
    r = session.post("/dataservice/template/feature", json=config)
    return r.content


class Template:
    def __init__(self) -> None:
        pass


# YAML
ts1 = TacacsServer(address="1.1.1.1")
ts2 = TacacsServer(address="1.1.1.2")
ltss = [ts1, ts2]

rs1 = RadiusServer(address="1.1.1.1", secret_key="1")
rs2 = RadiusServer(address="1.1.1.2", secret_key="2")
lrss = [rs1, rs2]

u1 = User(group=['a'], username="test", password="me1", description="default", locale='cos')

u2 = User(group=['b'], username="test2", password="me2", description="default2", locale='cos')

users = [u1, u2]

aaa = aaaConfig(
    template_name="aaa",
    template_description="template aaa desc.",
    auth_order=[AuthenticationOrder.LOCAL, AuthenticationOrder.RADIUS, AuthenticationOrder.TACACS],  # LRT default
    auth_fallback=False,
    auth_admin_order=True,
    auth_disable_audit_logs=False,
    local_users=users,
    auth_disable_netconf_logs=False,
    auth_radius_servers=["1.1.1.1", "2.2.3.4"],
    tacacs_servers=ltss,
    radius_servers=lrss,
)

dns1 = DNS(
    primary="192.168.1.1",
    secondary="192.168.1.2",
    primaryv6="2001:db8:bad:cab1:e001::41",
    secondaryv6="2001:db8:bad:cab1:e001::42",
)

mapping1 = Mapping("test_map1", ips=["192.168.2.1"])
mapping2 = Mapping("test_map2", ips=["192.168.2.2"])
map = [mapping1, mapping2]
vpn_transport = VPNModel(name="vpn_transport_test", description="vpn_transport_test", id=0, dns=dns1, mapping=map)
print(vpn_transport)
payload = vpn_transport.generate_payload()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "10.29.30.199"

subdomain = "apple.fruits.com"
port = 10100
username = 'admin'
password = "Cisco#123@Viptela"

session = create_vManageSession(url, username, password, port=port)

# print(prepare(aaa))
# print(prepare(vpn_transport))
# print(create_feature_template(FeatureTemplateType.aaa, session, **prepare(aaa)))
print()
print(create_feature_template(payload, session))
