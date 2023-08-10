from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.endpoints.administration_user_and_group import AdministrationUserAndGroup
from vmngclient.endpoints.certificate_management_vmanage import CertificateManagementVManage
from vmngclient.endpoints.client import Client
from vmngclient.endpoints.cluster_management import ClusterManagement
from vmngclient.endpoints.configuration_dashboard_status import ConfigurationDashboardStatus
from vmngclient.endpoints.configuration_device_actions import ConfigurationDeviceActions
from vmngclient.endpoints.configuration_device_software_update import ConfigurationDeviceSoftwareUpdate
from vmngclient.endpoints.configuration_device_template import ConfigurationDeviceTemplate
from vmngclient.endpoints.configuration_settings import ConfigurationSettings
from vmngclient.endpoints.monitoring_device_details import MonitoringDeviceDetails
from vmngclient.endpoints.monitoring_status import MonitoringStatus
from vmngclient.endpoints.sdavc_cloud_connector import SDAVCCloudConnector
from vmngclient.endpoints.tenant_backup_restore import TenantBackupRestore
from vmngclient.endpoints.tenant_management import TenantManagement
from vmngclient.endpoints.tenant_migration import TenantMigration

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIEndpointContainter:
    def __init__(self, session: vManageSession):
        self.administration_user_and_group = AdministrationUserAndGroup(session)
        self.certificate_management_vmanage = CertificateManagementVManage(session)
        self.client = Client(session)
        self.cluster_management = ClusterManagement(session)
        self.configuration_dashboard_status = ConfigurationDashboardStatus(session)
        self.configuration_device_actions = ConfigurationDeviceActions(session)
        self.configuration_device_software_update = ConfigurationDeviceSoftwareUpdate(session)
        self.configuration_device_template = ConfigurationDeviceTemplate(session)
        self.configuration_settings = ConfigurationSettings(session)
        self.monitoring_device_details = MonitoringDeviceDetails(session)
        self.monitoring_status = MonitoringStatus(session)
        self.sdavc_cloud_connector = SDAVCCloudConnector(session)
        self.tenant_backup_restore = TenantBackupRestore(session)
        self.tenant_management = TenantManagement(session)
        self.tenant_migration = TenantMigration(session)
