# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.timezone import Timezone


class SystemVsmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    timezone: Optional[Timezone] = Field(default=None)
    idle_timeout: Optional[int] = Field(default=None, ge=0, le=300, json_schema_extra={"vmanage_key": "idle-timeout"})
    admin_tech_on_failure: Optional[bool] = Field(
        default=True, json_schema_extra={"vmanage_key": "admin-tech-on-failure"}
    )
    iptables_enable: Optional[bool] = Field(default=True, json_schema_extra={"vmanage_key": "iptables-enable"})
    track_default_gateway: Optional[bool] = Field(
        default=True, json_schema_extra={"vmanage_key": "track-default-gateway"}
    )
    dns_cache_timeout: Optional[int] = Field(
        default=2, ge=1, le=30, json_schema_extra={"vmanage_key": "dns-cache-timeout"}
    )
    track_transport: Optional[bool] = Field(default=True, json_schema_extra={"vmanage_key": "track-transport"})
    controller_group_id: Optional[int] = Field(
        default=0, ge=0, le=100, json_schema_extra={"vmanage_key": "controller-group-id"}
    )
    control_session_pps: Optional[int] = Field(default=300, json_schema_extra={"vmanage_key": "control-session-pps"})
    port_hop: Optional[bool] = Field(default=True, json_schema_extra={"vmanage_key": "port-hop"})
    port_offset: Optional[int] = Field(default=0, ge=0, le=20, json_schema_extra={"vmanage_key": "port-offset"})
    overlay_id: Optional[int] = Field(default=1, ge=1, le=4294967295, json_schema_extra={"vmanage_key": "overlay-id"})
    site_id: Optional[int] = Field(default=1, ge=1, le=4294967295, json_schema_extra={"vmanage_key": "site-id"})
    system_ip: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "system-ip"})
    device_groups: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "device-groups"})
    longitude: Optional[int] = Field(default=None, ge=-180, le=180)
    latitude: Optional[int] = Field(default=None, ge=-90, le=90)
    system_tunnel_mtu: Optional[str] = Field(default=1024, json_schema_extra={"vmanage_key": "system-tunnel-mtu"})
    location: Optional[str] = None
    host_name: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "host-name"})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "system-vsmart"
