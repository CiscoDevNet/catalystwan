**THIS FILE IS AUTO-GENERATED DO NOT EDIT**

All URIs are relative to */dataservice*
HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode
------------ | ------------------ | ------ | ------------ | ----------- | ------------
POST /admin/user||[**AdministrationUserAndGroup.create_user**](vmngclient/endpoints/administration_user_and_group.py#L156)|[**User**](vmngclient/endpoints/administration_user_and_group.py#L10)||
POST /admin/usergroup||[**AdministrationUserAndGroup.create_user_group**](vmngclient/endpoints/administration_user_and_group.py#L160)|[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L47)||
DELETE /admin/user/{username}||[**AdministrationUserAndGroup.delete_user**](vmngclient/endpoints/administration_user_and_group.py#L172)|||
DELETE /admin/usergroup/{group_name}||[**AdministrationUserAndGroup.delete_user_group**](vmngclient/endpoints/administration_user_and_group.py#L176)|||
GET /admin/user/userAuthType||[**AdministrationUserAndGroup.find_user_auth_type**](vmngclient/endpoints/administration_user_and_group.py#L192)||[**UserAuthType**](vmngclient/endpoints/administration_user_and_group.py#L36)|
GET /admin/usergroup||[**AdministrationUserAndGroup.find_user_groups**](vmngclient/endpoints/administration_user_and_group.py#L196)||DataSequence[[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L47)]|
GET /admin/user/role||[**AdministrationUserAndGroup.find_user_role**](vmngclient/endpoints/administration_user_and_group.py#L204)||[**UserRole**](vmngclient/endpoints/administration_user_and_group.py#L32)|
GET /admin/user||[**AdministrationUserAndGroup.find_users**](vmngclient/endpoints/administration_user_and_group.py#L208)||DataSequence[[**User**](vmngclient/endpoints/administration_user_and_group.py#L10)]|
GET /admin/user/activeSessions||[**AdministrationUserAndGroup.get_active_sessions**](vmngclient/endpoints/administration_user_and_group.py#L212)||DataSequence[[**ActiveSession**](vmngclient/endpoints/administration_user_and_group.py#L88)]|
DELETE /admin/user/removeSessions||[**AdministrationUserAndGroup.remove_sessions**](vmngclient/endpoints/administration_user_and_group.py#L224)|[**SessionsDeleteRequest**](vmngclient/endpoints/administration_user_and_group.py#L104)|[**InvalidateSessionMessage**](vmngclient/endpoints/administration_user_and_group.py#L117)|
POST /admin/user/reset||[**AdministrationUserAndGroup.reset_user**](vmngclient/endpoints/administration_user_and_group.py#L228)|[**UserResetRequest**](vmngclient/endpoints/administration_user_and_group.py#L84)||
GET /admin/resourcegroup||[**AdministrationUserAndGroup.find_resource_groups**](vmngclient/endpoints/administration_user_and_group.py#L232)||DataSequence[[**ResourceGroup**](vmngclient/endpoints/administration_user_and_group.py#L126)]|
POST /admin/resourcegroup/switch||[**AdministrationUserAndGroup.switch_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L236)|[**ResourceGroupSwitchRequest**](vmngclient/endpoints/administration_user_and_group.py#L143)||
PUT /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroup.update_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L240)|[**ResourceGroupUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L136)||
DELETE /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroup.delete_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L244)|||
POST /admin/resourcegroup||[**AdministrationUserAndGroup.create_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L248)|[**ResourceGroup**](vmngclient/endpoints/administration_user_and_group.py#L126)||
PUT /admin/user/password/{username}||[**AdministrationUserAndGroup.update_password**](vmngclient/endpoints/administration_user_and_group.py#L260)|[**UserUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L19)||
PUT /admin/user/profile/password||[**AdministrationUserAndGroup.update_profile_password**](vmngclient/endpoints/administration_user_and_group.py#L268)|[**ProfilePasswordUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L121)||
PUT /admin/user/{username}||[**AdministrationUserAndGroup.update_user**](vmngclient/endpoints/administration_user_and_group.py#L272)|[**UserUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L19)||
PUT /admin/usergroup/{group_name}||[**AdministrationUserAndGroup.update_user_group**](vmngclient/endpoints/administration_user_and_group.py#L276)|[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L47)||
GET /client/server||[**Client.server**](vmngclient/endpoints/client.py#L61)||[**ServerInfo**](vmngclient/endpoints/client.py#L21)|
GET /client/about||[**Client.about**](vmngclient/endpoints/client.py#L65)||[**AboutInfo**](vmngclient/endpoints/client.py#L49)|
GET /device/action/status/{task_id}||[**ConfigurationDashboardStatus.find_status**](vmngclient/endpoints/configuration_dashboard_status.py#L88)||[**TaskData**](vmngclient/endpoints/configuration_dashboard_status.py#L75)|
GET /device/action/status/tasks||[**ConfigurationDashboardStatus.find_running_tasks**](vmngclient/endpoints/configuration_dashboard_status.py#L92)||[**TasksData**](vmngclient/endpoints/configuration_dashboard_status.py#L83)|
POST /device/action/software/package||[**ConfigurationDeviceSoftwareUpdate.install_pkg**](vmngclient/endpoints/configuration_device_software_update.py#L22)|[**SoftwarePackageUpdatePayload**](vmngclient/utils/upgrades_helper.py#L68)||
POST /template/device/config/config/||[**ConfigurationDeviceTemplate.get_device_configuration_preview**](vmngclient/endpoints/configuration_device_template.py#L18)|[**FeatureToCLIPayload**](vmngclient/endpoints/configuration_device_template.py#L9)|str|
GET /device/tier||[**MonitoringDeviceDetails.get_tiers**](vmngclient/endpoints/monitoring_device_details.py#L115)||DataSequence[[**Tier**](vmngclient/endpoints/monitoring_device_details.py#L14)]|
GET /tenantbackup/list||[**TenantBackupRestore.list_tenant_backup**](vmngclient/endpoints/tenant_backup_restore.py#L34)||[**BackupFiles**](vmngclient/endpoints/tenant_backup_restore.py#L9)|
POST /tenant||[**TenantManagement.create_tenant**](vmngclient/endpoints/tenant_management.py#L117)|[**Tenant**](vmngclient/model/tenant.py#L23)|[**Tenant**](vmngclient/model/tenant.py#L23)|
POST /tenant/async||[**TenantManagement.create_tenant_async**](vmngclient/endpoints/tenant_management.py#L122)|[**Tenant**](vmngclient/model/tenant.py#L23)|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L20)|
POST /tenant/bulk/async||[**TenantManagement.create_tenant_async_bulk**](vmngclient/endpoints/tenant_management.py#L127)|List[[**Tenant**](vmngclient/model/tenant.py#L23)]|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L20)|
DELETE /tenant/{tenant_id}/delete||[**TenantManagement.delete_tenant**](vmngclient/endpoints/tenant_management.py#L133)|[**TenantDeleteRequest**](vmngclient/endpoints/tenant_management.py#L11)||
DELETE /tenant/bulk/async||[**TenantManagement.delete_tenant_async_bulk**](vmngclient/endpoints/tenant_management.py#L138)|[**TenantBulkDeleteRequest**](vmngclient/endpoints/tenant_management.py#L15)|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L20)|
GET /tenantstatus||[**TenantManagement.get_all_tenant_statuses**](vmngclient/endpoints/tenant_management.py#L148)||DataSequence[[**TenantStatus**](vmngclient/endpoints/tenant_management.py#L53)]|
GET /tenant||[**TenantManagement.get_all_tenants**](vmngclient/endpoints/tenant_management.py#L153)||DataSequence[[**Tenant**](vmngclient/model/tenant.py#L23)]|
GET /tenant/{tenant_id}||[**TenantManagement.get_tenant**](vmngclient/endpoints/tenant_management.py#L158)||[**Tenant**](vmngclient/model/tenant.py#L23)|
GET /tenant/vsmart/capacity||[**TenantManagement.get_tenant_hosting_capacity_on_vsmarts**](vmngclient/endpoints/tenant_management.py#L163)||DataSequence[[**vSmartTenantCapacity**](vmngclient/endpoints/tenant_management.py#L102)]|
GET /tenant/vsmart||[**TenantManagement.get_tenant_vsmart_mapping**](vmngclient/endpoints/tenant_management.py#L168)||[**vSmartTenantMap**](vmngclient/endpoints/tenant_management.py#L108)|
PUT /tenant/{tenant_id}||[**TenantManagement.update_tenant**](vmngclient/endpoints/tenant_management.py#L181)|[**TenantUpdateRequest**](vmngclient/endpoints/tenant_management.py#L62)|[**Tenant**](vmngclient/model/tenant.py#L23)|
PUT /tenant/{tenant_id}/vsmart||[**TenantManagement.update_tenant_vsmart_placement**](vmngclient/endpoints/tenant_management.py#L186)|[**vSmartPlacementUpdateRequest**](vmngclient/endpoints/tenant_management.py#L97)||
POST /tenant/{tenant_id}/vsessionid||[**TenantManagement.vsession_id**](vmngclient/endpoints/tenant_management.py#L191)||[**vSessionId**](vmngclient/endpoints/tenant_management.py#L112)|
GET /tenantmigration/download/{path}||[**TenantMigration.download_tenant_data**](vmngclient/endpoints/tenant_migration.py#L38)||bytes|
POST /tenantmigration/export||[**TenantMigration.export_tenant_data**](vmngclient/endpoints/tenant_migration.py#L42)|[**Tenant**](vmngclient/model/tenant.py#L23)|[**ExportInfo**](vmngclient/endpoints/tenant_migration.py#L15)|
GET /tenantmigration/migrationToken||[**TenantMigration.get_migration_token**](vmngclient/endpoints/tenant_migration.py#L46)||str|
POST /tenantmigration/networkMigration||[**TenantMigration.migrate_network**](vmngclient/endpoints/tenant_migration.py#L55)|str|[**MigrationInfo**](vmngclient/endpoints/tenant_migration.py#L33)|
