# Copyright 2022 Cisco Systems, Inc. and its affiliates

# type: ignore
import unittest
from unittest.mock import MagicMock, patch

from attr.exceptions import NotAnAttrsClassError
from parameterized import parameterized  # type: ignore

from catalystwan.api.administration import (
    AdministrationSettingsAPI,
    ClusterManagementAPI,
    ResourceGroupsAPI,
    UserGroupsAPI,
    UsersAPI,
)
from catalystwan.dataclasses import (
    Certificate,
    CloudConnectorData,
    CloudServicesSettings,
    Connection,
    Organization,
    Password,
    ServiceConfigurationData,
    Vbond,
)
from catalystwan.endpoints.administration_user_and_group import (
    ResourceGroup,
    ResourceGroupSwitchRequest,
    ResourceGroupUpdateRequest,
    User,
    UserAuthType,
    UserGroup,
    UserGroupTask,
    UserResetRequest,
    UserRole,
    UserUpdateRequest,
)
from catalystwan.exceptions import CatalystwanException
from catalystwan.utils.certificate_status import ValidityPeriod
from catalystwan.utils.creation_tools import create_dataclass

password_dataclass = Password(old_password="old_password_123", new_password="new_password_123")
certificate_dataclass = Certificate("cert", "Name", "Surname", "name@sur.name", ValidityPeriod.ONE_YEAR, 10)
vbond_dataclass = Vbond("1.1.1.1", 1234)
organization_dataclass = Organization("My org name", 1)


class TestUsersAPI(unittest.TestCase):
    @patch("catalystwan.session.ManagerSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.session.api_version = None
        self.session.session_type = None
        self.session.password = "<>"
        self.api = UsersAPI(self.session)
        self.api._endpoints = MagicMock()

    def test_get(self):
        # Arrange
        expected_users = [
            User(
                username="new_user",
                password="new_user",  # pragma: allowlist secret
                group=["netadmin"],
                description="new user",
            )
        ]
        self.api._endpoints.find_users = MagicMock(return_value=expected_users)
        # Act
        observed_users = self.api.get()
        self.api._endpoints.find_users.assert_called_once()
        assert expected_users == observed_users

    def test_get_role(self):
        # Arrange
        expected_user_role = UserRole(isAdmin=True)
        self.api._endpoints.find_user_role = MagicMock(return_value=expected_user_role)
        # Act
        observed_user_role = self.api.get_role()
        # Assert
        self.api._endpoints.find_user_role.assert_called_once()
        assert expected_user_role == observed_user_role

    def test_get_auth_type(self):
        # Arrange
        expected_auth_type = "local"
        self.api._endpoints.find_user_auth_type = MagicMock(
            return_value=UserAuthType(user_auth_type=expected_auth_type)
        )
        # Act
        observed_auth_type = self.api.get_auth_type()
        # Assert
        self.api._endpoints.find_user_auth_type.assert_called_once()
        assert expected_auth_type == observed_auth_type

    def test_create(self):
        # Arrange
        user = User(username="new_user", password="new_user", group=["netadmin"], description="new user")
        self.api._endpoints.create_user = MagicMock()
        # Act
        self.api.create(user)
        # Assert
        self.api._endpoints.create_user.assert_called_once_with(user)

    def test_update(self):
        # Arrange
        user_update = UserUpdateRequest(
            username="new_user",
            password="new_user",  # pragma: allowlist secret
            group=["netadmin"],
            description="new user",
            resource_group="global",
        )
        self.api._endpoints.update_user = MagicMock()
        # Act
        self.api.update(user_update)
        # Assert
        self.api._endpoints.update_user.assert_called_once_with(user_update.username, user_update)

    def test_update_password(self):
        # Arrange
        username = "new_user"
        new_password = "PaSsWoRd"  # pragma: allowlist secret
        self.api._endpoints.update_password = MagicMock()
        # Act
        self.api.update_password(username, new_password)
        # Assert
        self.api._endpoints.update_password.assert_called_once_with(
            username,
            UserUpdateRequest(username=username, password=new_password, current_user_password=self.session.password),
        )

    def test_reset(self):
        # Arrange
        username = "new_user"
        user_reset_request = UserResetRequest(username=username)
        self.api._endpoints.reset_user = MagicMock()
        # Act
        self.api.reset(username)
        # Assert
        self.api._endpoints.reset_user.assert_called_once_with(user_reset_request)

    def test_delete(self):
        # Arrange
        username = "new_user"
        self.api._endpoints.delete_user = MagicMock()
        # Act
        self.api.delete(username)
        # Assert
        self.api._endpoints.delete_user.assert_called_once_with(username)


class TestUserGroupsAPI(unittest.TestCase):
    @patch("catalystwan.session.ManagerSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.session.api_version = None
        self.session.session_type = None
        self.session.password = "<>"
        self.api = UserGroupsAPI(self.session)
        self.api._endpoints = MagicMock()

    def test_get(self):
        # Arrange
        expected_user_groups = [
            UserGroup(
                groupName="new_group", tasks=[UserGroupTask(enabled=True, feature="Alarms", read=True, write=False)]
            )
        ]
        self.api._endpoints.find_user_groups = MagicMock(return_value=expected_user_groups)
        # Act
        observed_user_groups = self.api.get()
        # Assert
        self.api._endpoints.find_user_groups.assert_called_once()
        assert expected_user_groups == observed_user_groups

    def test_create(self):
        # Arrange
        user_group = UserGroup(
            group_name="new_group", tasks=[UserGroupTask(enabled=True, feature="Alarms", read=True, write=False)]
        )
        self.api._endpoints.create_user_group = MagicMock()
        # Act
        self.api.create(user_group)
        # Assert
        self.api._endpoints.create_user_group.assert_called_once_with(user_group)

    def test_update(self):
        # Arrange
        user_group = UserGroup(
            group_name="new_group", tasks=[UserGroupTask(enabled=True, feature="Alarms", read=True, write=False)]
        )
        self.api._endpoints.update_user_group = MagicMock()
        # Act
        self.api.update(user_group)
        # Assert
        self.api._endpoints.update_user_group.assert_called_once_with(user_group.group_name, user_group)

    def test_delete(self):
        # Arrange
        group_name = "new_group"
        self.api._endpoints.delete_user_group = MagicMock()
        # Act
        self.api.delete(group_name)
        # Assert
        self.api._endpoints.delete_user_group.assert_called_once_with(group_name)


class TestResourceGroupsAPI(unittest.TestCase):
    @patch("catalystwan.session.ManagerSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.session.api_version = None
        self.session.session_type = None
        self.session.password = "<>"
        self.api = ResourceGroupsAPI(self.session)
        self.api._endpoints = MagicMock()

    def test_get(self):
        # Arrange
        expected_resource_groups = [
            ResourceGroup(
                id="0:RESGROUP:14567:XD$eD", name="new_resource_group1", desc="New Resource Group #1", site_ids=[200]
            )
        ]
        self.api._endpoints.find_resource_groups = MagicMock(return_value=expected_resource_groups)
        # Act
        observed_resource_groups = self.api.get()
        # Assert
        self.api._endpoints.find_resource_groups.assert_called_once()
        assert expected_resource_groups == observed_resource_groups

    def test_create(self):
        # Arrange
        resource_group = ResourceGroup(name="new_resource_group3", desc="New Resource Group #3", site_ids=[200])
        self.api._endpoints.create_resource_group = MagicMock()
        # Act
        self.api.create(resource_group)
        # Assert
        self.api._endpoints.create_resource_group.assert_called_once_with(resource_group)

    def test_update(self):
        # Arrange
        resource_group_update = ResourceGroupUpdateRequest(
            id="0:RESGROUP:14567:XD$eD", name="new_resource_group1", desc="New Resource Group #1", site_ids=[101, 102]
        )
        self.api._endpoints.update_resource_group = MagicMock()
        # Act
        self.api.update(resource_group_update)
        # Assert
        self.api._endpoints.update_resource_group.assert_called_once_with(
            resource_group_update.id, resource_group_update
        )

    def test_switch(self):
        # Arrange
        resource_group_name = "new_resource_group1"
        self.api._endpoints.switch_resource_group = MagicMock()
        # Act
        self.api.switch(resource_group_name)
        # Assert
        self.api._endpoints.switch_resource_group.assert_called_once_with(
            ResourceGroupSwitchRequest(resource_group_name=resource_group_name)
        )

    def test_delete(self):
        # Arrange
        resource_group_id = "0:RESGROUP:14567:XD$eD"
        self.api._endpoints.delete_resource_group = MagicMock()
        # Act
        self.api.delete(resource_group_id)
        # Assert
        self.api._endpoints.delete_resource_group.assert_called_once_with(resource_group_id)


class TestClusterManagementAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.service_configuration = {
            "vmanageID": "1.1.1.1",
            "deviceIP": "1.1.1.2",
            "services": "none",
        }
        self.service_configuration_dataclass = create_dataclass(ServiceConfigurationData, self.service_configuration)
        self.cluster_management_health_status = [
            {"deviceIP": "localhost"},
            {
                "statistics-db": True,
                "application-server": True,
                "messaging-server": True,
                "configuration-db": True,
                "deviceIP": "localhost",
            },
        ]

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_modify_cluster_setup(self, status_code, expected_outcome, mock_response, mock_session):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = ClusterManagementAPI(mock_session).modify_cluster_setup(self.service_configuration_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.ManagerSession")
    def test_get_cluster_management_health_status(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.cluster_management_health_status
        # Act
        answer = ClusterManagementAPI(mock_session).get_cluster_management_health_status()
        # Assert
        self.assertEqual(answer, self.cluster_management_health_status)


class TestAdministrationSettingsAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.cloud_connector_data = {
            "clientId": "12345",
            "clientSecret": "secret",  # pragma: allowlist secret
            "orgName": "organization",
            "telemetryEnabled": True,
        }
        self.cloud_connector_data_dataclass = create_dataclass(CloudConnectorData, self.cloud_connector_data)
        self.cloud_services_settings = {"enabled": True}
        self.cloud_services_settings_dataclass = create_dataclass(CloudServicesSettings, self.cloud_services_settings)
        self.cloud_on_ramp = [{"": ""}]

    @patch("catalystwan.session.ManagerSession")
    def test_get_sdavc_cloud_connector_config(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = self.cloud_connector_data
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_sdavc_cloud_connector_config()
        # Assert
        self.assertEqual(answer, self.cloud_connector_data_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_enable_sdavc_cloud_connector(self, status_code, expected_outcome, mock_response, mock_session):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).enable_sdavc_cloud_connector(
            self.cloud_connector_data_dataclass
        )
        # Assert
        self.assertEqual(answer, expected_outcome)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_disable_sdavc_cloud_connector(self, status_code, expected_outcome, mock_response, mock_session):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).disable_sdavc_cloud_connector()
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.ManagerSession")
    def test_get_cloud_services(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = [self.cloud_services_settings]
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_cloud_services()
        # Assert
        self.assertEqual(answer, self.cloud_services_settings_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_set_cloud_services(self, status_code, expected_outcome, mock_response, mock_session):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).set_cloud_services(self.cloud_services_settings_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.ManagerSession")
    def test_get_cloud_on_ramp_for_saas_mode(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.cloud_on_ramp
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_cloud_on_ramp_for_saas_mode()
        # Assert
        self.assertEqual(answer, self.cloud_on_ramp)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_enable_cloud_on_ramp_for_saas_mode(self, status_code, expected_outcome, mock_response, mock_session):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).enable_cloud_on_ramp_for_saas_mode(True)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.ManagerSession")
    def test_get_organization(self, mock_session):
        # Arrange
        organization = [{"domain-id": "1", "org": "My org name", "controlConnectionUp": "true"}]
        organization_data = create_dataclass(Organization, organization[0])
        mock_session.get_data.return_value = organization
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_organization()
        # Assert
        self.assertEqual(answer, organization_data)

    @parameterized.expand([[password_dataclass], [certificate_dataclass], [organization_dataclass]])
    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_update(self, payload, mock_response, mock_session):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = 200
        # Act
        answer = AdministrationSettingsAPI(mock_session).update(payload)
        # Assert
        self.assertEqual(answer, True)

    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_update_vbond(self, mock_response, mock_session):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = 200
        # Act
        answer = AdministrationSettingsAPI(mock_session).update(vbond_dataclass)
        # Assert
        self.assertEqual(answer, True)

    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_update_error_with_dataclass(self, mock_response, mock_session):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = 200
        random_dataclass = Connection("random state", "random peer", "127.0.0.1")

        # Act
        def answer():
            AdministrationSettingsAPI(mock_session).update(random_dataclass)

        # Assert
        self.assertRaises(CatalystwanException, answer)

    @patch("catalystwan.session.ManagerSession")
    @patch("requests.Response")
    def test_update_error_without_dataclass(self, mock_response, mock_session):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = 200

        # Act
        def answer():
            AdministrationSettingsAPI(mock_session).update("random_dataclass")

        # Assert
        self.assertRaises(NotAnAttrsClassError, answer)
