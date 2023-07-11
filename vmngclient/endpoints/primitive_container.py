from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.endpoints.administration_user_and_group import AdministrationUserAndGroupPrimitives
from vmngclient.endpoints.client import ClientPrimitives
from vmngclient.endpoints.configuration_dashboard_status import ConfigurationDashboardStatusPrimitives
from vmngclient.endpoints.configuration_device_software_update import ConfigurationDeviceSoftwareUpdatePrimitives
from vmngclient.endpoints.configuration_device_template import ConfigurationDeviceTemplatePrimitives
from vmngclient.endpoints.monitoring_device_details import MonitoringDeviceDetailsPrimitives
from vmngclient.endpoints.tenant_backup_restore import TenantBackupRestorePrimitives
from vmngclient.endpoints.tenant_management import TenantManagementPrimitives
from vmngclient.endpoints.tenant_migration import TenantMigrationPrimitives

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIPrimitiveContainter:
    def __init__(self, session: vManageSession):
        self.administration_user_and_group = AdministrationUserAndGroupPrimitives(session)
        self.client = ClientPrimitives(session)
        self.configuration_dashboard_status = ConfigurationDashboardStatusPrimitives(session)
        self.configuration_device_software_update = ConfigurationDeviceSoftwareUpdatePrimitives(session)
        self.configuration_device_template = ConfigurationDeviceTemplatePrimitives(session)
        self.monitoring_device_details = MonitoringDeviceDetailsPrimitives(session)
        self.tenant_backup_restore = TenantBackupRestorePrimitives(session)
        self.tenant_management = TenantManagementPrimitives(session)
        self.tenant_migration = TenantMigrationPrimitives(session)
