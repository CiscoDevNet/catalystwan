# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from pydantic.v1 import BaseModel, Field

from catalystwan.endpoints import APIEndpoints, CustomPayloadType, PreparedPayload, get, post, versions, view
from catalystwan.models.tenant import TenantExport
from catalystwan.utils.session_type import ProviderView, SingleTenantView


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


class MigrationFile(CustomPayloadType):
    def __init__(self, filename: Path):
        self.filename = filename

    def prepared(self) -> PreparedPayload:
        data = open(self.filename, "rb")
        return PreparedPayload(files={"file": (Path(data.name).name, data)})


class TenantMigration(APIEndpoints):
    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @get("/tenantmigration/download/{path}")
    def download_tenant_data(self, path: str = "default.tar.gz") -> bytes:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @post("/tenantmigration/export")
    def export_tenant_data(self, payload: TenantExport) -> ExportInfo:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @get("/tenantmigration/migrationToken")
    def get_migration_token(self, params: MigrationTokenQueryParams) -> str:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6,<20.13")
    @post("/tenantmigration/import")
    def import_tenant_data(self, payload: MigrationFile) -> ImportInfo:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.13")
    @post("/tenantmigration/import/{migration_key}")
    def import_tenant_data_with_key(self, payload: MigrationFile, migration_key: str) -> ImportInfo:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @post("/tenantmigration/networkMigration")
    def migrate_network(self, payload: str) -> MigrationInfo:
        ...

    def retrigger_network_migration(self):
        # GET /tenantmigration/networkMigration
        ...
