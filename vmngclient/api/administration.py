import json
import logging
from enum import Enum
from typing import List, Union, cast

from requests import HTTPError

from vmngclient.dataclasses import CloudConnectorData, CloudServicesSettings, ServiceConfigurationData, User
from vmngclient.exceptions import RetrieveIntervalOutOfRange
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import asdict, create_dataclass

logger = logging.getLogger(__name__)


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotExists(Exception):
    pass


class ValidityPeriod(Enum):
    ONE_YEAR = "1Y"
    TWO_YEARS = "2Y"


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

    def get_organization_name(self) -> List[str]:
        endpoint = "/dataservice/settings/configuration/organization"

        return [organizations_info.get("org") for organizations_info in self.session.get_data(endpoint)]

    def update_organization_name(self, organization_name: str, domain_id: int = 1):
        endpoint = "/dataservice/settings/configuration/organization"
        payload = {"domain-id": domain_id, "org": organization_name}
        try:
            self.session.put(endpoint, json=payload)
        except HTTPError as e:
            error = json.loads(e.response.text).get("error")
            logger.error(f"{error.get('message')} - {error.get('details')}")

    def update_vbond_address(self, vbond_address: str, vbond_port: int) -> bool:
        endpoint = "/dataservice/settings/configuration/device"
        payload = {"domainIp": vbond_address, "port": vbond_port}

        response = self.session.post(endpoint, json=payload)
        logger.debug(f"vBond address set to {vbond_address}, and port set to {vbond_port}")
        return True if response.status_code == 200 else False

    def update_controller_certificate(
        self,
        controller_certificate: str = "",
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        validity_period: ValidityPeriod = ValidityPeriod.ONE_YEAR,
        retrieve_interval: int = 60,
    ) -> bool:
        if retrieve_interval < 1 or retrieve_interval > 60:
            raise RetrieveIntervalOutOfRange("Retrieve interval must be value between 1 and 60 minutes")

        endpoint = "/dataservice/settings/configuration/certificate"
        payload = {
            "certificateSigning": controller_certificate,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "validityPeriod": validity_period.value,
            "retrieveInterval": str(retrieve_interval),
        }
        response = self.session.put(endpoint, json=payload)
        return True if response.status_code == 200 else False

    def change_password(self, old_password: str, new_password: str) -> bool:
        logger.debug("Changing password.")
        endpoint = "/dataservice/admin/user/profile/password"
        payload = {"oldpassword": old_password, "newpassword": new_password}

        response = self.session.put(endpoint, json=payload)
        logger.info("Password changed.")
        return True if response.status_code == 200 else False
