**THIS FILE IS AUTO-GENERATED DO NOT EDIT**

All URIs are relative to */dataservice*
HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode
------------ | ------------------ | ------ | ------------ | ----------- | ------------
POST /admin/user||[**AdministrationUserAndGroupPrimitives.create_user**](vmngclient/primitives/administration_user_and_group.py#L157)|[**User**](vmngclient/primitives/administration_user_and_group.py#L11)||
POST /admin/usergroup||[**AdministrationUserAndGroupPrimitives.create_user_group**](vmngclient/primitives/administration_user_and_group.py#L161)|[**UserGroup**](vmngclient/primitives/administration_user_and_group.py#L48)||
DELETE /admin/user/{username}||[**AdministrationUserAndGroupPrimitives.delete_user**](vmngclient/primitives/administration_user_and_group.py#L173)|||
DELETE /admin/usergroup/{group_name}||[**AdministrationUserAndGroupPrimitives.delete_user_group**](vmngclient/primitives/administration_user_and_group.py#L177)|||
GET /admin/user/userAuthType||[**AdministrationUserAndGroupPrimitives.find_user_auth_type**](vmngclient/primitives/administration_user_and_group.py#L193)||[**UserAuthType**](vmngclient/primitives/administration_user_and_group.py#L37)|
GET /admin/usergroup||[**AdministrationUserAndGroupPrimitives.find_user_groups**](vmngclient/primitives/administration_user_and_group.py#L197)||DataSequence[[**UserGroup**](vmngclient/primitives/administration_user_and_group.py#L48)]|
GET /admin/user/role||[**AdministrationUserAndGroupPrimitives.find_user_role**](vmngclient/primitives/administration_user_and_group.py#L205)||[**UserRole**](vmngclient/primitives/administration_user_and_group.py#L33)|
GET /admin/user||[**AdministrationUserAndGroupPrimitives.find_users**](vmngclient/primitives/administration_user_and_group.py#L209)||DataSequence[[**User**](vmngclient/primitives/administration_user_and_group.py#L11)]|
GET /admin/user/activeSessions||[**AdministrationUserAndGroupPrimitives.get_active_sessions**](vmngclient/primitives/administration_user_and_group.py#L213)||DataSequence[[**ActiveSession**](vmngclient/primitives/administration_user_and_group.py#L89)]|
DELETE /admin/user/removeSessions||[**AdministrationUserAndGroupPrimitives.remove_sessions**](vmngclient/primitives/administration_user_and_group.py#L225)|[**SessionsDeleteRequest**](vmngclient/primitives/administration_user_and_group.py#L105)|[**InvalidateSessionMessage**](vmngclient/primitives/administration_user_and_group.py#L118)|
POST /admin/user/reset||[**AdministrationUserAndGroupPrimitives.reset_user**](vmngclient/primitives/administration_user_and_group.py#L229)|[**UserResetRequest**](vmngclient/primitives/administration_user_and_group.py#L85)||
GET /admin/resourcegroup||[**AdministrationUserAndGroupPrimitives.find_resource_groups**](vmngclient/primitives/administration_user_and_group.py#L233)||DataSequence[[**ResourceGroup**](vmngclient/primitives/administration_user_and_group.py#L127)]|
POST /admin/resourcegroup/switch||[**AdministrationUserAndGroupPrimitives.switch_resource_group**](vmngclient/primitives/administration_user_and_group.py#L237)|[**ResourceGroupSwitchRequest**](vmngclient/primitives/administration_user_and_group.py#L144)||
PUT /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroupPrimitives.update_resource_group**](vmngclient/primitives/administration_user_and_group.py#L241)|[**ResourceGroupUpdateRequest**](vmngclient/primitives/administration_user_and_group.py#L137)||
PUT /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroupPrimitives.delete_resource_group**](vmngclient/primitives/administration_user_and_group.py#L245)|||
POST /admin/resourcegroup||[**AdministrationUserAndGroupPrimitives.create_resource_group**](vmngclient/primitives/administration_user_and_group.py#L249)|||
PUT /admin/user/password/{username}||[**AdministrationUserAndGroupPrimitives.update_password**](vmngclient/primitives/administration_user_and_group.py#L261)|[**UserUpdateRequest**](vmngclient/primitives/administration_user_and_group.py#L20)||
PUT /admin/user/profile/password||[**AdministrationUserAndGroupPrimitives.update_profile_password**](vmngclient/primitives/administration_user_and_group.py#L269)|[**ProfilePasswordUpdateRequest**](vmngclient/primitives/administration_user_and_group.py#L122)||
PUT /admin/user/{username}||[**AdministrationUserAndGroupPrimitives.update_user**](vmngclient/primitives/administration_user_and_group.py#L273)|[**UserUpdateRequest**](vmngclient/primitives/administration_user_and_group.py#L20)||
PUT /admin/usergroup/{group_name}||[**AdministrationUserAndGroupPrimitives.update_user_group**](vmngclient/primitives/administration_user_and_group.py#L277)|[**UserGroup**](vmngclient/primitives/administration_user_and_group.py#L48)||
GET /client/server||[**ClientPrimitives.server**](vmngclient/primitives/client.py#L61)||[**ServerInfo**](vmngclient/primitives/client.py#L21)|
GET /client/about||[**ClientPrimitives.about**](vmngclient/primitives/client.py#L65)||[**AboutInfo**](vmngclient/primitives/client.py#L49)|
GET /device/action/status/{task_id}||[**ConfigurationDashboardStatusPrimitives.find_status**](vmngclient/primitives/configuration_dashboard_status.py#L89)||[**TaskData**](vmngclient/primitives/configuration_dashboard_status.py#L76)|
GET /device/action/status/tasks||[**ConfigurationDashboardStatusPrimitives.find_running_tasks**](vmngclient/primitives/configuration_dashboard_status.py#L93)||[**TasksData**](vmngclient/primitives/configuration_dashboard_status.py#L84)|
POST /template/device/config/config/||[**ConfigurationDeviceTemplatePrimitives.get_device_configuration_preview**](vmngclient/primitives/configuration_device_template.py#L19)|[**FeatureToCLIPayload**](vmngclient/primitives/configuration_device_template.py#L10)|str|
GET /device/tier||[**MonitoringDeviceDetailsPrimitives.get_tiers**](vmngclient/primitives/monitoring_device_details.py#L116)||DataSequence[[**Tier**](vmngclient/primitives/monitoring_device_details.py#L15)]|
GET /tenantbackup/list||[**TenantBackupRestorePrimitives.list_tenant_backup**](vmngclient/primitives/tenant_backup_restore.py#L35)||[**BackupFiles**](vmngclient/primitives/tenant_backup_restore.py#L10)|
POST /tenant||[**TenantManagementPrimitives.create_tenant**](vmngclient/primitives/tenant_management.py#L118)||[**Tenant**](vmngclient/model/tenant.py#L21)|
POST /tenant/async||[**TenantManagementPrimitives.create_tenant_async**](vmngclient/primitives/tenant_management.py#L123)||[**TenantTaskId**](vmngclient/primitives/tenant_management.py#L21)|
POST /tenant/bulk/async||[**TenantManagementPrimitives.create_tenant_async_bulk**](vmngclient/primitives/tenant_management.py#L128)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**TenantTaskId**](vmngclient/primitives/tenant_management.py#L21)|
DELETE /tenant/{tenant_id}/delete||[**TenantManagementPrimitives.delete_tenant**](vmngclient/primitives/tenant_management.py#L134)|[**TenantDeleteRequest**](vmngclient/primitives/tenant_management.py#L12)||
DELETE /tenant/bulk/async||[**TenantManagementPrimitives.delete_tenant_async_bulk**](vmngclient/primitives/tenant_management.py#L139)|[**TenantBulkDeleteRequest**](vmngclient/primitives/tenant_management.py#L16)|[**TenantTaskId**](vmngclient/primitives/tenant_management.py#L21)|
GET /tenantstatus||[**TenantManagementPrimitives.get_all_tenant_statuses**](vmngclient/primitives/tenant_management.py#L149)||DataSequence[[**TenantStatus**](vmngclient/primitives/tenant_management.py#L54)]|
GET /tenant||[**TenantManagementPrimitives.get_all_tenants**](vmngclient/primitives/tenant_management.py#L154)||DataSequence[[**Tenant**](vmngclient/model/tenant.py#L21)]|
GET /tenant/{tenant_id}||[**TenantManagementPrimitives.get_tenant**](vmngclient/primitives/tenant_management.py#L159)||[**Tenant**](vmngclient/model/tenant.py#L21)|
GET /tenant/vsmart/capacity||[**TenantManagementPrimitives.get_tenant_hosting_capacity_on_vsmarts**](vmngclient/primitives/tenant_management.py#L164)||DataSequence[[**vSmartTenantCapacity**](vmngclient/primitives/tenant_management.py#L103)]|
GET /tenant/vsmart||[**TenantManagementPrimitives.get_tenant_vsmart_mapping**](vmngclient/primitives/tenant_management.py#L169)||[**vSmartTenantMap**](vmngclient/primitives/tenant_management.py#L109)|
PUT /tenant/{tenant_id}||[**TenantManagementPrimitives.update_tenant**](vmngclient/primitives/tenant_management.py#L182)|[**TenantUpdateRequest**](vmngclient/primitives/tenant_management.py#L63)|[**Tenant**](vmngclient/model/tenant.py#L21)|
PUT /tenant/{tenant_id}/vsmart||[**TenantManagementPrimitives.update_tenant_vsmart_placement**](vmngclient/primitives/tenant_management.py#L187)|[**vSmartPlacementUpdateRequest**](vmngclient/primitives/tenant_management.py#L98)||
POST /tenant/{tenant_id}/vsessionid||[**TenantManagementPrimitives.vsession_id**](vmngclient/primitives/tenant_management.py#L192)||[**vSessionId**](vmngclient/primitives/tenant_management.py#L113)|
GET /tenantmigration/download/{path}||[**TenantMigrationPrimitives.download_tenant_data**](vmngclient/primitives/tenant_migration.py#L39)||bytes|
POST /tenantmigration/export||[**TenantMigrationPrimitives.export_tenant_data**](vmngclient/primitives/tenant_migration.py#L43)||[**ExportInfo**](vmngclient/primitives/tenant_migration.py#L16)|
POST /tenantmigration/networkMigration||[**TenantMigrationPrimitives.migrate_network**](vmngclient/primitives/tenant_migration.py#L56)|str|[**MigrationInfo**](vmngclient/primitives/tenant_migration.py#L34)|
