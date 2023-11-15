# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import Dict, List, Optional, Set

from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.typed_list import DataSequence


class User(BaseModel):
    username: str = Field(alias="userName")
    password: Optional[str]
    group: List[str]
    locale: Optional[str]
    description: Optional[str]
    resource_group: Optional[str] = Field(alias="resGroupName")


class UserUpdateRequest(BaseModel):
    username: str = Field(alias="userName")
    current_password: bool = Field(alias="currentPassword", default=False)
    show_password: bool = Field(alias="showPassword", default=False)
    show_confirm_password: bool = Field(alias="showConfirmPassword", default=False)
    current_user_password: Optional[str] = Field(alias="currentUserPassword")
    password: Optional[str]
    group: Optional[List[str]]
    locale: Optional[str]
    description: Optional[str]
    resource_group: Optional[str] = Field(alias="resGroupName")


class UserRole(BaseModel):
    is_admin: bool = Field(alias="isAdmin")


class UserAuthType(BaseModel):
    user_auth_type: str = Field(alias="userAuthType")


class UserGroupTask(BaseModel):
    enabled: bool
    feature: str
    read: bool
    write: bool


class UserGroup(BaseModel):
    group_name: str = Field(alias="groupName")
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
    username: str = Field(alias="userName")


class ActiveSession(BaseModel):
    uuid: str
    source_ip: Optional[str] = Field(alias="sourceIp")
    remote_host: Optional[str] = Field(alias="remoteHost")
    raw_username: Optional[str] = Field(alias="rawUserName")
    raw_id: Optional[str] = Field(alias="rawId")
    tenant_domain: Optional[str] = Field(alias="tenantDomain")
    user_group: Optional[str] = Field(
        alias="userGroup"
    )  # workaround: should be List[str] but JSON array is quoted in response
    user_mode: Optional[str] = Field(alias="userMode")
    create_date_time: Optional[datetime] = Field(alias="createDateTime")
    tenant_id: Optional[str] = Field(alias="tenantId")
    last_accessed_time: Optional[datetime] = Field(alias="lastAccessedTime")


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
    message: Optional[str]


class ProfilePasswordUpdateRequest(BaseModel):
    oldpassword: str
    newpassword: str


class ResourceGroup(BaseModel):
    id: Optional[str]
    name: str
    desc: str
    site_ids: List[int] = Field(alias="siteIds")
    device_ips: Optional[List[str]] = Field(alias="deviceIPs")
    mgmt_sytem_ips_map: Optional[Dict[str, str]] = Field(alias="mgmtSytemIpsMap")
    uuid_sytem_ips_map: Optional[Dict[str, str]] = Field(alias="uuidSytemIpsMap")


class ResourceGroupUpdateRequest(BaseModel):
    id: str
    name: str
    desc: str
    site_ids: List[int] = Field(alias="siteIds")


class ResourceGroupSwitchRequest(BaseModel):
    resource_group_name: str = Field(alias="resourceGroupName")


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

    @get("/admin/resourcegroup")
    def find_resource_groups(self) -> DataSequence[ResourceGroup]:
        ...

    @post("/admin/resourcegroup/switch")
    def switch_resource_group(self, payload: ResourceGroupSwitchRequest) -> None:
        ...

    @put("/admin/resourcegroup/{group_id}")
    def update_resource_group(self, group_id: str, payload: ResourceGroupUpdateRequest) -> None:
        ...

    @delete("/admin/resourcegroup/{group_id}", json={})
    def delete_resource_group(self, group_id: str) -> None:
        ...

    @post("/admin/resourcegroup")
    def create_resource_group(self, payload: ResourceGroup) -> None:
        ...

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
