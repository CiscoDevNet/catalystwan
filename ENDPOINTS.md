**THIS FILE IS AUTO-GENERATED DO NOT EDIT**

All URIs are relative to */dataservice*
HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode
------------ | ------------------ | ------ | ------------ | ----------- | ------------
POST /admin/user||[**AdministrationUserAndGroup.create_user**](vmngclient/endpoints/administration_user_and_group.py#L157)|[**User**](vmngclient/endpoints/administration_user_and_group.py#L11)||
POST /admin/usergroup||[**AdministrationUserAndGroup.create_user_group**](vmngclient/endpoints/administration_user_and_group.py#L161)|[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L48)||
DELETE /admin/user/{username}||[**AdministrationUserAndGroup.delete_user**](vmngclient/endpoints/administration_user_and_group.py#L173)|||
DELETE /admin/usergroup/{group_name}||[**AdministrationUserAndGroup.delete_user_group**](vmngclient/endpoints/administration_user_and_group.py#L177)|||
GET /admin/user/userAuthType||[**AdministrationUserAndGroup.find_user_auth_type**](vmngclient/endpoints/administration_user_and_group.py#L193)||[**UserAuthType**](vmngclient/endpoints/administration_user_and_group.py#L37)|
GET /admin/usergroup||[**AdministrationUserAndGroup.find_user_groups**](vmngclient/endpoints/administration_user_and_group.py#L197)||DataSequence[[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L48)]|
GET /admin/user/role||[**AdministrationUserAndGroup.find_user_role**](vmngclient/endpoints/administration_user_and_group.py#L205)||[**UserRole**](vmngclient/endpoints/administration_user_and_group.py#L33)|
GET /admin/user||[**AdministrationUserAndGroup.find_users**](vmngclient/endpoints/administration_user_and_group.py#L209)||DataSequence[[**User**](vmngclient/endpoints/administration_user_and_group.py#L11)]|
GET /admin/user/activeSessions||[**AdministrationUserAndGroup.get_active_sessions**](vmngclient/endpoints/administration_user_and_group.py#L213)||DataSequence[[**ActiveSession**](vmngclient/endpoints/administration_user_and_group.py#L89)]|
DELETE /admin/user/removeSessions||[**AdministrationUserAndGroup.remove_sessions**](vmngclient/endpoints/administration_user_and_group.py#L225)|[**SessionsDeleteRequest**](vmngclient/endpoints/administration_user_and_group.py#L105)|[**InvalidateSessionMessage**](vmngclient/endpoints/administration_user_and_group.py#L118)|
POST /admin/user/reset||[**AdministrationUserAndGroup.reset_user**](vmngclient/endpoints/administration_user_and_group.py#L229)|[**UserResetRequest**](vmngclient/endpoints/administration_user_and_group.py#L85)||
GET /admin/resourcegroup||[**AdministrationUserAndGroup.find_resource_groups**](vmngclient/endpoints/administration_user_and_group.py#L233)||DataSequence[[**ResourceGroup**](vmngclient/endpoints/administration_user_and_group.py#L127)]|
POST /admin/resourcegroup/switch||[**AdministrationUserAndGroup.switch_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L237)|[**ResourceGroupSwitchRequest**](vmngclient/endpoints/administration_user_and_group.py#L144)||
PUT /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroup.update_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L241)|[**ResourceGroupUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L137)||
DELETE /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroup.delete_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L245)|||
POST /admin/resourcegroup||[**AdministrationUserAndGroup.create_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L249)|[**ResourceGroup**](vmngclient/endpoints/administration_user_and_group.py#L127)||
PUT /admin/user/password/{username}||[**AdministrationUserAndGroup.update_password**](vmngclient/endpoints/administration_user_and_group.py#L261)|[**UserUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L20)||
PUT /admin/user/profile/password||[**AdministrationUserAndGroup.update_profile_password**](vmngclient/endpoints/administration_user_and_group.py#L269)|[**ProfilePasswordUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L122)||
PUT /admin/user/{username}||[**AdministrationUserAndGroup.update_user**](vmngclient/endpoints/administration_user_and_group.py#L273)|[**UserUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L20)||
PUT /admin/usergroup/{group_name}||[**AdministrationUserAndGroup.update_user_group**](vmngclient/endpoints/administration_user_and_group.py#L277)|[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L48)||
GET /client/server||[**Client.server**](vmngclient/endpoints/client.py#L61)||[**ServerInfo**](vmngclient/endpoints/client.py#L21)|
GET /client/about||[**Client.about**](vmngclient/endpoints/client.py#L65)||[**AboutInfo**](vmngclient/endpoints/client.py#L49)|
GET /device/action/status/{task_id}||[**ConfigurationDashboardStatus.find_status**](vmngclient/endpoints/configuration_dashboard_status.py#L89)||[**TaskData**](vmngclient/endpoints/configuration_dashboard_status.py#L76)|
GET /device/action/status/tasks||[**ConfigurationDashboardStatus.find_running_tasks**](vmngclient/endpoints/configuration_dashboard_status.py#L93)||[**TasksData**](vmngclient/endpoints/configuration_dashboard_status.py#L84)|
POST /device/action/software/package||[**ConfigurationDeviceSoftwareUpdate.install_pkg**](vmngclient/endpoints/configuration_device_software_update.py#L22)|[**SoftwarePackageUpdatePayload**](vmngclient/utils/upgrades_helper.py#L68)||
POST /template/device/config/config/||[**ConfigurationDeviceTemplate.get_device_configuration_preview**](vmngclient/endpoints/configuration_device_template.py#L19)|[**FeatureToCLIPayload**](vmngclient/endpoints/configuration_device_template.py#L10)|str|
GET /device/tier||[**MonitoringDeviceDetails.get_tiers**](vmngclient/endpoints/monitoring_device_details.py#L116)||DataSequence[[**Tier**](vmngclient/endpoints/monitoring_device_details.py#L15)]|
GET /tenantbackup/list||[**TenantBackupRestore.list_tenant_backup**](vmngclient/endpoints/tenant_backup_restore.py#L35)||[**BackupFiles**](vmngclient/endpoints/tenant_backup_restore.py#L10)|
POST /tenant||[**TenantManagement.create_tenant**](vmngclient/endpoints/tenant_management.py#L118)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**Tenant**](vmngclient/model/tenant.py#L21)|
POST /tenant/async||[**TenantManagement.create_tenant_async**](vmngclient/endpoints/tenant_management.py#L123)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L21)|
POST /tenant/bulk/async||[**TenantManagement.create_tenant_async_bulk**](vmngclient/endpoints/tenant_management.py#L128)|List[[**Tenant**](vmngclient/model/tenant.py#L21)]|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L21)|
DELETE /tenant/{tenant_id}/delete||[**TenantManagement.delete_tenant**](vmngclient/endpoints/tenant_management.py#L134)|[**TenantDeleteRequest**](vmngclient/endpoints/tenant_management.py#L12)||
DELETE /tenant/bulk/async||[**TenantManagement.delete_tenant_async_bulk**](vmngclient/endpoints/tenant_management.py#L139)|[**TenantBulkDeleteRequest**](vmngclient/endpoints/tenant_management.py#L16)|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L21)|
GET /tenantstatus||[**TenantManagement.get_all_tenant_statuses**](vmngclient/endpoints/tenant_management.py#L149)||DataSequence[[**TenantStatus**](vmngclient/endpoints/tenant_management.py#L54)]|
GET /tenant||[**TenantManagement.get_all_tenants**](vmngclient/endpoints/tenant_management.py#L154)||DataSequence[[**Tenant**](vmngclient/model/tenant.py#L21)]|
GET /tenant/{tenant_id}||[**TenantManagement.get_tenant**](vmngclient/endpoints/tenant_management.py#L159)||[**Tenant**](vmngclient/model/tenant.py#L21)|
GET /tenant/vsmart/capacity||[**TenantManagement.get_tenant_hosting_capacity_on_vsmarts**](vmngclient/endpoints/tenant_management.py#L164)||DataSequence[[**vSmartTenantCapacity**](vmngclient/endpoints/tenant_management.py#L103)]|
GET /tenant/vsmart||[**TenantManagement.get_tenant_vsmart_mapping**](vmngclient/endpoints/tenant_management.py#L169)||[**vSmartTenantMap**](vmngclient/endpoints/tenant_management.py#L109)|
PUT /tenant/{tenant_id}||[**TenantManagement.update_tenant**](vmngclient/endpoints/tenant_management.py#L182)|[**TenantUpdateRequest**](vmngclient/endpoints/tenant_management.py#L63)|[**Tenant**](vmngclient/model/tenant.py#L21)|
PUT /tenant/{tenant_id}/vsmart||[**TenantManagement.update_tenant_vsmart_placement**](vmngclient/endpoints/tenant_management.py#L187)|[**vSmartPlacementUpdateRequest**](vmngclient/endpoints/tenant_management.py#L98)||
POST /tenant/{tenant_id}/vsessionid||[**TenantManagement.vsession_id**](vmngclient/endpoints/tenant_management.py#L192)||[**vSessionId**](vmngclient/endpoints/tenant_management.py#L113)|
GET /tenantmigration/download/{path}||[**TenantMigration.download_tenant_data**](vmngclient/endpoints/tenant_migration.py#L39)||bytes|
POST /tenantmigration/export||[**TenantMigration.export_tenant_data**](vmngclient/endpoints/tenant_migration.py#L43)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**ExportInfo**](vmngclient/endpoints/tenant_migration.py#L16)|
GET /tenantmigration/migrationToken||[**TenantMigration.get_migration_token**](vmngclient/endpoints/tenant_migration.py#L47)||str|
POST /tenantmigration/networkMigration||[**TenantMigration.migrate_network**](vmngclient/endpoints/tenant_migration.py#L56)|str|[**MigrationInfo**](vmngclient/endpoints/tenant_migration.py#L34)|
