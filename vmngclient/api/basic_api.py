"""Methods covering essential API endpoints and related data classes."""
import json
from contextlib import contextmanager
from enum import Enum
from typing import Iterator, List, Union, cast

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from vmngclient.dataclasses import BfdSessionData, Connection, Device, Reboot, WanInterface
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.operation_status import OperationStatus
from vmngclient.utils.personality import Personality
from vmngclient.utils.reachability import Reachability


# TODO link that with dataclass
class DeviceField(Enum):
    HOSTNAME = 'hostname'
    ID = 'id'


class DeviceNotFoundError(Exception):
    pass


class DevicesAPI:
    """API methods of vManage for getting devices and controllers.

    Attributes:
        session: logged in API client session
        devices: List with system status for all devices
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    @property
    def controllers(self) -> List[Device]:
        """List of controller devices only."""
        return [
            controller
            for controller in self.devices
            if controller.personality in [Personality.VMANAGE, Personality.VSMART]
        ]

    @property
    def orchestrators(self) -> List[Device]:
        """List of orchestrator devices only."""
        return [orchestrator for orchestrator in self.devices if Personality.VBOND is orchestrator.personality]

    @property
    def edges(self) -> List[Device]:
        """List of edge devices only."""
        return [edge for edge in self.devices if Personality.EDGE is edge.personality]

    @property
    def vsmarts(self) -> List[Device]:
        """List of vsmart devices only."""
        return [vsmart for vsmart in self.devices if Personality.VSMART is vsmart.personality]

    @property
    def system_ips(self) -> List[str]:
        """List of device system IP addresses."""
        return [device.local_system_ip for device in self.devices]

    @property
    def ips(self):
        """List of device IP addresses."""
        return [device.id for device in self.devices]

    def get_system_ip_based_on_local_system_ip(self, local_system_ip) -> str:
        for dev in self.devices:
            if local_system_ip == dev.local_system_ip:
                return dev.id
        return ''

    @property
    def devices(self) -> List[Device]:
        """List of all devices."""
        devices_basic_info = self.session.get_data('/dataservice/device')

        devices_ids = ""
        for device in devices_basic_info:
            devices_ids += f"&deviceId={device['deviceId']}"

        devices_full_info = self.session.get_data(f'/dataservice/device/system/info?{devices_ids}')

        return [create_dataclass(Device, device) for device in devices_full_info]

    def get_device_details(self, uuid: str) -> Device:
        """Gets system information for a device.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            Device object
        """
        devices = self.session.get_data(f'/dataservice/system/device/vedges?uuid={uuid}')

        assert len(devices) == 1, 'Expected system info response list to have one member'

        return create_dataclass(Device, devices[0])

    def count_devices(self, personality: Personality) -> int:
        """Gets number of devices of given personality.

        Args:
            personality: personality of the device

        Returns:
            count of devices
        """
        return sum([1 for device in self.devices if device.personality == personality.value])

    def get_tenants(self) -> Union[list, dict]:
        """Gets Tenants.

        Returns:
            Tenants
        """
        tenants = self.session.get_data('/dataservice/tenant')

        return tenants

    def get_reachable_devices(self, personality: Personality):
        """Get reachable devices by personality.

        Args:
            personality: personality of the device

        Returns:
            reachable devices
        """
        unsupported_personality = [Personality.VMANAGE]
        assert personality not in unsupported_personality, 'Unsupported personality for reachable endpoint'
        return self.session.get_data(f'/dataservice/device/reachable?personality={personality.value}')

    def send_certificate_state_to_controllers(
        self,
        sleep_seconds: int = 5,
        timeout_seconds: int = 600,
    ) -> bool:
        """Sending the current status of certificates to the controllers

        Returns:
            bool: True if all ok, False like something wrong
        """

        def _log_exception(retry_state):
            self.session.__get_logger(f"Orignial exception: {retry_state.outcome.exception()}.")

        def check_state(action_data):
            list_action = [action['status'] == OperationStatus.SUCCESS.value for action in action_data]
            return not all(list_action)

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_state),
            retry_error_callback=_log_exception,
        )
        def wait_for_state():
            status_api = f'/dataservice/device/action/status/{action_id}'
            return self.session.get_data(f'{status_api}')

        response = cast(dict, self.session.post_json('/dataservice/certificate/vedge/list?action=push'))
        if response.get('id'):
            action_id = response['id']
        else:
            raise FailedSend('Failed to push edges list certificates')

        return True if wait_for_state() else False

    def get(self, field: DeviceField, value: str) -> Device:
        supported_fields = [
            DeviceField.HOSTNAME,
            DeviceField.ID,
        ]

        if field not in supported_fields:
            raise TypeError(f"{field} is not supported. Available fields: {supported_fields}")

        for device in self.devices:
            if getattr(device, field.value) == value:
                return device
        raise DeviceNotFoundError(f"Device with `{field.value}` equals to `{value}` does not exists.")


class DeviceStateAPI:
    """Basic API methods of vManage.

    Attributes:
        session: logged in API client session
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def get_device_crash_info(self, device_id: str) -> Union[list, dict]:
        """Gets crash info for a device.

        Args:
             device_id: device ID (usually system-ip)

        Returns:
            Union[list, dict]: list of dicts (FIXME: add mapping to a NamedTuples)
        """
        return self.session.get_data(f'/dataservice/device/crashlog?deviceId={device_id}')

    def get_device_control_connections_info(self, device_id) -> List[Connection]:
        """Gets control connections for a device.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            list of Connection objects
        """
        items = self.session.get_data(f'/dataservice/device/control/connections?deviceId={device_id}')

        return [create_dataclass(Connection, item) for item in items]

    def get_device_orchestrator_connections_info(self, device_id) -> List[Connection]:
        """Gets orchestrator connections for a device

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            list of Connection objects
        """
        items = self.session.get_data(f'/dataservice/device/orchestrator/connections?deviceId={device_id}')

        return [create_dataclass(Connection, item) for item in items]

    def get_device_reboot_history(self, device_id):
        """Gets device reboots list.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            list of Reboot objects
        """
        items = self.session.get_data(f'/dataservice/device/reboothistory?deviceId={device_id}')

        return [create_dataclass(Reboot, item) for item in items]

    def get_system_status(self, device_id: str) -> Device:
        """Get system information for a device.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
           Device object
        """
        devices = self.session.get_data(f'/dataservice/device/system/info?deviceId={device_id}')

        assert len(devices) == 1, 'Expected system info response list to have one member'

        return create_dataclass(Device, devices[0])

    def get_device_wan_interfaces(self, device_id: str):
        wan_interfaces = self.session.get_data(f'/dataservice/device/control/waninterface?deviceId={device_id}')
        return [create_dataclass(WanInterface, wan_ifc) for wan_ifc in wan_interfaces]

    def get_colors(self, device_id: str) -> List[str]:
        url = '/dataservice/device/bfd/state/device/tlocInterfaceMap'
        colors_raw = DevicesAPI(self.session).session.get(url + f'?deviceId={device_id}')
        json_colors = json.loads(str(colors_raw.read(), 'utf-8'))
        colors = list(json_colors["intfList"].keys())

        return colors

    @contextmanager
    def enable_data_stream(self) -> Iterator:
        try:
            url_path = "/dataservice/settings/configuration/vmanagedatastream"
            data_stream_status = self.session.get_data(url_path)[0]
            query = {
                "enable": True,
                "ipType": "systemIp",
                "serverHostName": "systemIp",
                "vpn": 0,
            }
            url_path = "/dataservice/settings/configuration/vmanagedatastream"
            self.session.post_data(url_path, query)
            yield None
        finally:
            url_path = "/dataservice/settings/configuration/vmanagedatastream"
            self.session.post_data(url_path, data_stream_status)

    def get_bfd_sessions(self, device_id: str) -> List[BfdSessionData]:
        items = self.session.get_data(f'/dataservice/device/bfd/sessions?deviceId={device_id}')

        return [create_dataclass(BfdSessionData, item) for item in items]

    def wait_for_bfd_session_up(
        self, system_ip: str, sleep_seconds: int = 5, timeout_seconds: int = 60, exp_state: str = 'up'
    ):
        def check_state(bfd_sessions):
            return not all([bfd_session.state == exp_state for bfd_session in bfd_sessions])

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_state),
        )
        def wait_for_bfd_session_come_up():
            return self.get_bfd_sessions(system_ip)
            # from my observation it is necessary to wait minimum 5 seconds for BFD's session gets up state

        wait_for_bfd_session_come_up()

    def wait_for_device_state(
        self,
        device_id: str,
        sleep_seconds: int = 5,
        timeout_seconds: int = 600,
        exp_state: Reachability = Reachability.REACHABLE,
    ):
        """
        Waiting for the state of the machine.

        Args:
          device_id(Str): Device ID (usually system-ip)
          timeout_seconds(int): Failure timeout.
          sleep_seconds(int): Sleep time.
          exp_state(Reachability): The expected state of the machine

        Returns:
          True if the expected state has been achieved

        """

        def _log_exception(retry_state):
            self.session.__get_logger(f"Orignial exception: {retry_state.outcome.exception()}.")

        def check_state(state):
            return state == exp_state.value

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_state),
            retry_error_callback=_log_exception,
        )
        def wait_for_state():
            return self.get_system_status(device_id).reachability

        return True if wait_for_state() else False


class FailedSend(Exception):
    """Used when a referenced item is not found"""

    pass


__all__ = ['Device']
