from pathlib import Path
from typing import ClassVar, Optional

from pydantic.v1 import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.timezone import Timezone


class SystemVsmart(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    timezone: Optional[Timezone] = Field(default=None, converter=Timezone)
    idle_timeout: Optional[int] = Field(default=None, vmanage_key="idle-timeout", ge=0, le=300)
    admin_tech_on_failure: Optional[bool] = Field(default=True, vmanage_key="admin-tech-on-failure")
    iptables_enable: Optional[bool] = Field(default=True, vmanage_key="iptables-enable")
    track_default_gateway: Optional[bool] = Field(default=True, vmanage_key="track-default-gateway")
    dns_cache_timeout: Optional[int] = Field(default=2, vmanage_key="dns-cache-timeout", ge=1, le=30)
    track_transport: Optional[bool] = Field(default=True, vmanage_key="track-transport")
    controller_group_id: Optional[int] = Field(default=0, vmanage_key="controller-group-id", ge=0, le=100)
    control_session_pps: Optional[int] = Field(default=300, vmanage_key="control-session-pps")
    port_hop: Optional[bool] = Field(default=True, vmanage_key="port-hop")
    port_offset: Optional[int] = Field(default=0, vmanage_key="port-offset", ge=0, le=20)
    overlay_id: Optional[int] = Field(default=1, vmanage_key="overlay-id", ge=1, le=4294967295)
    site_id: Optional[int] = Field(default=1, vmanage_key="site-id", ge=1, le=4294967295)
    system_ip: Optional[str] = Field(default=None, vmanage_key="system-ip")
    device_groups: Optional[str] = Field(default=None, vmanage_key="device-groups")
    longitude: Optional[int] = Field(ge=-180, le=180)
    latitude: Optional[int] = Field(ge=-90, le=90)
    system_tunnel_mtu: Optional[str] = Field(default=1024, vmanage_key="system-tunnel-mtu")
    location: Optional[str]
    host_name: Optional[str] = Field(default=None, vmanage_key="host-name")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "system-vsmart"
