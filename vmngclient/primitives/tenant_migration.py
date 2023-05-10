from typing import Optional

from pydantic import BaseModel, Field

from vmngclient.model.tenant import Tenant
from vmngclient.primitives import APIPrimitiveBase


class ExportProcessId(BaseModel):
    process_id: str = Field(alias="processId")


class TenantMigrationPrimitives(APIPrimitiveBase):
    def download_tenant_data(self, path: Optional[str] = "default.tar.gz") -> bytes:
        return self.get(f"/tenantmigration/download/{path}").content

    def export_tenant_data(self, tenant: Tenant):
        response = self.post("/tenantmigration/export", payload=tenant)
        return response.dataobj(ExportProcessId, None)

    def get_migration_token(self):
        # GET /tenantmigration/migrationToken
        pass

    def import_tenant_data(self):
        # POST /tenantmigration/import
        pass

    def migrate_network(self):
        # POST /tenantmigration/networkMigration
        pass

    def retrigger_network_migration(self):
        # GET /tenantmigration/networkMigration
        pass
