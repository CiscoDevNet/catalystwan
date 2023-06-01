from typing import List

from pydantic import BaseModel

from vmngclient.primitives import APIPrimitiveBase, View
from vmngclient.utils.session_type import ProviderAsTenantView, TenantView


class BackupFiles(BaseModel):
    backup_files: List[str]


class TenantBackupRestorePrimitives(APIPrimitiveBase):
    @View({ProviderAsTenantView})
    def delete_tenant_backup(self):
        # DELETE /tenantbackup/delete
        ...

    @View({ProviderAsTenantView, TenantView})
    def download_existing_backup_file(self):
        # GET /tenantbackup/download/{path}
        ...

    @View({ProviderAsTenantView, TenantView})
    def export_tenant_backup(self):
        # GET /tenantbackup/export
        ...

    @View({ProviderAsTenantView})
    def import_tenant_backup(self):
        # POST /tenantbackup/import
        ...

    @View({ProviderAsTenantView, TenantView})
    def list_tenant_backup(self) -> BackupFiles:
        return self.get("/tenantbackup/list").dataobj(BackupFiles, None)
