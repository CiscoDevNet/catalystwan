# Copyright 2022 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, List, Union, cast, overload

from requests import Response
from typing_extensions import deprecated

from catalystwan.dataclasses import (
    Certificate,
    CloudConnectorData,
    CloudServicesSettings,
    Organization,
    Password,
    ServiceConfigurationData,
    SoftwareInstallTimeout,
    Vbond,
)
from catalystwan.endpoints.administration_user_and_group import (
    ActiveSession,
    AdministrationUserAndGroup,
    InvalidateSessionMessage,
    ResourceGroup,
    ResourceGroupSwitchRequest,
    ResourceGroupUpdateRequest,
    SessionsDeleteRequest,
    User,
    UserGroup,
    UserResetRequest,
    UserRole,
    UserUpdateRequest,
)
from catalystwan.exceptions import CatalystwanDeprecationWarning, CatalystwanException
from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import asdict, create_dataclass

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class UsersAPI:
    """Class implementing methods for user managment.

    Attributes:
        session: logged in API client session

    Usage example:
        # Create session
        session = create_manager_session(...)
        # Get information about all users
        all_users = session.api.users.get()
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self._endpoints = AdministrationUserAndGroup(session)

    def get(self) -> DataSequence[User]:
        """List all users

        Returns:
            DataSequence[User]: List-like object representing users
        """
        return self._endpoints.find_users()

    def get_role(self) -> UserRole:
        """Get currently logged user role

        Returns:
            UserRole: Currently logged user role information
        """
        return self._endpoints.find_user_role()

    def get_auth_type(self) -> str:
        """Get currently logged user authentication type

        Returns:
            str: Currently logged user authentication type
        """
        return self._endpoints.find_user_auth_type().user_auth_type

    def create(self, user: User):
        """Creates a new user

        Args:
            user (User): Definition of new user to be created
        """
        self._endpoints.create_user(user)

    def update(self, user_update_request: UserUpdateRequest):
        """Updates existing user

        Args:
            user_update_request (UserUpdateRequest): User attributes to be updated
        """
        self._endpoints.update_user(user_update_request.username, user_update_request)

    def update_password(self, username: str, new_password: str):
        """Updates exisiting user password

        Args:
            username (str): Name of the user
            new_password (str): New password for given user
        """
        update_password_request = UserUpdateRequest(
            username=username, password=new_password, current_user_password=self.session.password
        )  # type: ignore
        self._endpoints.update_password(username, update_password_request)

    def reset(self, username: str):
        """Resets given user (unlocks blocked user eg. after number of unsuccessfull login attempts)

        Args:
            username (str): Name of the user to be unlocked
        """
        self._endpoints.reset_user(UserResetRequest(username=username))

    def delete(self, username: str):
        """Deletes given user

        Args:
            username (str): Name of the user to be deleted
        """
        self._endpoints.delete_user(username)


class UserGroupsAPI:
    """Class implementing methods for user group management."""

    def __init__(self, session: ManagerSession):
        self.session = session
        self._endpoints = AdministrationUserAndGroup(session)

    def get(self) -> DataSequence[UserGroup]:
        """List all user groups

        Returns:
            DataSequence[UserGroup]: List-like object representing user groups
        """
        return self._endpoints.find_user_groups()

    def create(self, user_group: UserGroup):
        """Creates a new user group

        Args:
            user_group (UserGroup): Definition of user group to be created
        """
        self._endpoints.create_user_group(user_group)

    def update(self, user_group: UserGroup):
        """Updates existing user group

        Args:
            user_group (UserGroup): User group attributes to be updated
        """
        self._endpoints.update_user_group(user_group.group_name, user_group)

    def delete(self, group_name: str):
        """Deletes given user group

        Args:
            group_name (str): Name of the user group to be deleted
        """
        self._endpoints.delete_user_group(group_name)


class ResourceGroupsAPI:
    """Class implementing methods for resource groups management."""

    def __init__(self, session: ManagerSession):
        self.session = session
        self._endpoints = AdministrationUserAndGroup(session)

    def get(self) -> DataSequence[ResourceGroup]:
        """List all resource groups

        Returns:
            DataSequence[ResourceGroup]: List-like object containing user groups information
        """
        return self._endpoints.find_resource_groups()

    def create(self, resource_group: ResourceGroup):
        """Creates a new resource group

        Args:
            resource_group (ResourceGroup): Definition of new resource group to be created
        """
        self._endpoints.create_resource_group(resource_group)

    def update(self, resource_group_update_request: ResourceGroupUpdateRequest):
        """Updates existing resource group

        Args:
            resource_group_update_request (ResourceGroupUpdateRequest): Object containing existing
            resource group id and attributes to be updated
        """
        self._endpoints.update_resource_group(resource_group_update_request.id, resource_group_update_request)

    def switch(self, resource_group_name: str):
        """Switch to view only a specific resource group (for global admin only)

        Args:
            resource_group_name (str): Name of resource group to switch view
        """
        switch_request = ResourceGroupSwitchRequest(resource_group_name=resource_group_name)
        self._endpoints.switch_resource_group(switch_request)

    def delete(self, resource_group_id: str):
        """Deletes a given resource group

        Args:
            resource_group_id (str): Resource group id
        """
        self._endpoints.delete_resource_group(resource_group_id)


class SessionsAPI:
    """Class implementing methods for vmanage sessions management."""

    def __init__(self, session: ManagerSession):
        self.session = session
        self._endpoints = AdministrationUserAndGroup(session)

    def get(self) -> DataSequence[ActiveSession]:
        """List all active sessions

        Returns:
            DataSequence[ActiveSession]: List-like object representing active user sessions
        """
        return self._endpoints.get_active_sessions()

    def invalidate(self, sessions: List[ActiveSession]) -> InvalidateSessionMessage:
        """Invalidates given sessions

        Args:
            sessions (List[ActiveSession]): List of active sessions

        Returns:
            InvalidateSessionMessage: Information about invalidation result
        """
        sessions_delete_request = SessionsDeleteRequest.from_active_session_list(sessions)
        return self._endpoints.remove_sessions(sessions_delete_request)


class ClusterManagementAPI:
    """Covers clusterManagement API calls.

    Attributes:
        session: logged in API admin session

    Example usage:
        # Create session
        session = create_manager_session(...)
        # Get health status
        health_status = session.api.cluster_management.get_cluster_management_health_status()
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session

    def modify_cluster_setup(self, service_configuration: ServiceConfigurationData) -> bool:
        """Updates vManage cluster configuration.

        Args:
            service_configuration: vManage cluster config
        """
        url_path = "/dataservice/clusterManagement/setup"
        data = asdict(service_configuration)  # type: ignore
        response = self.session.put(url_path, json=data)
        return True if response.status_code == 200 else False

    def get_cluster_management_health_status(self) -> Union[dict, list]:
        """Gets Cluster Management Service Reachability health status.

        Returns:
            TODO return health status dataclass
        """
        url_path = "/dataservice/clusterManagement/health/status"
        return self.session.get_data(url_path)


class AdministrationSettingsAPI:
    def __init__(self, session: ManagerSession) -> None:
        """Covers Administration Settings API calls.

        Args:
            session: logged in API admin session

        Example usage:
            - to update e.g. password:
                password = Password(old_password="qwer1234", new_password="asdf9876")
                AdministrationSettingsAPI(session).update(password)
        """
        self.session = session

    def get_sdavc_cloud_connector_config(self) -> CloudConnectorData:
        """Gets SD-AVC Cloud Connector Config.

        Returns:
            CloudConnector dataclass config
        """
        url_path = "/dataservice/sdavc/cloudconnector"
        response = cast(dict, self.session.get_json(url_path))
        return create_dataclass(CloudConnectorData, response)

    def enable_sdavc_cloud_connector(self, cloud_connector: CloudConnectorData) -> bool:
        """Enables SD-AVC Cloud Connector on vManage."""
        url_path = "/dataservice/sdavc/cloudconnector"
        data = asdict(cloud_connector)  # type: ignore
        response = self.session.post(url_path, json=data)
        return True if response.status_code == 200 else False

    def disable_sdavc_cloud_connector(self) -> bool:
        """Disables SD-AVC Cloud Connector on vManage."""
        url_path = "/dataservice/sdavc/cloudconnector"
        data = {"cloudEnabled": False}
        response = self.session.put(url_path, data)
        return True if response.status_code == 200 else False

    def get_cloud_services(self) -> CloudServicesSettings:
        url_path = "/dataservice/settings/configuration/cloudservices"
        data = self.session.get_data(url_path)[0]
        return create_dataclass(CloudServicesSettings, data)

    def set_cloud_services(self, config: CloudServicesSettings) -> bool:
        url_path = "/dataservice/settings/configuration/cloudservices"
        response = self.session.post(url_path, asdict(config))  # type: ignore
        return True if response.status_code == 200 else False

    def get_cloud_on_ramp_for_saas_mode(self):
        """Get information about Cloud on Ramp for Saas mode"""
        url_path = "/dataservice/settings/configuration/cloudx"
        return self.session.get_data(url_path)

    def enable_cloud_on_ramp_for_saas_mode(self, disable=False):
        """Enable or disable COR for SaaS"""
        url_path = "/dataservice/settings/configuration/cloudx"
        data = {"mode": "on"} if not disable else {"mode": "off"}
        response = self.session.put(url_path, data)
        return True if response.status_code == 200 else False

    @deprecated(
        "Use .endpoints.configuration_settings.get_organizations() instead", category=CatalystwanDeprecationWarning
    )
    def get_organization(self) -> Organization:
        endpoint = "/dataservice/settings/configuration/organization"

        return create_dataclass(Organization, self.session.get_data(endpoint)[0])

    def get_software_install_timeout(self) -> SoftwareInstallTimeout:
        url_path = "/settings/configuration/softwareMaintenance"

        return create_dataclass(SoftwareInstallTimeout, self.session.get_data(url_path)[0])

    def set_software_install_timeout(self, download_timeout_min: int, activate_timeout_min: int):
        MINIMAL_DOWNLOAD_TIMEOUT_MIN = 60
        MINIMAL_ACTIVATE_TIMEOUT_MIN = 30
        assert download_timeout_min >= MINIMAL_DOWNLOAD_TIMEOUT_MIN
        assert activate_timeout_min >= MINIMAL_ACTIVATE_TIMEOUT_MIN

        url_path = "/settings/configuration/softwareMaintenance"
        data = asdict(SoftwareInstallTimeout(download_timeout_min, activate_timeout_min))  # type: ignore
        response = self.session.post(url_path, json=data)
        return True if response.status_code == 200 else False

    @overload
    def update(self, payload: Password) -> bool:
        ...

    @overload
    def update(self, payload: Certificate) -> bool:
        ...

    @overload
    def update(self, payload: Vbond) -> bool:
        ...

    @overload
    def update(self, payload: Organization) -> bool:
        ...

    def update(self, payload: Union[Organization, Certificate, Password, Vbond]) -> bool:
        json_payload = asdict(payload)  # type: ignore
        if isinstance(payload, Organization):
            response = self.__update_organization(json_payload)
        elif isinstance(payload, Certificate):
            response = self.__update_certificate(payload)
        elif isinstance(payload, Password):
            response = self.__update_password(json_payload)
        elif isinstance(payload, Vbond):
            response = self.__update_vbond(json_payload)
        else:
            raise CatalystwanException(f"Not supported payload type: {type(payload).__name__}")

        return True if response.status_code == HTTPStatus.OK else False

    def __update_password(self, payload: dict) -> Response:
        endpoint = "/dataservice/admin/user/profile/password"
        response = self.session.put(endpoint, json=payload)
        logger.info("Password changed.")
        return response

    def __update_certificate(self, payload: Certificate) -> Response:
        json_payload = asdict(payload)  # type: ignore
        endpoint = "/dataservice/settings/configuration/certificate"
        return self.session.put(endpoint, json=json_payload)

    def __update_vbond(self, payload: dict) -> Response:
        endpoint = "/dataservice/settings/configuration/device"
        return self.session.post(endpoint, json=payload)

    @deprecated(
        "Use .endpoints.configuration_settings.edit_organizations() instead", category=CatalystwanDeprecationWarning
    )
    def __update_organization(self, payload: dict) -> Response:
        endpoint = "/dataservice/settings/configuration/organization"
        del payload["controlConnectionUp"]
        return self.session.put(endpoint, json=payload)
