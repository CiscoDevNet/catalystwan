from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional

from attr import define, field
from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta

from vmngclient.dataclasses import User
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


# from vmngclient.third_parties
@define
class TacacsServer:
    address: str
    auth_port: int
    secret_key: str
    source_interface: str
    vpn: int
    priority: int


@define
class RadiusServer:
    """Default values from documentations."""

    address: str
    secret_key: str
    source_interface: Optional[str] = field(default=None)
    key: Optional[str] = field(default=None)
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


def prepare(dataclass: AttrsInstance) -> Dict[str, Any]:
    d = asdict(dataclass)
    for key, value in d.items():
        if isinstance(value, bool):
            d[key] = str(value).lower()
    return d


from enum import Enum


class FeatureTemplateType(Enum):
    aaa = aaaConfig


def create_feature_template(type: FeatureTemplateType, session, **kwargs) -> bool:
    env = Environment(
        loader=FileSystemLoader("vmngclient\\api\\templates\\payloads\\aaa\\feature\\15.0.0"),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=DebugUndefined,
    )
    env.filters['jsonify'] = json.dumps
    template = env.get_template('aaa.json.j2')
    output = template.render(kwargs)

    ast = env.parse(output)
    if meta.find_undeclared_variables(ast):
        print(meta.find_undeclared_variables(ast))
        raise Exception
    # print(output)
    config = json.loads(output)
    r = session.post("/dataservice/template/feature", json=config)
    return r.content


class Template:
    def __init__(self) -> None:
        pass


# YAML
ts1 = TacacsServer("1.1.1.1", 1, "1", "1", 1, 1)
ts2 = TacacsServer("1.1.1.2", 1, "1", "1", 1, 1)
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


import urllib3

from vmngclient.session import create_vManageSession

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "10.29.30.199"

subdomain = "apple.fruits.com"
port = 10100
username = 'admin'
password = "Cisco#123@Viptela"

session = create_vManageSession(url, username, password, port=port)

print(prepare(aaa))
print(create_feature_template(FeatureTemplateType.aaa, session, **prepare(aaa)))
