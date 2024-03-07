# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import List, Optional

from pydantic.v1 import BaseModel, Field

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.typed_list import DataSequence


class TLOC(BaseModel):
    color: str
    encapsulation: str


class Tier(BaseModel):
    """Endpoint: /dataservice/tier

    Since vManage 20.12 version, object has been renamed to "Resource Profile".
    """

    name: str = Field(alias="tierName")
    vpn: int
    rid: int = Field(alias="@rid")
    ipv4_route_limit_type: Optional[str] = Field(alias="ipv4RouteLimitType")
    ipv4_route_limit_threshold: Optional[int] = Field(alias="ipv4RouteLimitThreshold")
    ipv4_route_limit: Optional[int] = Field(alias="ipv4RouteLimit")
    ipv6_route_limit_type: Optional[str] = Field(alias="ipv6RouteLimitType")
    ipv6_route_limit_threshold: Optional[int] = Field(alias="ipv6RouteLimitThreshold")
    ipv6_route_limit: Optional[int] = Field(alias="ipv6RouteLimit")
    tlocs: List[TLOC] = Field(default=[])
    # New in 20.12 version
    nat_session_limit: Optional[int] = Field(alias="natSessionLimit")


class DeviceData(BaseModel):
    board_serial: Optional[str] = Field(None, alias="board-serial")
    certificate_validity: Optional[str] = Field(None, alias="certificate-validity")
    connected_vmanages: Optional[List[str]] = Field(None, alias="connectedVManages")
    control_connections: Optional[str] = Field(None, alias="controlConnections")
    device_groups: Optional[List[str]] = Field(None, alias="device-groups")
    device_model: Optional[str] = Field(None, alias="device-model")
    device_os: Optional[str] = Field(None, alias="device-os")
    device_type: Optional[str] = Field(None, alias="device-type")
    device_id: str = Field(alias="deviceId")
    domain_id: Optional[str] = Field(None, alias="domain-id")
    host_name: Optional[str] = Field(None, alias="host-name")
    is_device_geo_data: Optional[bool] = Field(None, alias="isDeviceGeoData")
    lastupdated: Optional[str] = None
    latitude: Optional[str] = None
    layout_level: Optional[int] = Field(None, alias="layoutLevel")
    local_system_ip: Optional[str] = Field(None, alias="local-system-ip")
    longitude: Optional[str] = None
    max_controllers: Optional[str] = Field(None, alias="max-controllers")
    model_sku: Optional[str] = None
    personality: Optional[str] = None
    platform: Optional[str] = None
    reachability: Optional[str] = None
    site_id: Optional[str] = Field(None, alias="site-id")
    state: Optional[str] = None
    state_description: Optional[str] = None
    status: Optional[str] = None
    status_order: Optional[str] = Field(None, alias="statusOrder")
    system_ip: Optional[str] = Field(None, alias="system-ip")
    testbed_mode: Optional[bool] = None
    timezone: Optional[str] = None
    total_cpu_count: Optional[str] = None
    uptime_date: Optional[str] = Field(None, alias="uptime-date")
    uuid: Optional[str] = None
    validity: Optional[str] = None
    version: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class MonitoringDeviceDetails(APIEndpoints):
    def add_tier(self):
        #  POST /device/tier
        ...

    def delete_tier(self):
        #  DELETE /device/tier/{tierName}
        ...

    def enable_sdavcon_device(self):
        #  POST /device/enableSDAVC/{deviceIP}/{enable}
        ...

    def generate_device_state_data(self):
        #  GET /data/device/state/{state_data_type}
        ...

    def generate_device_state_data_fields(self):
        #  GET /data/device/state/{state_data_type}/fields
        ...

    def generate_device_state_data_with_query_string(self):
        #  GET /data/device/state/{state_data_type}/query
        ...

    def get_all_device_status(self):
        #  GET /device/status
        ...

    def get_device_counters(self):
        #  GET /device/counters
        ...

    def get_device_list_as_key_value(self):
        #  GET /device/keyvalue
        ...

    def get_device_models(self):
        #  GET /device/models/{uuid}
        ...

    def get_device_only_status(self):
        #  GET /device/devicestatus
        ...

    def get_device_running_config(self):
        #  GET /device/config
        ...

    def get_device_running_config_html(self):
        #  GET /device/config/html
        ...

    def get_device_tloc_status(self):
        #  GET /device/tloc
        ...

    def get_device_tloc_util(self):
        #  GET /device/tlocutil
        ...

    def get_device_tloc_util_details(self):
        #  GET /device/tlocutil/detail
        ...

    def get_hardware_health_details(self):
        #  GET /device/hardwarehealth/detail
        ...

    def get_hardware_health_summary(self):
        #  GET /device/hardwarehealth/summary
        ...

    def get_stats_queues(self):
        #  GET /device/stats
        ...

    def get_sync_queues(self):
        #  GET /device/queues
        ...

    @get("/device/tier", "data")
    def get_tiers(self) -> DataSequence[Tier]:
        ...

    def get_unconfigured(self):
        #  GET /device/unconfigured
        ...

    def get_vmanage_system_ip(self):
        #  GET /device/vmanage
        ...

    def get_vedge_inventory(self):
        #  GET /device/vedgeinventory/detail
        ...

    def get_vedge_inventory_summary(self):
        #  GET /device/vedgeinventory/summary
        ...

    def list_all_device_models(self):
        #  GET /device/models
        ...

    @get("/device", "data")
    def list_all_devices(self) -> DataSequence[DeviceData]:
        #  GET /device
        ...

    def list_all_monitor_details_devices(self):
        #  GET /device/monitor
        ...

    def list_currently_syncing_devices(self):
        #  GET /device/sync_status
        ...

    def list_reachable_devices(self):
        #  GET /device/reachable
        ...

    def list_unreachable_devices(self):
        #  GET /device/unreachable
        ...

    def remove_unreachable_device(self):
        #  DELETE /device/unreachable/{deviceIP}
        ...

    def set_block_sync(self):
        #  POST /device/blockSync
        ...

    def sync_all_devices_mem_db(self):
        #  POST /device/syncall/memorydb
        ...
