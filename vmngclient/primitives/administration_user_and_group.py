from datetime import datetime
from typing import Dict, List, Optional, Set

from pydantic import BaseModel, Field

from vmngclient.primitives import APIPrimitiveBase
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


class AdministrationUserAndGroupPrimitives(APIPrimitiveBase):
    def create_colo_group(self):
        # POST /admin/cologroup
        ...

    def create_group_grid_columns(self):
        # GET /admin/usergroup/definition
        ...

    def create_user(self, user: User):
        self._post("/admin/user", payload=user)

    def create_user_group(self, user_group: UserGroup):
        self._post("/admin/usergroup", payload=user_group)

    def create_vpn_group(self):
        # POST /admin/vpngroup
        ...

    def delete_colo_group(self):
        # DELETE /admin/cologroup/{id}
        ...

    def delete_user(self, username: str):
        self._delete(f"/admin/user/{username}")

    def delete_user_group(self, group_name: str):
        self._delete(f"/admin/usergroup/{group_name}")

    def delete_vpn_group(self):
        # DELETE /admin/vpngroup/{id}
        ...

    def edit_colo_group(self):
        # PUT /admin/cologroup/{id}
        ...

    def edit_vpn_group(self):
        # PUT /admin/vpngroup/{id}
        ...

    def find_user_auth_type(self) -> UserAuthType:
        return self._get("/admin/user/userAuthType").dataobj(UserAuthType, None)

    def find_user_groups(self) -> DataSequence[UserGroup]:
        return self._get("/admin/usergroup").dataseq(UserGroup)

    def find_user_groups_as_key_value(self):
        # GET /admin/usergroup/keyvalue
        ...

    def find_user_role(self) -> UserRole:
        return self._get("/admin/user/role").dataobj(UserRole, None)

    def find_users(self) -> DataSequence[User]:
        return self._get("/admin/user").dataseq(User)

    def get_active_sessions(self) -> DataSequence[ActiveSession]:
        return self._get("/admin/user/activeSessions").dataseq(ActiveSession)

    def get_colo_groups(self):
        # GET /admin/cologroup
        ...

    def get_vpn_groups(self):
        # GET /admin/vpngroup
        ...

    def remove_sessions(self, sessions_delete_request: SessionsDeleteRequest) -> InvalidateSessionMessage:
        response = self._delete("/admin/user/removeSessions", payload=sessions_delete_request)
        return response.dataobj(InvalidateSessionMessage)

    def reset_user(self, user_reset_request: UserResetRequest):
        self._post("/admin/user/reset", payload=user_reset_request)

    def find_resource_groups(self) -> DataSequence[ResourceGroup]:
        # GET /admin/resourcegroup
        return self._get("/admin/resourcegroup").dataseq(ResourceGroup, None)

    def switch_resource_group(self, resource_group_switch_request: ResourceGroupSwitchRequest):
        # POST /admin/resourcegroup/switch
        self._post("/admin/resourcegroup/switch", payload=resource_group_switch_request)

    def update_resource_group(self, group_id: str, resource_group_update_request: ResourceGroupUpdateRequest):
        # PUT /admin/resourcegroup/{groupId}
        self._put(f"/admin/resourcegroup/{group_id}", payload=resource_group_update_request)

    def delete_resource_group(self, group_id: str):
        # DELETE /admin/resourcegroup/{groupId}
        self._delete(f"/admin/resourcegroup/{group_id}", json={})

    def create_resource_group(self, resource_group: ResourceGroup):
        # POST /admin/resourcegroup
        self._post("/admin/resourcegroup", payload=resource_group)

    def resource_group_name(self):
        # GET /admin/user/resourceGroupName
        ...

    def update_admin_password(self):
        # POST /admin/user/admin/password
        ...

    def update_password(self, username: str, update_user_request: UserUpdateRequest):
        self._put(f"/admin/user/password/{username}", payload=update_user_request)

    def update_profile_locale(self):
        # PUT /admin/user/profile/locale
        ...

    def update_profile_password(self, profile_password_update_request: ProfilePasswordUpdateRequest):
        self._put("/admin/user/profile/password", payload=profile_password_update_request)

    def update_user(self, username: str, user_update_request: UserUpdateRequest):
        self._put(f"/admin/user/{username}", payload=user_update_request)

    def update_user_group(self, group_name: str, user_group: UserGroup):
        self._put(f"/admin/usergroup/{group_name}", payload=user_group)

    def validate_password(self):
        # POST /admin/user/password/validate
        ...
