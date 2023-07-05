**THIS FILE IS AUTO-GENERATED DO NOT EDIT**

All URIs are relative to */dataservice*
HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode
------------ | ------------------ | ------ | ------------ | ----------- | ------------
POST /admin/user||[**AdministrationUserAndGroupPrimitives.create_user**](vmngclient/primitives/administration_user_and_group.py#L157)|[**User**](vmngclient/primitives/administration_user_and_group.py#L11)||
POST /admin/usergroup||[**AdministrationUserAndGroupPrimitives.create_user_group**](vmngclient/primitives/administration_user_and_group.py#L161)|[**UserGroup**](vmngclient/primitives/administration_user_and_group.py#L48)||
DELETE /admin/usergroup/{group_name}||[**AdministrationUserAndGroupPrimitives.delete_user_group**](vmngclient/primitives/administration_user_and_group.py#L176)|||
GET /admin/user/userAuthType||[**AdministrationUserAndGroupPrimitives.find_user_auth_type**](vmngclient/primitives/administration_user_and_group.py#L192)||[**UserAuthType**](vmngclient/primitives/administration_user_and_group.py#L37)|
GET /admin/usergroup||[**AdministrationUserAndGroupPrimitives.find_user_groups**](vmngclient/primitives/administration_user_and_group.py#L196)||DataSequence[[**UserGroup**](vmngclient/primitives/administration_user_and_group.py#L48)]|
GET /admin/resourcegroup||[**AdministrationUserAndGroupPrimitives.find_resource_groups**](vmngclient/primitives/administration_user_and_group.py#L228)||DataSequence[[**ResourceGroup**](vmngclient/primitives/administration_user_and_group.py#L127)]|
PUT /admin/user/password/{username}||[**AdministrationUserAndGroupPrimitives.update_password**](vmngclient/primitives/administration_user_and_group.py#L256)|[**UserUpdateRequest**](vmngclient/primitives/administration_user_and_group.py#L20)||
POST /tenant/bulk/async||[**TenantManagementPrimitives.create_tenant_async_bulk**](vmngclient/primitives/tenant_management.py#L88)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**TenantTaskId**](vmngclient/primitives/tenant_management.py#L21)|