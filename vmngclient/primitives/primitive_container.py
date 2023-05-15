from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.primitives.client import ClientPrimitives
from vmngclient.primitives.task_status_api import TasksPrimitives
from vmngclient.primitives.tenant_backup_restore import TenantBackupRestorePrimitives
from vmngclient.primitives.tenant_management import TenantManagementPrimitives
from vmngclient.primitives.tenant_migration import TenantMigrationPrimitives

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIPrimitiveContainter:
    def __init__(self, session: vManageSession):
        self.client = ClientPrimitives(session)
        self.tenant_management = TenantManagementPrimitives(session)
        self.tenant_backup_restore = TenantBackupRestorePrimitives(session)
        self.tenant_migration = TenantMigrationPrimitives(session)
        self.task_status = TasksPrimitives(session)
