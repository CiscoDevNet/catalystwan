# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import List

from pydantic.v1 import BaseModel

from catalystwan.endpoints import APIEndpoints, get, view
from catalystwan.utils.session_type import ProviderAsTenantView, TenantView


class BackupFiles(BaseModel):
    backup_files: List[str]


class TenantBackupRestore(APIEndpoints):
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
    @get("/tenantbackup/list")
    def list_tenant_backup(self) -> BackupFiles:
        ...
