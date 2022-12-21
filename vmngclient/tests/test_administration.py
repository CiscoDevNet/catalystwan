import unittest
from unittest.mock import patch

from parameterized import parameterized  # type: ignore

from vmngclient.api.administration import (
    AdministrationSettingsAPI,
    ClusterManagementAPI,
    UserAlreadyExistsError,
    UserDoesNotExists,
    UsersAPI,
)
from vmngclient.dataclasses import CloudConnectorData, CloudServicesSettings, ServiceConfigurationData, User
from vmngclient.utils.creation_tools import create_dataclass


class TestUsersAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.users = [
            {"userName": "admin", "locale": "en_US", "group": []},
            {
                "userName": "demo_user",
                "password": "qwer",
                "description": "Demo User",
                "resGroupName": "group1",
                "locale": "en_US",
                "group": ["basic"],
            },
        ]
        self.user_dataclass = [create_dataclass(User, user) for user in self.users]

    @patch("vmngclient.session.Session")
    def test_get_all_users(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.users
        # Act
        answer = UsersAPI(mock_session).get_all_users()
        # Assert
        self.assertEqual(answer, self.user_dataclass)

    @patch("vmngclient.session.Session")
    def test_exists_true(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.users
        # Act
        answer = UsersAPI(mock_session).exists("demo_user")
        # Assert
        self.assertTrue(answer)

    @patch("vmngclient.session.Session")
    def test_exists_false(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.users
        # Act
        answer = UsersAPI(mock_session).exists("no_user")
        # Assert
        self.assertFalse(answer)

    @parameterized.expand([[200, True], [400, False]])
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_create_user(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = [self.users[1]]
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = UsersAPI(mock_session).create_user(self.user_dataclass[0])
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("vmngclient.session.Session")
    def test_create_user_existing(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.users

        # Act
        def answer():
            UsersAPI(mock_session).create_user(self.user_dataclass[0])

        # Assert
        self.assertRaises(UserAlreadyExistsError, answer)

    @parameterized.expand([[200, True], [400, False]])
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_delete_user(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.users
        mock_session.delete.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = UsersAPI(mock_session).delete_user("admin")
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("vmngclient.session.Session")
    def test_delete_user_not_existing(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = [self.users[1]]

        # Act
        def answer():
            UsersAPI(mock_session).delete_user("no_user")

        # Assert
        self.assertRaises(UserDoesNotExists, answer)


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
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_modify_cluster_setup(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = ClusterManagementAPI(mock_session).modify_cluster_setup(self.service_configuration_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("vmngclient.session.Session")
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
            "clientSecret": "secret",
            "orgName": "organization",
            "telemetryEnabled": True,
        }
        self.cloud_connector_data_dataclass = create_dataclass(CloudConnectorData, self.cloud_connector_data)
        self.cloud_services_settings = {"enabled": True}
        self.cloud_services_settings_dataclass = create_dataclass(CloudServicesSettings, self.cloud_services_settings)
        self.cloud_on_ramp = [{"": ""}]

    @patch("vmngclient.session.Session")
    def test_get_sdavc_cloud_connector_config(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = self.cloud_connector_data
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_sdavc_cloud_connector_config()
        # Assert
        self.assertEqual(answer, self.cloud_connector_data_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_enable_sdavc_cloud_connector(self, status_code, expected_outcome, mock_session, mock_response):
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
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_disable_sdavc_cloud_connector(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).disable_sdavc_cloud_connector()
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("vmngclient.session.Session")
    def test_get_cloud_services(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = [self.cloud_services_settings]
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_cloud_services()
        # Assert
        self.assertEqual(answer, self.cloud_services_settings_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_set_cloud_services(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).set_cloud_services(self.cloud_services_settings_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("vmngclient.session.Session")
    def test_get_cloud_on_ramp_for_saas_mode(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.cloud_on_ramp
        # Act
        answer = AdministrationSettingsAPI(mock_session).get_cloud_on_ramp_for_saas_mode()
        # Assert
        self.assertEqual(answer, self.cloud_on_ramp)

    @parameterized.expand([[200, True], [400, False]])
    @patch("vmngclient.session.Session")
    @patch("requests.Response")
    def test_enable_cloud_on_ramp_for_saas_mode(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = AdministrationSettingsAPI(mock_session).enable_cloud_on_ramp_for_saas_mode(True)
        # Assert
        self.assertEqual(answer, expected_outcome)
