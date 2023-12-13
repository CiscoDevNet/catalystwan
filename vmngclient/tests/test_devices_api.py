from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized  # type: ignore
from pytest import mark  # type: ignore
from tenacity import RetryError  # type: ignore

from vmngclient.api.basic_api import DevicesAPI, DeviceStateAPI
from vmngclient.dataclasses import BfdSessionData, Connection, Device, WanInterface
from vmngclient.endpoints.endpoints_container import APIEndpointContainter
from vmngclient.endpoints.monitoring_device_details import DeviceData
from vmngclient.endpoints.real_time_monitoring.reboot_history import RebootEntry
from vmngclient.exceptions import InvalidOperationError
from vmngclient.response import vManageResponse
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.personality import Personality


class ResponseMock:
    def __init__(self, json, headers={}, cookies={}):
        self._json = json
        self.headers = headers
        self.cookies = cookies

    def json(self):
        return self._json


class TestDevicesAPI(TestCase):
    def setUp(self) -> None:
        self.devices = [
            {  # vmanage
                "device-model": "vmanage",
                "deviceId": "1.1.1.1",
                "uuid": "aaaaaaaa-6169-445c-8e49-c0bdaaaaaaa",
                "cpuLoad": 4.71,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.1",
                "board-serial": "11122233",
                "personality": "vmanage",
                "memUsage": 57.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm200",
                "cpuState": "normal",
                "chassis-number": "aaaaaaaa-6aa9-445c-8e49-c0aaaaaaaaa9",
            },
            {  # vsmart
                "device-model": "vsmart",
                "deviceId": "1.1.1.3",
                "uuid": "bbcccccc-6169-445c-8e49-c0bdccccccc",
                "cpuLoad": 2.76,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.3",
                "board-serial": "11223399",
                "personality": "vsmart",
                "memUsage": 28.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm129",
                "cpuState": "normal",
                "chassis-number": "abbbbbbb-6169-445c-8e49-c0bccccccccc",
            },
            {  # vbond
                "device-model": "vedge-cloud",
                "deviceId": "1.1.1.2",
                "uuid": "bbbbbbbb-6169-445c-8e49-c0bdaaaaaaa",
                "cpuLoad": 1.76,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.2",
                "board-serial": "11223344",
                "personality": "vbond",
                "memUsage": 26.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm128",
                "cpuState": "normal",
                "chassis-number": "abbbbbbb-6169-445c-8e49-c0bbbbbbbbb9",
            },
            {  # vedge
                "device-model": "vedge-cloud",
                "deviceId": "169.254.10.10",
                "uuid": "bc2a78ac-a06e-40fd-b2b7-1b1e062f3f9e",
                "cpuLoad": 1.46,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "172.16.254.2",
                "board-serial": "12345708",
                "personality": "vedge",
                "memUsage": 24.1,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm1",
                "cpuState": "normal",
                "chassis-number": "bc2a78ac-a06e-40fd-b2b7-1b1e062f3f9e",
            },
        ]
        self.devices_dataclass = [create_dataclass(Device, device) for device in self.devices]
        self.devices_dataseq = DataSequence(Device, [create_dataclass(Device, device) for device in self.devices])
        self.controllers_dataclass = DataSequence(
            Device, [create_dataclass(Device, device) for device in self.devices[:2]]
        )
        self.orchestrators_dataseq = DataSequence(Device, [create_dataclass(Device, self.devices[2])])
        self.vsmarts_dataseq = DataSequence(Device, [create_dataclass(Device, self.devices[1])])
        self.vbonds_dataseq = DataSequence(Device, [create_dataclass(Device, self.devices[2])])
        self.edges_dataseq = DataSequence(Device, [create_dataclass(Device, self.devices[3])])
        self.system_ips_list = [device["local-system-ip"] for device in self.devices]
        self.ips_list = [device["deviceId"] for device in self.devices]
        self.list_all_devices_resp = DataSequence(DeviceData, [DeviceData.parse_obj(dev) for dev in self.devices])

    @patch.object(DevicesAPI, "get")
    def test_controllers(self, mock_devices):
        # # Arrange
        # MockDevices = Mock()
        # mock_devices.return_value = MockDevices
        # session = Mock()
        # test_object = DevicesAPI(session)
        # test_object.devices = self.devices_dataclass
        # # Act
        # answer = test_object.get().filter(personality=[Personality.VMANAGE, Personality.VSMART])
        # # Assert
        # self.assertEqual(answer, self.controllers_dataclass)
        pass  # TODO fix after updating .filter()

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_orchestrators(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).get().filter(personality=Personality.VBOND)

        # Assert
        self.assertEqual(answer, self.orchestrators_dataseq)

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_edges(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).get().filter(personality=Personality.EDGE)

        # Assert
        self.assertEqual(answer, self.edges_dataseq)

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_vsmarts(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).get().filter(personality=Personality.VSMART)

        # Assert
        self.assertEqual(answer, self.vsmarts_dataseq)

    @patch("vmngclient.session.vManageSession")
    @patch.object(DevicesAPI, "get")
    def test_system_ips(self, mock_devices, mock_session):
        # Arrange
        mock_devices.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).system_ips

        # Assert
        self.assertEqual(answer, self.system_ips_list)

    @patch("vmngclient.session.vManageSession")
    @patch.object(DevicesAPI, "get")
    def test_ips(self, mock_devices, mock_session):
        # Arrange
        mock_devices.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).ips

        # Assert
        self.assertEqual(answer, self.ips_list)

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).get()

        # Assert
        self.assertEqual(answer, self.devices_dataseq)

    @parameterized.expand(
        [
            ["aaaaaaaa-6169-445c-8e49-c0bdaaaaaaa", 0],
            ["bbcccccc-6169-445c-8e49-c0bdccccccc", 1],
            ["bbbbbbbb-6169-445c-8e49-c0bdaaaaaaa", 2],
            ["bc2a78ac-a06e-40fd-b2b7-1b1e062f3f9e", 3],
        ]
    )
    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get_device_details(self, uuid, device_number, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = DataSequence(
            Device, [create_dataclass(Device, self.devices[device_number])]
        )

        # Act
        answer = DevicesAPI(mock_session).get_device_details(uuid=uuid)

        # Assert
        self.assertEqual(answer, create_dataclass(Device, self.devices[device_number]))

    @parameterized.expand(
        [[Personality.EDGE, 1], [Personality.VBOND, 1], [Personality.VMANAGE, 1], [Personality.VSMART, 1]]
    )
    @patch("vmngclient.session.vManageSession")
    @patch.object(DevicesAPI, "get")
    def test_count_devices(self, personality, devices_number, mock_get, mock_session):
        # Arrange
        mock_get.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).count_devices(personality=personality)

        # Assert
        self.assertEqual(answer, devices_number)

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_vsmarts(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = DataSequence(Device, [create_dataclass(Device, self.devices[1])])

        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality=Personality.VSMART)

        # Assert
        self.assertEqual(answer, self.vsmarts_dataseq)

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_vbonds(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = DataSequence(Device, [create_dataclass(Device, self.devices[2])])

        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality=Personality.VBOND)

        # Assert
        self.assertEqual(answer, self.vbonds_dataseq)

    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_vedgess(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = DataSequence(Device, [create_dataclass(Device, self.devices[3])])

        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality=Personality.EDGE)

        # Assert
        self.assertEqual(answer, self.edges_dataseq)

    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_for_vmanage(self, mock_session, personality=Personality.VMANAGE):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]

        # Act
        def answer():
            return DevicesAPI(mock_session).get_reachable_devices(personality)

        # Assert
        self.assertRaises(AssertionError, answer)

    @patch("vmngclient.session.vManageSession")
    def test_send_certificate_state_to_controllers(self, mock_session):
        # Arrange
        mock_session.post().json.return_value = {"id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"}

        # Act
        answer = DevicesAPI(mock_session).send_certificate_state_to_controllers()

        # Assert
        self.assertTrue(answer)

    @patch("vmngclient.session.vManageSession")
    def test_send_certificate_state_to_controllers_error(self, mock_session):
        # Arrange
        mock_session.post().json.return_value = {}

        # Act
        def answer():
            return DevicesAPI(mock_session).send_certificate_state_to_controllers()

        # Assert
        self.assertRaises(InvalidOperationError, answer)

    @parameterized.expand([["vm200", 0], ["vm129", 1], ["vm128", 2], ["vm1", 3]])
    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get_by_hostname(self, hostname, device_number, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).get().filter(hostname=hostname)

        # Assert
        self.assertEqual(answer, DataSequence(Device, [create_dataclass(Device, self.devices[device_number])]))

    @parameterized.expand([["1.1.1.1", 0], ["1.1.1.3", 1], ["1.1.1.2", 2], ["169.254.10.10", 3]])
    @patch("vmngclient.response.vManageResponse")
    @patch("vmngclient.session.vManageSession")
    def test_get_by_id(self, device_id, device_number, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_session.endpoints.monitoring_device_details.list_all_devices.return_value = self.list_all_devices_resp
        mock_response.dataseq.return_value = self.devices_dataseq

        # Act
        answer = DevicesAPI(mock_session).get().filter(id=device_id)

        # Assert
        self.assertEqual(answer, DataSequence(Device, [create_dataclass(Device, self.devices[device_number])]))


class TestDevicesStateAPI(TestCase):
    def setUp(self) -> None:
        self.crash_info = [
            {
                "core-time": "Tue Feb 15 04:14:38 UTC 2022",
                "vdevice-dataKey": "169.254.10.12-0",
                "vdevice-name": "169.254.10.12",
                "index": 0,
                "lastupdated": 1645064726542,
                "core-filename": "vm5_htx_19219_20220215-041430-UTC.core.gz",
                "core-time-date": 1644898478000,
                "vdevice-host-name": "vm5",
            },
            {
                "core-time": "Tue Feb 15 04:15:24 UTC 2022",
                "vdevice-dataKey": "169.254.10.12-1",
                "vdevice-name": "169.254.10.12",
                "index": 1,
                "lastupdated": 1645064726542,
                "core-filename": "vm5_htx_19539_20220215-041515-UTC.core.gz",
                "core-time-date": 1644898524000,
                "vdevice-host-name": "vm5",
            },
        ]
        self.connections_info = [
            {
                "system-ip": "1.1.1.1",
                "peer-type": "vsmart",
                "state": "up",
            },
            {
                "system-ip": "1.1.1.2",
                "peer-type": "vedge",
                "state": "up",
            },
        ]
        self.connections_info_dataclass = [create_dataclass(Connection, item) for item in self.connections_info]
        self.reboot_history = [
            {
                "reboot_date_time-date": 1642651714000,
                "lastupdated": 1642656685355,
                "vdevice-dataKey": "172.16.255.11-2022-01-20T04:08:34+00:00",
                "reboot_date_time": "2022-01-20T04:08:34+00:00",
                "reboot_reason": "Initiated by user - Reboot issued via NETCONF",
                "vdevice-host-name": "vm1",
                "vdevice-name": "172.16.255.11",
            },
            {
                "reboot_date_time-date": 164265171400,
                "lastupdated": 1642656685356,
                "vdevice-dataKey": "172.16.255.11-2022-01-20T04:08:34+00:00",
                "reboot_date_time": "2022-01-20T04:08:34+00:00",
                "reboot_reason": "Initiated by user - Reboot issued via NETCONF",
                "vdevice-host-name": "vm2",
                "vdevice-name": "172.16.255.12",
            },
        ]
        self.reboot_history_payload = DataSequence(
            RebootEntry, [RebootEntry.model_validate(item) for item in self.reboot_history]
        )
        self.device = [
            {  # vmanage
                "device-model": "vmanage",
                "deviceId": "1.1.1.1",
                "uuid": "aaaaaaaa-6169-445c-8e49-c0bdaaaaaaa",
                "cpuLoad": 4.71,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.1",
                "board-serial": "11122233",
                "personality": "vmanage",
                "memUsage": 57.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm200",
                "cpuState": "normal",
                "chassis-number": "aaaaaaaa-6aa9-445c-8e49-c0aaaaaaaaa9",
            }
        ]
        self.device_dataclass = create_dataclass(Device, self.device[0])
        self.wan_interfaces = [
            {
                "color": "default",
                "vdevice-name": "1.1.1.1",
                "admin-state": "up",
                "interface": "eth1",
                "private-port": 12345,
                "vdevice-host-name": "vm1",
                "public-ip": "1.1.1.1",
                "operation-state": "up",
                "public-port": 12345,
                "private-ip": "1.1.1.1",
            },
            {
                "color": "default",
                "vdevice-name": "1.1.1.1",
                "admin-state": "up",
                "interface": "eth1",
                "private-port": 11111,
                "vdevice-host-name": "vm2",
                "public-ip": "1.1.1.1",
                "operation-state": "up",
                "public-port": 11111,
                "private-ip": "1.1.1.1",
            },
        ]
        self.wan_interfaces_dataclass = [create_dataclass(WanInterface, item) for item in self.wan_interfaces]
        self.bfd_session = [
            {
                "src-ip": "1.1.1.1",
                "dst-ip": "1.1.1.2",
                "color": "3g",
                "system-ip": "1.1.1.1",
                "site-id": 1,
                "local-color": "3g",
                "state": "up",
            },
            {
                "src-ip": "1.1.1.1",
                "dst-ip": "1.1.1.3",
                "color": "3g",
                "system-ip": "1.1.1.1",
                "site-id": 1,
                "local-color": "3g",
                "state": "up",
            },
        ]
        self.bfd_session_dataclass = [create_dataclass(BfdSessionData, item) for item in self.bfd_session]
        self.bfd_session_down = [
            {
                "src-ip": "1.1.1.1",
                "dst-ip": "1.1.1.2",
                "color": "3g",
                "system-ip": "1.1.1.1",
                "site-id": 1,
                "local-color": "3g",
                "state": "down",
            }
        ]
        self.device_unreachable = [
            {  # vmanage
                "device-model": "vmanage",
                "deviceId": "1.1.1.1",
                "uuid": "zzzzzzzz-6169-445c-8e49-c0bdaaaaaaa",
                "cpuLoad": 4.71,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.1",
                "board-serial": "11122233",
                "personality": "vmanage",
                "memUsage": 57.0,
                "reachability": "unreachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm200",
                "cpuState": "normal",
                "chassis-number": "aaaaaaaa-6aa9-445c-8e49-c0aaaaaaaaa9",
            }
        ]

    @patch("vmngclient.session.vManageSession")
    def test_get_device_crash_info(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.crash_info
        # Act
        answer = DeviceStateAPI(mock_session).get_device_crash_info(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, self.crash_info)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_crash_info_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = DeviceStateAPI(mock_session).get_device_crash_info(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.vManageSession")
    def test_get_device_control_connections_info(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.connections_info
        # Act
        answer = DeviceStateAPI(mock_session).get_device_control_connections_info(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, self.connections_info_dataclass)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_control_connections_info_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = DeviceStateAPI(mock_session).get_device_control_connections_info(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.vManageSession")
    def test_get_device_orchestrator_connections_info(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.connections_info
        # Act
        answer = DeviceStateAPI(mock_session).get_device_orchestrator_connections_info(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, self.connections_info_dataclass)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_orchestrator_connections_info_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = DeviceStateAPI(mock_session).get_device_orchestrator_connections_info(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.vManageSession")
    def test_get_device_reboot_history(self, mock_session):
        # Arrange
        mock_session.endpoints = APIEndpointContainter(mock_session)
        mock_session.request.return_value = vManageResponse(ResponseMock({"data": self.reboot_history}))
        # Act
        answer = DeviceStateAPI(mock_session).get_device_reboot_history(device_id="1.1.1.11")
        # Assert
        self.assertEqual(answer, self.reboot_history_payload)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_reboot_history_empty(self, mock_session):
        # Arrange
        mock_session.endpoints = APIEndpointContainter(mock_session)
        mock_session.request.return_value = vManageResponse(ResponseMock({"data": []}))
        # Act
        answer = DeviceStateAPI(mock_session).get_device_reboot_history(device_id="1.1.1.1")
        # Assert
        self.assertEqual(len(answer), 0)

    @patch("vmngclient.session.vManageSession")
    def test_get_system_status(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.device
        # Act
        answer = DeviceStateAPI(mock_session).get_system_status(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, self.device_dataclass)

    @patch("vmngclient.session.vManageSession")
    def test_get_system_status_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []

        # Act
        def answer():
            return DeviceStateAPI(mock_session).get_system_status(device_id="1.1.1.1")

        # Assert
        self.assertRaises(AssertionError, answer)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_wan_interfaces(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.wan_interfaces
        # Act
        answer = DeviceStateAPI(mock_session).get_device_wan_interfaces(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, self.wan_interfaces_dataclass)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_wan_interfaces_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = DeviceStateAPI(mock_session).get_device_wan_interfaces(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, [])

    def test_get_colors(self):
        pass  # TODO fix method before test

    def test_enable_data_stream(self):
        pass  # TODO fix method before test

    @patch("vmngclient.session.vManageSession")
    def test_get_bfd_sessions(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.bfd_session
        # Act
        answer = DeviceStateAPI(mock_session).get_bfd_sessions(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, self.bfd_session_dataclass)

    @patch("vmngclient.session.vManageSession")
    def test_get_bfd_sessions_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = DeviceStateAPI(mock_session).get_bfd_sessions(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_bfd_session_up(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.bfd_session
        # Act
        answer = DeviceStateAPI(mock_session).wait_for_bfd_session_up(system_ip="1.1.1.1")
        # Assert
        self.assertIsNone(answer)

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_bfd_session_up_timeout(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.bfd_session_down

        # Act
        def answer():
            return DeviceStateAPI(mock_session).wait_for_bfd_session_up(
                system_ip="1.1.1.1", sleep_seconds=1, timeout_seconds=1
            )

        # Assert
        self.assertRaises(RetryError, answer)

    @mark.skip(reason="10 minutes length")
    @patch("vmngclient.session.vManageSession")
    def test_wait_for_device_state(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.device
        # Act
        answer = DeviceStateAPI(mock_session).wait_for_device_state(device_id="1.1.1.1")
        # Assert
        self.assertTrue(answer)

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_device_state_unreachable(self, mock_session):
        pass  # TODO fix method before test
