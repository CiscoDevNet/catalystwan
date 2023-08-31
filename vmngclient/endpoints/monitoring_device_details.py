# mypy: disable-error-code="empty-body"
from typing import List, Optional

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get
from vmngclient.typed_list import DataSequence


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

    def list_all_devices(self):
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
