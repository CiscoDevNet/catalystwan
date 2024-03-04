# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.typed_list import DataSequence


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    username: str = Field(serialization_alias="userName", validation_alias="userName")
    password: Optional[str] = None
    group: List[str]
    locale: Optional[str] = None
    description: Optional[str] = None
    resource_group: Optional[str] = Field(
        default=None,
        serialization_alias="resGroupName",
        validation_alias="resGroupName",
        description="can be set only for >=20.5, <20.13 where default value is 'global'",
    )
    resource_domain: Optional[str] = Field(
        default=None,
        serialization_alias="resourceDomainName",
        validation_alias="resourceDomainName",
        description="can be set only for >=20.13 where default value is 'all'",
    )


class UserUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    username: str = Field(serialization_alias="userName", validation_alias="userName")
    current_password: bool = Field(
        serialization_alias="currentPassword", validation_alias="currentPassword", default=False
    )
    show_password: bool = Field(serialization_alias="showPassword", validation_alias="showPassword", default=False)
    show_confirm_password: bool = Field(
        serialization_alias="showConfirmPassword", validation_alias="showConfirmPassword", default=False
    )
    current_user_password: Optional[str] = Field(
        default=None,
        serialization_alias="currentUserPassword",
        validation_alias="currentUserPassword",
    )
    password: Optional[str] = None
    group: Optional[List[str]] = None
    locale: Optional[str] = None
    description: Optional[str] = None
    resource_group: Optional[str] = Field(
        default=None,
        serialization_alias="resGroupName",
        validation_alias="resGroupName",
        description="can be set only for >=20.5, <20.13 where default value is 'global'",
    )
    resource_domain: Optional[str] = Field(
        default=None,
        serialization_alias="resourceDomainName",
        validation_alias="resourceDomainName",
        description="can be set only for >=20.13 where default value is 'all'",
    )


class UserRole(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    is_admin: bool = Field(serialization_alias="isAdmin", validation_alias="isAdmin")


class UserAuthType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_auth_type: str = Field(serialization_alias="userAuthType", validation_alias="userAuthType")


class UserGroupTask(BaseModel):
    enabled: bool
    feature: str
    read: bool
    write: bool


class UserGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    group_name: str = Field(serialization_alias="groupName", validation_alias="groupName")
    tasks: List[UserGroupTask]

    def __map_task_index_by_feature(self) -> Dict[str, int]:
        """Returns a mapping of internal task list index by feature name the task contains"""
        return {task.feature: index for index, task in enumerate(self.tasks)}

    def get_task(self, feature: str) -> Optional[UserGroupTask]:
        """Returns task object by feature name if found"""
        if index := self.__map_task_index_by_feature().get(feature, None) is not None:
            return self.tasks[index]
        return None

    def update_task(self, task: UserGroupTask):
        """Updates existing task entry or creates new entry if not exist"""
        if index := self.__map_task_index_by_feature().get(task.feature, None) is not None:
            self.tasks[index] = task
        else:
            self.tasks.append(task)

    def enable_read(self, features: Set[str]):
        """Enables read-only permissions for given feature set"""
        for feature in features:
            self.update_task(UserGroupTask(enabled=True, feature=feature, read=True, write=False))

    def enable_read_and_write(self, features: Set[str]):
        """Enables read-write permissions for given feature set"""
        for feature in features:
            self.update_task(UserGroupTask(enabled=True, feature=feature, read=True, write=True))

    def disable(self, features: Set[str]):
        """Disables access permissions for given feature set"""
        for feature in features:
            self.update_task(UserGroupTask(enabled=False, feature=feature, read=False, write=False))


class UserResetRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    username: str = Field(serialization_alias="userName", validation_alias="userName")


class ActiveSession(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    uuid: str
    source_ip: Optional[str] = Field(default=None, serialization_alias="sourceIp", validation_alias="sourceIp")
    remote_host: Optional[str] = Field(default=None, serialization_alias="remoteHost", validation_alias="remoteHost")
    raw_username: Optional[str] = Field(default=None, serialization_alias="rawUserName", validation_alias="rawUserName")
    raw_id: Optional[str] = Field(default=None, serialization_alias="rawId", validation_alias="rawId")
    tenant_domain: Optional[str] = Field(
        default=None, serialization_alias="tenantDomain", validation_alias="tenantDomain"
    )
    user_group: Optional[str] = Field(
        default=None, serialization_alias="userGroup", validation_alias="userGroup"
    )  # workaround: should be List[str] but JSON array is quoted in response
    user_mode: Optional[str] = Field(default=None, serialization_alias="userMode", validation_alias="userMode")
    create_date_time: Optional[datetime] = Field(
        default=None, serialization_alias="createDateTime", validation_alias="createDateTime"
    )
    tenant_id: Optional[str] = Field(default=None, serialization_alias="tenantId", validation_alias="tenantId")
    last_accessed_time: Optional[datetime] = Field(
        default=None, serialization_alias="lastAccessedTime", validation_alias="lastAccessedTime"
    )


class SessionsDeleteRequest(BaseModel):
    data: List[ActiveSession]

    @classmethod
    def from_active_session_list(cls, sessions: List[ActiveSession]) -> "SessionsDeleteRequest":
        sessions_delete_request = SessionsDeleteRequest(data=[])
        for session in sessions:
            sessions_delete_request.data.append(
                ActiveSession(uuid=session.uuid, tenantId=session.tenant_id, rawId=session.raw_id)  # type: ignore
            )
        return sessions_delete_request


class InvalidateSessionMessage(BaseModel):
    message: Optional[str] = None


class ProfilePasswordUpdateRequest(BaseModel):
    oldpassword: str
    newpassword: str


class ResourceGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = None
    name: str
    desc: str
    site_ids: List[int] = Field(serialization_alias="siteIds", validation_alias="siteIds")
    device_ips: Optional[List[str]] = Field(default=None, serialization_alias="deviceIPs", validation_alias="deviceIPs")
    mgmt_sytem_ips_map: Optional[Dict[str, str]] = Field(
        default=None, serialization_alias="mgmtSytemIpsMap", validation_alias="mgmtSytemIpsMap"
    )
    uuid_sytem_ips_map: Optional[Dict[str, str]] = Field(
        default=None, serialization_alias="uuidSytemIpsMap", validation_alias="uuidSytemIpsMap"
    )


class ResourceGroupUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    name: str
    desc: str
    site_ids: List[int] = Field(serialization_alias="siteIds", validation_alias="siteIds")


class ResourceGroupSwitchRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    resource_group_name: str = Field(serialization_alias="resourceGroupName", validation_alias="resourceGroupName")


class AdministrationUserAndGroup(APIEndpoints):
    def create_colo_group(self):
        # POST /admin/cologroup
        ...

    def create_group_grid_columns(self):
        # GET /admin/usergroup/definition
        ...

    @post("/admin/user")
    def create_user(self, payload: User) -> None:
        ...

    @post("/admin/usergroup")
    def create_user_group(self, payload: UserGroup) -> None:
        ...

    def create_vpn_group(self):
        # POST /admin/vpngroup
        ...

    def delete_colo_group(self):
        # DELETE /admin/cologroup/{id}
        ...

    @delete("/admin/user/{username}")
    def delete_user(self, username: str) -> None:
        ...

    @delete("/admin/usergroup/{group_name}")
    def delete_user_group(self, group_name: str) -> None:
        ...

    def delete_vpn_group(self):
        # DELETE /admin/vpngroup/{id}
        ...

    def edit_colo_group(self):
        # PUT /admin/cologroup/{id}
        ...

    def edit_vpn_group(self):
        # PUT /admin/vpngroup/{id}
        ...

    @get("/admin/user/userAuthType")
    def find_user_auth_type(self) -> UserAuthType:
        ...

    @get("/admin/usergroup", "data")
    def find_user_groups(self) -> DataSequence[UserGroup]:
        ...

    def find_user_groups_as_key_value(self):
        # GET /admin/usergroup/keyvalue
        ...

    @get("/admin/user/role")
    def find_user_role(self) -> UserRole:
        ...

    @get("/admin/user", "data")
    def find_users(self) -> DataSequence[User]:
        ...

    @get("/admin/user/activeSessions", "data")
    def get_active_sessions(self) -> DataSequence[ActiveSession]:
        ...

    def get_colo_groups(self):
        # GET /admin/cologroup
        ...

    def get_vpn_groups(self):
        # GET /admin/vpngroup
        ...

    @delete("/admin/user/removeSessions", "data")
    def remove_sessions(self, payload: SessionsDeleteRequest) -> InvalidateSessionMessage:
        ...

    @post("/admin/user/reset")
    def reset_user(self, payload: UserResetRequest) -> None:
        ...

    @versions(">20.4, <20.13")
    @get("/admin/resourcegroup")
    def find_resource_groups(self) -> DataSequence[ResourceGroup]:
        ...

    @versions(">20.4, <20.13")
    @post("/admin/resourcegroup/switch")
    def switch_resource_group(self, payload: ResourceGroupSwitchRequest) -> None:
        ...

    @versions(">20.4, <20.13")
    @put("/admin/resourcegroup/{group_id}")
    def update_resource_group(self, group_id: str, payload: ResourceGroupUpdateRequest) -> None:
        ...

    @versions(">20.4, <20.13")
    @delete("/admin/resourcegroup/{group_id}", json={})
    def delete_resource_group(self, group_id: str) -> None:
        ...

    @versions(">20.4, <20.13")
    @post("/admin/resourcegroup")
    def create_resource_group(self, payload: ResourceGroup) -> None:
        ...

    @versions(">20.4, <20.13")
    def resource_group_name(self):
        # GET /admin/user/resourceGroupName
        ...

    def update_admin_password(self):
        # POST /admin/user/admin/password
        ...

    @put("/admin/user/password/{username}")
    def update_password(self, username: str, payload: UserUpdateRequest) -> None:
        ...

    def update_profile_locale(self):
        # PUT /admin/user/profile/locale
        ...

    @put("/admin/user/profile/password")
    def update_profile_password(self, payload: ProfilePasswordUpdateRequest) -> None:
        ...

    @put("/admin/user/{username}")
    def update_user(self, username: str, payload: UserUpdateRequest) -> None:
        ...

    @put("/admin/usergroup/{group_name}")
    def update_user_group(self, group_name: str, payload: UserGroup) -> None:
        ...

    def validate_password(self):
        # POST /admin/user/password/validate
        ...
