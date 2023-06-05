from typing import List

from pydantic import BaseModel

from vmngclient.primitives import APIPrimitiveBase, view
from vmngclient.utils.session_type import ProviderAsTenantView, TenantView


class BackupFiles(BaseModel):
    backup_files: List[str]


class TenantBackupRestorePrimitives(APIPrimitiveBase):
    @view({ProviderAsTenantView})
    def delete_tenant_backup(self):
        # DELETE /tenantbackup/delete
        ...

    @view({ProviderAsTenantView, TenantView})
    def download_existing_backup_file(self):
        # GET /tenantbackup/download/{path}
        ...

    @view({ProviderAsTenantView, TenantView})
    def export_tenant_backup(self):
        # GET /tenantbackup/export
        ...

    @view({ProviderAsTenantView})
    def import_tenant_backup(self):
        # POST /tenantbackup/import
        ...

    @view({ProviderAsTenantView, TenantView})
    def list_tenant_backup(self) -> BackupFiles:
        return self._get("/tenantbackup/list").dataobj(BackupFiles, None)
