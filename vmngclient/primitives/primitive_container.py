from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.primitives.administration_user_and_group import AdministrationUserAndGroupPrimitives
from vmngclient.primitives.client import ClientPrimitives
from vmngclient.primitives.configuration_dashboard_status import ConfigurationDashboardStatusPrimitives
from vmngclient.primitives.configuration_device_template import ConfigurationDeviceTemplatePrimitives
from vmngclient.primitives.monitoring_device_details import MonitoringDeviceDetailsPrimitives
from vmngclient.primitives.tenant_backup_restore import TenantBackupRestorePrimitives
from vmngclient.primitives.tenant_management import TenantManagementPrimitives
from vmngclient.primitives.tenant_migration import TenantMigrationPrimitives

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIPrimitiveContainter:
    def __init__(self, session: vManageSession):
        self.client = ClientPrimitives(session)
        self.configuration_device_template = ConfigurationDeviceTemplatePrimitives(session)
        self.tenant_management = TenantManagementPrimitives(session)
        self.tenant_backup_restore = TenantBackupRestorePrimitives(session)
        self.tenant_migration = TenantMigrationPrimitives(session)
        self.configuration_dashboard_status = ConfigurationDashboardStatusPrimitives(session)
        self.monitoring_device_details = MonitoringDeviceDetailsPrimitives(session)
        self.administration_user_and_group = AdministrationUserAndGroupPrimitives(session)
