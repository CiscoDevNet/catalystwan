from pathlib import Path
from typing import BinaryIO
from urllib.parse import parse_qsl, urlsplit

from pydantic import BaseModel, Field

from vmngclient.model.tenant import Tenant
from vmngclient.primitives import APIPrimitiveBase


class MigrationTokenQueryParams(BaseModel):
    migration_id: str = Field(alias="migrationId")


class ExportInfo(BaseModel):
    process_id: str = Field(alias="processId")


class ImportInfo(BaseModel):
    process_id: str = Field(alias="processId")
    migration_token_url: str = Field(alias="migrationTokenURL")

    @property
    def migration_token_query(self) -> str:
        return urlsplit(self.migration_token_url).query

    @property
    def migration_token_query_params(self) -> MigrationTokenQueryParams:
        query = self.migration_token_query
        return MigrationTokenQueryParams.parse_obj(parse_qsl(query))


class MigrationInfo(BaseModel):
    process_id: str = Field(alias="processId")


class TenantMigrationPrimitives(APIPrimitiveBase):
    def download_tenant_data(self, path: str = "default.tar.gz") -> bytes:
        return self.get(f"/tenantmigration/download/{path}").content

    def export_tenant_data(self, tenant: Tenant) -> ExportInfo:
        response = self.post("/tenantmigration/export", payload=tenant)
        return response.dataobj(ExportInfo, None)

    def get_migration_token(self, params: MigrationTokenQueryParams) -> str:
        return self.get("/tenantmigration/migrationToken", params=params.dict(by_alias=True)).text

    def import_tenant_data(self, data: BinaryIO) -> ImportInfo:
        response = self.post("/tenantmigration/import", files={"file": (Path(data.name).name, data)})
        return response.dataobj(ImportInfo, None)

    def migrate_network(self, migration_token: str) -> MigrationInfo:
        response = self.post("/tenantmigration/networkMigration", data=migration_token)
        return response.dataobj(MigrationInfo, None)

    def retrigger_network_migration(self):
        # GET /tenantmigration/networkMigration
        ...
