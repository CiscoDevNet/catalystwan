import logging
from unittest import TestCase
from unittest.mock import patch

from vmngclient.api.alarms_api import AlarmsAPI, AlarmVerification
from vmngclient.dataclasses import AlarmData
from vmngclient.utils.creation_tools import create_dataclass, flatten_dict


class TestAlarmsAPI(TestCase):
    def setUp(self) -> None:
        self.alarms_data = {
            "data": [
                {
                    "type": "site_up",
                    "component": "OMP",
                    "severity": "Critical",
                    "active": False,
                    "consumed_events": [
                        {
                            "eventname": "omp-peer-state-change",
                            "peer-new-state": "handshake-in-gr",
                            "eventId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                            "builtBy": "EventDataCollector",
                            "component": "OMP",
                            "severity-level": "major ",
                            "vmanage-system-ip": "1.1.1.1",
                            "entry_time": 1671028426000,
                            "system-ip": "1.1.1.1",
                            "host-name": "vm1",
                            "peer": "1.1.1.1",
                        }
                    ],
                    "site_id": "1",
                    "devices": [{"system-ip": "1.1.1.1"}],
                },
                {
                    "type": "site_up",
                    "component": "OMP",
                    "severity": "Major",
                    "active": False,
                    "consumed_events": [
                        {
                            "eventname": "omp-peer-state-change",
                            "peer-new-state": "handshake-in-gr",
                            "eventId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaab",
                            "builtBy": "EventDataCollector",
                            "component": "OMP",
                            "severity-level": "major ",
                            "vmanage-system-ip": "1.1.1.2",
                            "entry_time": 1671028426000,
                            "system-ip": "1.1.1.2",
                            "host-name": "vm2",
                            "peer": "1.1.1.2",
                        }
                    ],
                    "site_id": "2",
                    "devices": [{"system-ip": "1.1.1.2"}],
                },
                {
                    "type": "site_up",
                    "component": "OMP",
                    "severity": "Medium",
                    "active": False,
                    "consumed_events": [
                        {
                            "eventname": "omp-peer-state-change",
                            "peer-new-state": "handshake-in-gr",
                            "eventId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaac",
                            "builtBy": "EventDataCollector",
                            "component": "OMP",
                            "severity-level": "major ",
                            "vmanage-system-ip": "1.1.1.3",
                            "entry_time": 1671028426000,
                            "system-ip": "1.1.1.3",
                            "host-name": "vm3",
                            "peer": "1.1.1.3",
                        }
                    ],
                    "site_id": "3",
                    "devices": [{"system-ip": "1.1.1.3"}],
                },
                {
                    "type": "site_up",
                    "component": "OMP",
                    "severity": "Minor",
                    "active": False,
                    "consumed_events": [
                        {
                            "eventname": "omp-peer-state-change",
                            "peer-new-state": "handshake-in-gr",
                            "eventId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaad",
                            "builtBy": "EventDataCollector",
                            "component": "OMP",
                            "severity-level": "major ",
                            "vmanage-system-ip": "1.1.1.4",
                            "entry_time": 1671028426000,
                            "system-ip": "1.1.1.4",
                            "host-name": "vm4",
                            "peer": "1.1.1.4",
                        }
                    ],
                    "site_id": "4",
                    "devices": [{"system-ip": "1.1.1.4"}],
                },
            ]
        }
        self.alarms = self.alarms_data["data"]
        self.critical_alarms_data = {"data": [self.alarms[0]]}
        self.major_alarms_data = {"data": [self.alarms[1]]}
        self.medium_alarms_data = {"data": [self.alarms[2]]}
        self.minor_alarms_data = {"data": [self.alarms[3]]}
        self.alarms_dataclass = [create_dataclass(AlarmData, flatten_dict(alarm)) for alarm in self.alarms]
        self.critical_alarms_dataclass = [create_dataclass(AlarmData, flatten_dict(self.alarms[0]))]
        self.major_alarms_dataclass = [create_dataclass(AlarmData, flatten_dict(self.alarms[1]))]
        self.medium_alarms_dataclass = [create_dataclass(AlarmData, flatten_dict(self.alarms[2]))]
        self.minor_alarms_dataclass = [create_dataclass(AlarmData, flatten_dict(self.alarms[3]))]
        self.maxDiff = None

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.alarms_data
        # Act
        answer = AlarmsAPI(mock_session).get_alarms()
        # Assert
        self.assertEqual(answer, self.alarms_dataclass)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_critical_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.critical_alarms_data
        # Act
        answer = AlarmsAPI(mock_session).get_critical_alarms()
        # Assert
        self.assertEqual(answer, self.critical_alarms_dataclass)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_major_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.major_alarms_data
        # Act
        answer = AlarmsAPI(mock_session).get_major_alarms()
        # Assert
        self.assertEqual(answer, self.major_alarms_dataclass)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_medium_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.medium_alarms_data
        # Act
        answer = AlarmsAPI(mock_session).get_medium_alarms()
        # Assert
        self.assertEqual(answer, self.medium_alarms_dataclass)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_minor_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.minor_alarms_data
        # Act
        answer = AlarmsAPI(mock_session).get_minor_alarms()
        # Assert
        self.assertEqual(answer, self.minor_alarms_dataclass)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_not_viewed_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.alarms_data
        # Act
        answer = AlarmsAPI(mock_session).get_not_viewed_alarms()
        # Assert
        self.assertEqual(answer, self.alarms_dataclass)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_mark_all_as_viewed(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = {"data": []}
        # Act
        answer = AlarmsAPI(mock_session).mark_all_as_viewed()
        # Assert
        self.assertTrue(answer)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_check_alarms(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.minor_alarms_data
        # Act
        answer = AlarmsAPI(mock_session).check_alarms(self.minor_alarms_data["data"])
        # Assert
        self.assertEqual(answer, {"found": set(self.minor_alarms_dataclass), "not-found": set()})

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_check_alarms_not_found(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.critical_alarms_data
        # Act
        answer = AlarmsAPI(mock_session).check_alarms(self.minor_alarms_data["data"], 2, 1)
        # Assert
        self.assertEqual(answer, {"found": set(), "not-found": set(self.minor_alarms_dataclass)})

    # test AlarmVerification class
    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_verify(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.minor_alarms_data
        alarms_getter = AlarmsAPI(mock_session).get_not_viewed_alarms
        logger = logging.getLogger("test")
        # Act
        answer = AlarmVerification(logger, alarms_getter)
        answer.verify(set(self.minor_alarms_dataclass), 2, 1)
        # Assert
        self.assertEqual(answer.found, set(self.minor_alarms_dataclass))
        self.assertEqual(answer.not_found, set())

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_verify_not_found(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.critical_alarms_data
        alarms_getter = AlarmsAPI(mock_session).get_not_viewed_alarms
        logger = logging.getLogger("test")
        # Act
        answer = AlarmVerification(logger, alarms_getter)
        answer.verify(set(self.minor_alarms_dataclass), 2, 1)
        # Assert
        self.assertEqual(answer.found, set())
        self.assertEqual(answer.not_found, set(self.minor_alarms_dataclass))
