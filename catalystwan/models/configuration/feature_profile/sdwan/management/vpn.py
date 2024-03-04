# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Default
from catalystwan.models.configuration.feature_profile.common import (
    DNSIPv4,
    DNSIPv6,
    HostMapping,
    WANIPv4StaticRoute,
    WANIPv6StaticRoute,
)


class ManagementVPN(BaseModel):
    # TODO (mlembke): vpn_id can't have other value, it needs to be constant. How to do that?
    vpn_id: Default[int] = Field(default=Default(value=512), frozen=True, alias="vpnId")
    ipv4_routes: Optional[List[WANIPv4StaticRoute]] = Field(default=[], alias="ipv4Route")
    ipv6_routes: Optional[List[WANIPv6StaticRoute]] = Field(default=[], alias="ipv6Route")
    dns_ipv4: Optional[DNSIPv4] = Field(default=None, alias="dnsIpv4")
    dns_ipv6: Optional[DNSIPv6] = Field(default=None, alias="dnsIpv6")
    new_host_mapping: Optional[List[HostMapping]] = Field(default=[], alias="newHostMapping")
    # TODO (mlembke): add interfaces
    interface: Optional[Any] = Field(default=None)
