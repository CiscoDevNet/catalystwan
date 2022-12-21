from unittest import TestCase
from unittest.mock import Mock, patch

from parameterized import parameterized  # type: ignore
from tenacity import RetryError  # type: ignore

from vmngclient.api.basic_api import DeviceField, DevicesAPI, DeviceStateAPI, FailedSend
from vmngclient.dataclasses import BfdSessionData, Connection, Device, Reboot, WanInterface
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.personality import Personality


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
        self.controllers_dataclass = [create_dataclass(Device, device) for device in self.devices[:2]]
        self.orchestrators_dataclass = [create_dataclass(Device, self.devices[2])]
        self.edges_dataclass = [create_dataclass(Device, self.devices[3])]
        self.vsmarts_dataclass = [create_dataclass(Device, self.devices[1])]
        self.system_ips_list = [device["local-system-ip"] for device in self.devices]
        self.ips_list = [device["deviceId"] for device in self.devices]
        self.tenants = [
            {
                "flakeId": 11111,
                "orgName": "my-org Inc",
                "samlSpInfo": "",
                "subDomain": "sub1.domain.com",
                "vBondAddress": "1.1.1.1",
                "oldIdpMetadata": "",
                "configDBClusterServiceName": "",
                "vSmarts": [
                    "aaaaaaaa-aaac-42f4-b2c7-1aaaaaaaaaaaa",
                    "bbbbbbbb-9d8a-453c-841f-4bbbbbbbbbbb",
                ],
                "mode": "off",
                "idpMetadata": "",
                "createdAt": 1111111111111,
                "@rid": 1111,
                "tenantId": "aaaaaaaaaa-9ca8-42fd-8290-67aaaaaaaaaa",
                "name": "sub1",
                "wanEdgeForecast": "100",
                "spMetadata": "",
                "state": "READY",
                "wanEdgePresent": 1,
                "desc": "This is sub1",
            },
            {
                "flakeId": 22222,
                "orgName": "my-org Inc",
                "samlSpInfo": "",
                "subDomain": "sub2.domain.com",
                "vBondAddress": "1.1.1.2",
                "oldIdpMetadata": "",
                "configDBClusterServiceName": "",
                "vSmarts": [
                    "ccccccccccccccc-42f4-b2c7-1cccccccccc",
                    "ddddddddd-9d8a-453c-841f-4dddddddddd",
                ],
                "mode": "off",
                "idpMetadata": "",
                "createdAt": 2222222222222,
                "@rid": 2222,
                "tenantId": "ccccccccca-9ca8-42fd-8290-67aaaccccccc",
                "name": "sub2",
                "wanEdgeForecast": "100",
                "spMetadata": "",
                "state": "READY",
                "wanEdgePresent": 1,
                "desc": "This is sub2",
            },
        ]
        self.devices_vbonds = [self.devices[2]]
        self.devices_vsmatrs = [self.devices[1]]
        self.devices_edges = [self.devices[3]]

    @patch.object(DevicesAPI, "devices")
    def test_controllers(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.controllers
        # Assert
        self.assertEqual(answer, self.controllers_dataclass)

    @patch.object(DevicesAPI, "devices")
    def test_orchestrators(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.orchestrators
        # Assert
        self.assertEqual(answer, self.orchestrators_dataclass)

    @patch.object(DevicesAPI, "devices")
    def test_edges(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.edges
        # Assert
        self.assertEqual(answer, self.edges_dataclass)

    @patch.object(DevicesAPI, "devices")
    def test_vsmarts(self, mock_vsmarts):
        # Arrange
        MockDevices = Mock()
        mock_vsmarts.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.vsmarts
        # Assert
        self.assertEqual(answer, self.vsmarts_dataclass)

    @patch.object(DevicesAPI, "devices")
    def test_system_ips(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.system_ips
        # Assert
        self.assertEqual(answer, self.system_ips_list)

    @patch.object(DevicesAPI, "devices")
    def test_ips(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.ips
        # Assert
        self.assertEqual(answer, self.ips_list)

    @patch("vmngclient.session.vManageSession")
    def test_devices(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.devices
        # Act
        answer = DevicesAPI(mock_session).devices
        # Assert
        self.assertEqual(answer, self.devices_dataclass)

    def test_get_device_details(self):
        pass  # TODO fix method before test

    def test_count_devices(self):
        pass  # TODO fix method before test

    @patch("vmngclient.session.vManageSession")
    def test_get_tenants(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.tenants
        # Act
        answer = DevicesAPI(mock_session).get_tenants()
        # Assert
        self.assertEqual(answer, self.tenants)

    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_for_vsmatrs(self, mock_session, personality=Personality.VSMART):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]
        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality)
        # Assert
        self.assertEqual(answer, self.devices_vsmatrs)

    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_for_vbonds(self, mock_session, personality=Personality.VBOND):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]
        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality)
        # Assert
        self.assertEqual(answer, self.devices_vbonds)

    @patch("vmngclient.session.vManageSession")
    def test_get_reachable_devices_for_edges(self, mock_session, personality=Personality.EDGE):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]
        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality)
        # Assert
        self.assertEqual(answer, self.devices_edges)

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
        self.assertRaises(FailedSend, answer)

    @parameterized.expand([["vm200", 0], ["vm129", 1], ["vm128", 2], ["vm1", 3]])
    @patch.object(DevicesAPI, "devices")
    def test_get_by_hostname(self, hostname, device_number, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.get(DeviceField.HOSTNAME, hostname)
        # Assert
        self.assertEqual(answer, self.devices_dataclass[device_number])

    @parameterized.expand([["1.1.1.1", 0], ["1.1.1.3", 1], ["1.1.1.2", 2], ["169.254.10.10", 3]])
    @patch.object(DevicesAPI, "devices")
    def test_get_by_id(self, device_id, device_number, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.get(DeviceField.ID, device_id)
        # Assert
        self.assertEqual(answer, self.devices_dataclass[device_number])


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
        self.reboot_history_dataclass = [create_dataclass(Reboot, item) for item in self.reboot_history]
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
        mock_session.get_data.return_value = self.reboot_history
        # Act
        answer = DeviceStateAPI(mock_session).get_device_reboot_history(device_id="1.1.1.11")
        # Assert
        self.assertEqual(answer, self.reboot_history_dataclass)

    @patch("vmngclient.session.vManageSession")
    def test_get_device_reboot_history_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = DeviceStateAPI(mock_session).get_device_reboot_history(device_id="1.1.1.1")
        # Assert
        self.assertEqual(answer, [])

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
