# mypy: disable-error-code="empty-body"
from pathlib import Path
from typing import BinaryIO
from urllib.parse import parse_qsl, urlsplit

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get, post, request
from vmngclient.model.tenant import Tenant


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


class TenantMigration(APIEndpoints):
    @request(get, "/tenantmigration/download/{path}")
    def download_tenant_data(self, path: str = "default.tar.gz") -> bytes:
        ...

    @request(post, "/tenantmigration/export")
    def export_tenant_data(self, payload: Tenant) -> ExportInfo:
        ...

    @request(get, "/tenantmigration/migrationToken")
    def get_migration_token(self, params: MigrationTokenQueryParams) -> str:
        ...

    def import_tenant_data(self, data: BinaryIO) -> ImportInfo:
        # TODO implement dedicated payload types for files upload in request decorator
        response = self._request(post, "/tenantmigration/import", files={"file": (Path(data.name).name, data)})
        return response.dataobj(ImportInfo, None)

    @request(post, "/tenantmigration/networkMigration")
    def migrate_network(self, payload: str) -> MigrationInfo:
        ...

    def retrigger_network_migration(self):
        # GET /tenantmigration/networkMigration
        ...
