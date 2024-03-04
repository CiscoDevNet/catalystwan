# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from attr import define, field  # type: ignore
from pydantic import ConfigDict

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.dataclasses import User


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


class AAAModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    payload_path: ClassVar[Path] = Path(__file__).parent / "feature" / "aaa.json.j2"
    type: ClassVar[str] = "aaa"  # AAA

    auth_order: List[AuthenticationOrder]
    auth_fallback: bool
    auth_disable_audit_logs: bool
    auth_admin_order: bool
    auth_disable_netconf_logs: bool
    auth_radius_servers: List[str] = []

    local_users: List[User] = []

    accounting: bool = True

    tacacs_authentication: TacacsAuthenticationMethod = TacacsAuthenticationMethod.PAP
    tacacs_timeout: int = 5
    tacacs_servers: List[TacacsServer] = []
    radius_retransmit: int = 3
    radius_timeout: int = 5
    radius_servers: List[RadiusServer] = []
