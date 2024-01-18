# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, get, post
from vmngclient.typed_list import DataSequence


class ProcessId(BaseModel):
    id: str


class GroupId(BaseModel):
    group_id: str = Field(default="all", serialization_alias="groupIP")


class DeviceType(str, Enum):
    VEDGE = "vedge"
    CONTROLLER = "controller"
    VMANAGE = "vmanage"


class ZTPUpgradeSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    version_id: str = Field(alias="versionId")
    platform_family: str = Field(alias="platformFamily")
    enable_upgrade: bool = Field(alias="enableUpgrade")
    version_name: str = Field(alias="versionName")


class Device(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    version: str
    device_ip: str = Field(alias="deviceIP")
    device_id: str = Field(alias="deviceId")


class PartitionActionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action: str
    devices: List[Device]
    device_type: DeviceType = Field(alias="deviceType")


class Data(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    family: str
    version: str
    version_id: str = Field(alias="versionId")


class InstallInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    v_edge_vpn: int = Field(alias="vEdgeVPN")
    v_smart_vpn: int = Field(alias="vSmartVPN")
    data: List[Data]
    version_type: str = Field(alias="versionType")
    reboot: bool
    sync: bool


class InstallDevice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_ip: str = Field(alias="deviceIP")
    device_id: str = Field(alias="deviceId")
    is_nutella_migration: Optional[bool] = Field(alias="isNutellaMigration")


class InstallActionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action: str
    input: InstallInput
    devices: List[InstallDevice]
    device_type: str = Field(alias="deviceType")


class InstalledDeviceData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_model: Optional[str] = Field(None, alias="device-model")
    device_os: Optional[str] = Field(None, alias="device-os")
    local_system_ip: Optional[str] = Field(None, alias="local-system-ip")
    system_ip: Optional[str] = Field(None, alias="system-ip")
    site_id: Optional[str] = Field(None, alias="site-id")
    uuid: Optional[str]
    platform: Optional[str]
    is_schedule_upgrade_supported: Optional[bool] = Field(None, alias="isScheduleUpgradeSupported")
    personality: Optional[str]
    device_type: Optional[str] = Field(None, alias="device-type")
    reachability: Optional[str]
    available_versions: Optional[List[str]] = Field(None, alias="availableVersions")
    host_name: Optional[str] = Field(None, alias="host-name")
    version: Optional[str]
    layout_level: Optional[int] = Field(None, alias="layoutLevel")
    uptime_date: Optional[int] = Field(None, alias="uptime-date")
    is_multi_step_upgrade_supported: Optional[bool] = Field(None, alias="isMultiStepUpgradeSupported")
    default_version: Optional[str] = Field(None, alias="defaultVersion")
    platform_family: Optional[str] = Field(None, alias="platformFamily")
    current_partition: Optional[str] = Field(None, alias="current-partition")


class ConfigurationDeviceActions(APIEndpoints):
    def create_filter_vpn_list(self):
        # GET /device/action/filter/vpn
        ...

    def create_unique_vpn_list(self):
        # POST /device/action/uniquevpnlist
        ...

    def create_vpn_list(self):
        # GET /device/action/vpn
        ...

    def generate_change_partition_info(self):
        # GET /device/action/changepartition
        ...

    def generate_deactivate_info(self):
        # GET /device/action/deactivate
        ...

    def generate_device_action_list(self):
        # GET /device/action/list
        ...

    @get("/device/action/install/devices/{device_type}", "data")
    def get_list_of_installed_devices(
        self, device_type: DeviceType, params: GroupId = GroupId()
    ) -> DataSequence[InstalledDeviceData]:
        ...

    def generate_install_info(self):
        # GET /device/action/install
        ...

    def generate_reboot_device_list(self):
        # GET /device/action/reboot/devices/{deviceType}
        ...

    def generate_reboot_info(self):
        # GET /device/action/reboot
        ...

    def generate_rediscover_info(self):
        # GET /device/action/rediscover
        ...

    def generate_remove_partition_info(self):
        # GET /device/action/removepartition
        ...

    def generate_security_devices_list(self):
        # GET /device/action/security/devices/{policyType}
        ...

    def get_ztp_upgrade_config(self):
        # GET /device/action/ztp/upgrade
        ...

    @get("/device/action/ztp/upgrade/setting", "data")
    def get_ztp_upgrade_config_setting(self) -> DataSequence[ZTPUpgradeSettings]:
        ...

    def initiate_image_download(self):
        # POST /device/action/image-download
        ...

    def process_amp_api_re_key(self):
        # POST /device/action/security/amp/rekey
        ...

    def process_cancel_task(self):
        # POST /device/action/cancel
        ...

    def process_change_partition(self):
        # POST /device/action/changepartition
        ...

    def process_deactivate_smu(self):
        # POST /device/action/deactivate
        ...

    @post("/device/action/defaultpartition")
    def process_mark_default_partition(self, payload: List[PartitionActionPayload]) -> None:
        ...

    def process_delete_amp_api_key(self):
        # DELETE /device/action/security/amp/apikey/{uuid}
        ...

    @post("/device/action/install", "data")
    def process_install_operation(self, payload: InstallActionPayload) -> ProcessId:
        ...

    def process_lxc_activate(self):
        # POST /device/action/lxcactivate
        ...

    def process_lxc_delete(self):
        # POST /device/action/lxcdelete
        ...

    def process_lxc_install(self):
        # POST /device/action/lxcinstall
        ...

    def process_lxc_reload(self):
        # POST /device/action/lxcreload
        ...

    def process_lxc_reset(self):
        # POST /device/action/lxcreset
        ...

    def process_lxc_upgrade(self):
        # POST /device/action/lxcupgrade
        ...

    def process_reboot(self):
        # POST /device/action/reboot
        ...

    def process_remove_partition(self):
        # POST /device/action/removepartition
        ...

    def process_remove_software_image(self):
        # POST /device/action/image-remove
        ...

    def process_vnf_install(self):
        # POST /device/action/vnfinstall
        ...

    def process_ztp_upgrade_config(self):
        # POST /device/action/ztp/upgrade
        ...

    def process_ztp_upgrade_config_setting(self):
        # POST /device/action/ztp/upgrade/setting
        ...

    def re_discover_all_device(self):
        # POST /device/action/rediscoverall
        ...

    def re_discover_devices(self):
        # POST /device/action/rediscover
        ...

    def test_api_key(self):
        # GET /device/action/security/apikey/{uuid}
        ...

    def test_iox_config(self):
        # GET /device/action/test/ioxconfig/{deviceIP}
        ...

    def trigger_pending_tasks_monitoring(self):
        # GET /device/action/startmonitor
        ...
