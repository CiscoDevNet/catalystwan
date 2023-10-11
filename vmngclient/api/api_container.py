from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.api.admin_tech_api import AdminTechAPI
from vmngclient.api.administration import (
    AdministrationSettingsAPI,
    ClusterManagementAPI,
    ResourceGroupsAPI,
    SessionsAPI,
    UserGroupsAPI,
    UsersAPI,
)
from vmngclient.api.alarms_api import AlarmsAPI
from vmngclient.api.basic_api import DevicesAPI, DeviceStateAPI
from vmngclient.api.config_device_inventory_api import ConfigurationDeviceInventoryAPI
from vmngclient.api.config_group_api import ConfigGroupAPI
from vmngclient.api.dashboard_api import DashboardAPI
from vmngclient.api.feature_profile_api import SDRoutingFeatureProfilesAPI
from vmngclient.api.logs_api import LogsAPI
from vmngclient.api.omp_api import OmpAPI
from vmngclient.api.packet_capture_api import PacketCaptureAPI
from vmngclient.api.partition_manager_api import PartitionManagerAPI
from vmngclient.api.resource_pool_api import ResourcePoolAPI
from vmngclient.api.software_action_api import SoftwareActionAPI
from vmngclient.api.speedtest_api import SpeedtestAPI
from vmngclient.api.template_api import TemplatesAPI
from vmngclient.api.tenant_backup_restore_api import TenantBackupRestoreAPI
from vmngclient.api.tenant_management_api import TenantManagementAPI
from vmngclient.api.tenant_migration_api import TenantMigrationAPI
from vmngclient.api.versions_utils import RepositoryAPI

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIContainer:
    def __init__(self, session: vManageSession):
        self.tenant_management = TenantManagementAPI(session)
        self.admin_tech = AdminTechAPI(session)
        self.administration_settings = AdministrationSettingsAPI(session)
        self.alarms = AlarmsAPI(session)
        self.config_device_inventory_api = ConfigurationDeviceInventoryAPI(session)
        self.config_group = ConfigGroupAPI(session)
        self.dashboard = DashboardAPI(session)
        self.devices = DevicesAPI(session)
        self.device_state = DeviceStateAPI(session)
        self.logs = LogsAPI(session)
        self.omp = OmpAPI(session)
        self.packet_capture = PacketCaptureAPI(session)
        self.speedtest = SpeedtestAPI(session)
        self.templates = TemplatesAPI(session)
        self.tenant_backup = TenantBackupRestoreAPI(session)
        self.tenant_migration = TenantMigrationAPI(session)
        self.repository = RepositoryAPI(session)
        self.resource_pool = ResourcePoolAPI(session)
        self.software = SoftwareActionAPI(session)
        self.partition = PartitionManagerAPI(session)
        self.users = UsersAPI(session)
        self.cluster_management = ClusterManagementAPI(session)
        self.user_groups = UserGroupsAPI(session)
        self.resource_groups = ResourceGroupsAPI(session)
        self.sessions = SessionsAPI(session)
        self.sd_routing_feature_profiles = SDRoutingFeatureProfilesAPI(session)
