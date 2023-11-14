# mypy: disable-error-code="empty-body"


from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get
from vmngclient.typed_list import DataSequence


class ZTPUpgradeSettings(BaseModel):
    version_id: str = Field(alias="versionId")
    platform_family: str = Field(alias="platformFamily")
    enable_upgrade: bool = Field(alias="enableUpgrade")
    version_name: str = Field(alias="versionName")


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

    def generate_device_list(self):
        # GET /device/action/install/devices/{deviceType}
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

    def process_default_partition(self):
        # POST /device/action/defaultpartition
        ...

    def process_delete_amp_api_key(self):
        # DELETE /device/action/security/amp/apikey/{uuid}
        ...

    def process_install(self):
        # POST /device/action/install
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
