from vmngclient.primitives import APIPrimitiveBase


class TenantMigrationPrimitives(APIPrimitiveBase):
    def download_tenant_data(self):
        # GET /tenantmigration/download/{path}
        pass

    def export_tenant_data(self):
        # POST /tenantmigration/export
        pass

    def get_migration_token(self):
        # GET /tenantmigration/migrationToken
        pass

    def import_tenant_data(self):
        # POST /tenantmigration/import
        pass

    def migrate_network(self):
        # POST /tenantmigration/networkMigration
        pass

    def re_trigger_network_migration(self):
        # GET /tenantmigration/networkMigration
        pass
