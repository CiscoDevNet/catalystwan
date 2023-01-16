"""Contains a list of feature templates.

These feature template models are used to create and modify the templates
on the vManage server.

In addition, they are used to convert CLI config into separate feature
templates in vManage.
"""

# Basic FeatureTemplate class
from vmngclient.api.templates.feature_template import FeatureTemplate

# AAA Templates
from vmngclient.api.templates.payloads.aaa.aaa_model import AAAModel

# Cisco VPN Templates
from vmngclient.api.templates.payloads.cisco_vpn.cisco_vpn_model import (
    DNS,
    CiscoVPNModel,
    GatewayType,
    IPv4Route,
    IPv6Route,
    Mapping,
    NextHop,
)

# CEdge Templates
from vmngclient.api.templates.payloads.tenant.tenant_model import TenantModel

__all__ = [
    "FeatureTemplate",
    "TenantModel",
    "AAAModel",
    "CiscoVPNModel",
    "DNS",
    "Mapping",
    "IPv4Route",
    "IPv6Route",
    "GatewayType",
    "NextHop",
]
