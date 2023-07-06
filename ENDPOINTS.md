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
POST /tenant/bulk/async||[**TenantManagementPrimitives.create_tenant_async_bulk**](vmngclient/primitives/tenant_management.py#L88)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**TenantTaskId**](vmngclient/primitives/tenant_management.py#L21)|
GET /client/server||[**ClientPrimitives.server**](vmngclient/primitives/client.py#L61)||[**ServerInfo**](vmngclient/primitives/client.py#L21)|
GET /client/about||[**ClientPrimitives.about**](vmngclient/primitives/client.py#L65)||[**AboutInfo**](vmngclient/primitives/client.py#L49)|
