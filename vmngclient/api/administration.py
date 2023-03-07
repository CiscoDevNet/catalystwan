from __future__ import annotations

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, List, Union, cast, overload

from requests import Response

from vmngclient.dataclasses import (
    Certificate,
    CloudConnectorData,
    CloudServicesSettings,
    Organization,
    Password,
    ServiceConfigurationData,
    SoftwareInstallTimeout,
    User,
    Vbond,
)
from vmngclient.exceptions import InvalidOperationError
from vmngclient.utils.creation_tools import asdict, create_dataclass

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotExists(Exception):
    pass


class UsersAPI:
    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def get_all_users(self) -> List[User]:
        url_path = "/dataservice/admin/user"
        users = self.session.get_data(url_path)
        logger.debug(f"List of users: {users}")
        return [create_dataclass(User, user) for user in users]

    def exists(self, username: str) -> bool:
        return username in [user.username for user in self.get_all_users()]

    def create_user(self, user: User) -> bool:
        if self.exists(user.username):
            raise UserAlreadyExistsError(f"{user.username} already exists.")
        url_path = "/dataservice/admin/user"
        data = asdict(user)  # type: ignore

        response = self.session.post(url=url_path, json=data)
        logger.info(response)
        return True if response.status_code == 200 else False

    def delete_user(self, username: str) -> bool:
        if not self.exists(username):
            raise UserDoesNotExists(f"{username} does not exists.")
        url_path = f"/dataservice/admin/user/{username}"
        logger.debug(f"Deleting user {username}.")
        response = self.session.delete(url_path)
        return True if response.status_code == 200 else False


class ClusterManagementAPI:
    """Covers clusterManagement API calls.

    Attributes:
        session: logged in API admin session
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def modify_cluster_setup(self, service_configuration: ServiceConfigurationData) -> bool:
        """Updates vManage cluster configuration.

        Args:
            service_configuration: vManage cluster config
        """
        url_path = "/dataservice/clusterManagement/setup"
        data = asdict(service_configuration)  # type: ignore
        response = self.session.put(url_path, data)
        return True if response.status_code == 200 else False

    def get_cluster_management_health_status(self) -> Union[dict, list]:
        """Gets Cluster Management Service Reachability health status.

        Returns:
            TODO return health status dataclass
        """
        url_path = "/dataservice/clusterManagement/health/status"
        return self.session.get_data(url_path)


class AdministrationSettingsAPI:
    def __init__(self, session: vManageSession) -> None:
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
            raise InvalidOperationError(f"Not supported payload type: {type(payload).__name__}")

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

    def __update_organization(self, payload: dict) -> Response:
        endpoint = "/dataservice/settings/configuration/organization"
        del payload["controlConnectionUp"]
        return self.session.put(endpoint, json=payload)
