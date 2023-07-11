from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.endpoints.administration_user_and_group import AdministrationUserAndGroup
from vmngclient.endpoints.client import Client
from vmngclient.endpoints.configuration_dashboard_status import ConfigurationDashboardStatus
from vmngclient.endpoints.configuration_device_software_update import ConfigurationDeviceSoftwareUpdate
from vmngclient.endpoints.configuration_device_template import ConfigurationDeviceTemplate
from vmngclient.endpoints.monitoring_device_details import MonitoringDeviceDetails
from vmngclient.endpoints.tenant_backup_restore import TenantBackupRestore
from vmngclient.endpoints.tenant_management import TenantManagement
from vmngclient.endpoints.tenant_migration import TenantMigration

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIEndpointContainter:
    def __init__(self, session: vManageSession):
        self.administration_user_and_group = AdministrationUserAndGroup(session)
        self.client = Client(session)
        self.configuration_dashboard_status = ConfigurationDashboardStatus(session)
        self.configuration_device_software_update = ConfigurationDeviceSoftwareUpdate(session)
        self.configuration_device_template = ConfigurationDeviceTemplate(session)
        self.monitoring_device_details = MonitoringDeviceDetails(session)
        self.tenant_backup_restore = TenantBackupRestore(session)
        self.tenant_management = TenantManagement(session)
        self.tenant_migration = TenantMigration(session)
