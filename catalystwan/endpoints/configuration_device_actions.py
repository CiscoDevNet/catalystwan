# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from catalystwan.endpoints import APIEndpoints, get, post
from catalystwan.typed_list import DataSequence


def convert_to_list(element: Union[str, List[str]]) -> List[str]:
    return [element] if isinstance(element, str) else element


DeviceType = Literal["vedge", "controller", "vmanage"]

VersionType = Literal["vmanage", "remote"]

PartitionActionType = Literal["removepartition", "defaultpartition", "changepartition"]


class ActionId(BaseModel):
    id: str


class GroupId(BaseModel):
    group_id: str = Field(default="all", serialization_alias="groupID", validation_alias="groupID")


class ZTPUpgradeSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    enable_upgrade: bool = Field(serialization_alias="enableUpgrade", validation_alias="enableUpgrade")
    platform_family: str = Field(serialization_alias="platformFamily", validation_alias="platformFamily")
    version_id: str = Field(serialization_alias="versionId", validation_alias="versionId")
    version_name: str = Field(serialization_alias="versionName", validation_alias="versionName")


class PartitionDevice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str = Field(serialization_alias="deviceId", validation_alias="deviceId")
    device_ip: str = Field(serialization_alias="deviceIP", validation_alias="deviceIP")
    version: Union[str, List[str]] = Field(default="")


VersionList = Annotated[Union[str, List[str]], BeforeValidator(convert_to_list)]


class RemovePartitionDevice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str = Field(serialization_alias="deviceId", validation_alias="deviceId")
    device_ip: str = Field(serialization_alias="deviceIP", validation_alias="deviceIP")
    version: VersionList


class PartitionActionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action: PartitionActionType
    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    devices: List[PartitionDevice]


class RemovePartitionActionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action: PartitionActionType
    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    devices: List[RemovePartitionDevice]


class InstallData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    family: str
    version: str
    version_id: str = Field(serialization_alias="versionId", validation_alias="versionId")
    remote_server_id: str = Field(serialization_alias="remoteServerId", validation_alias="remoteServerId")


class InstallInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: Optional[List[InstallData]] = Field(default=None)
    family: Optional[str] = Field(default=None)
    reboot: bool
    sync: bool
    v_edge_vpn: int = Field(serialization_alias="vEdgeVPN", validation_alias="vEdgeVPN")
    v_smart_vpn: int = Field(serialization_alias="vSmartVPN", validation_alias="vSmartVPN")
    version: Optional[str] = Field(default=None)
    version_type: VersionType = Field(serialization_alias="versionType", validation_alias="versionType")


class InstallDevice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_id: str = Field(serialization_alias="deviceId", validation_alias="deviceId")
    device_ip: str = Field(serialization_alias="deviceIP", validation_alias="deviceIP")
    is_nutella_migration: Optional[bool] = Field(
        default=False, serialization_alias="isNutellaMigration", validation_alias="isNutellaMigration"
    )


class InstallActionPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action: str = Field(default="install")
    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    devices: List[InstallDevice]
    input: InstallInput


class InstalledDeviceData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    available_versions: Optional[List[str]] = Field(
        None, serialization_alias="availableVersions", validation_alias="availableVersions"
    )
    current_partition: Optional[str] = Field(
        None, serialization_alias="current-partition", validation_alias="current-partition"
    )
    default_version: Optional[str] = Field(
        None, serialization_alias="defaultVersion", validation_alias="defaultVersion"
    )
    device_model: Optional[str] = Field(None, serialization_alias="device-model", validation_alias="device-model")
    device_os: Optional[str] = Field(None, serialization_alias="device-os", validation_alias="device-os")
    device_type: Optional[str] = Field(None, serialization_alias="device-type", validation_alias="device-type")
    host_name: Optional[str] = Field(None, serialization_alias="host-name", validation_alias="host-name")
    is_multi_step_upgrade_supported: Optional[bool] = Field(
        None, serialization_alias="isMultiStepUpgradeSupported", validation_alias="isMultiStepUpgradeSupported"
    )
    is_schedule_upgrade_supported: Optional[bool] = Field(
        None, serialization_alias="isScheduleUpgradeSupported", validation_alias="isScheduleUpgradeSupported"
    )
    layout_level: Optional[int] = Field(None, serialization_alias="layoutLevel", validation_alias="layoutLevel")
    local_system_ip: Optional[str] = Field(
        None, serialization_alias="local-system-ip", validation_alias="local-system-ip"
    )
    personality: Optional[str] = Field(None)
    platform: Optional[str] = Field(None)
    platform_family: Optional[str] = Field(
        None, serialization_alias="platformFamily", validation_alias="platformFamily"
    )
    reachability: Optional[str] = Field(None)
    site_id: Optional[str] = Field(None, serialization_alias="site-id", validation_alias="site-id")
    system_ip: Optional[str] = Field(None, serialization_alias="system-ip", validation_alias="system-ip")
    uptime_date: Optional[int] = Field(None, serialization_alias="uptime-date", validation_alias="uptime-date")
    uuid: Optional[str] = Field(None)
    version: Optional[str] = Field(None)


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
        self, device_type: DeviceType = "controller", params: GroupId = GroupId()
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

    @post("/device/action/changepartition")
    def process_mark_change_partition(self, payload: PartitionActionPayload) -> ActionId:
        ...

    def process_deactivate_smu(self):
        # POST /device/action/deactivate
        ...

    @post("/device/action/defaultpartition")
    def process_mark_default_partition(self, payload: PartitionActionPayload) -> ActionId:
        ...

    def process_delete_amp_api_key(self):
        # DELETE /device/action/security/amp/apikey/{uuid}
        ...

    @post("/device/action/install")
    def process_install_operation(self, payload: InstallActionPayload) -> ActionId:
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

    @post("/device/action/removepartition")
    def process_remove_partition(self, payload: RemovePartitionActionPayload) -> ActionId:
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
