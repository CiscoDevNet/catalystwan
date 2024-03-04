# Copyright 2022 Cisco Systems, Inc. and its affiliates

"""Methods covering essential API endpoints and related data classes."""
from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Iterator, List, Union

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from catalystwan.dataclasses import BfdSessionData, Connection, Device, WanInterface
from catalystwan.endpoints.real_time_monitoring.reboot_history import RebootEntry
from catalystwan.exceptions import CatalystwanException
from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import create_dataclass
from catalystwan.utils.operation_status import OperationStatus
from catalystwan.utils.personality import Personality
from catalystwan.utils.reachability import Reachability

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


logger = logging.getLogger(__name__)


class DevicesAPI:
    """API methods of vManage for getting devices and controllers.

    Attributes:
        session: logged in API client session
    """

    max_params = 1000

    def __init__(self, session: ManagerSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    @property
    def system_ips(self) -> List[str]:
        """List of device system IP addresses."""
        return [device.local_system_ip for device in self.get()]

    @property
    def ips(self):
        """List of device IP addresses."""
        return [device.id for device in self.get()]

    def get_system_ip_based_on_local_system_ip(self, local_system_ip) -> str:
        for dev in self.get():
            if local_system_ip == dev.local_system_ip:
                return dev.id
        return ""

    def get_device_details(self, uuid: str) -> Device:
        """Gets system information for a device.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            Device object
        """
        response = self.session.get(f"/dataservice/system/device/vedges?uuid={uuid}")

        devices = response.dataseq(Device)
        assert len(devices) == 1, "Expected system info response list to have one member"

        return devices[0]

    def count_devices(self, personality: Personality) -> int:
        """Gets number of devices of given personality.

        Args:
            personality: personality of the device

        Returns:
            count of devices
        """
        return sum([1 for device in self.get() if device.personality == personality])

    def get_reachable_devices(self, personality: Personality) -> DataSequence[Device]:
        """Get reachable devices by personality.

        Args:
            personality: personality of the device

        Returns:
            reachable devices
        """
        unsupported_personality = [Personality.VMANAGE]
        assert personality not in unsupported_personality, "Unsupported personality for reachable endpoint"

        devices = self.session.get(f"/dataservice/device/reachable?personality={personality.value}")
        return devices.dataseq(Device)

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
            list_action = [action["status"] == OperationStatus.SUCCESS.value for action in action_data]
            return not all(list_action)

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_state),
            retry_error_callback=_log_exception,
        )
        def wait_for_state():
            status_api = f"/dataservice/device/action/status/{action_id}"
            return self.session.get_data(f"{status_api}")

        response = self.session.post("/dataservice/certificate/vedge/list?action=push").json()
        if response.get("id"):
            action_id = response["id"]
        else:
            raise CatalystwanException("Failed to push edges list certificates")

        return True if wait_for_state() else False

    def get(self, rediscover: bool = False) -> DataSequence[Device]:
        """Data sequence of all devices.

        Args:
            rediscover: Rediscover device request payload

        Returns:
            DataSequence[Device] of all devices

        ## Examples:

        Get all vManages:
        >>> devices = DevicesAPI(session).get()
        >>> vManages = devices.filter(personality=Personality.VMANAGE)
        """
        if rediscover:
            logger.info("Rediscovering devices...")
            api = "/dataservice/device/action/rediscoverall"
            self.session.post(url=api)
        devices = self.session.endpoints.monitoring_device_details.list_all_devices()
        device_ids = [device.device_id for device in devices]
        devices_sys_info = DataSequence(Device, [])
        for i in range(0, len(device_ids), self.max_params):
            params = {"deviceId": device_ids[i : i + self.max_params]}
            resp = self.session.get(url="/dataservice/device/system/info", params=params)
            devices_sys_info += resp.dataseq(Device)

        return devices_sys_info


class DeviceStateAPI:
    """Basic API methods of vManage.

    Attributes:
        session: logged in API client session
    """

    def __init__(self, session: ManagerSession) -> None:
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
        return self.session.get_data(f"/dataservice/device/crashlog?deviceId={device_id}")

    def get_device_control_connections_info(self, device_id) -> List[Connection]:
        """Gets control connections for a device.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            list of Connection objects
        """
        items = self.session.get_data(f"/dataservice/device/control/connections?deviceId={device_id}")

        return [create_dataclass(Connection, item) for item in items]

    def get_device_orchestrator_connections_info(self, device_id) -> List[Connection]:
        """Gets orchestrator connections for a device

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            list of Connection objects
        """
        items = self.session.get_data(f"/dataservice/device/orchestrator/connections?deviceId={device_id}")

        return [create_dataclass(Connection, item) for item in items]

    def get_device_reboot_history(self, device_id) -> DataSequence[RebootEntry]:
        """Gets device reboots list.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
            list of Reboot objects
        """
        params = {"deviceId": device_id}
        return self.session.endpoints.real_time_monitoring.reboot_history.create_reboot_history_list(params)

    def get_system_status(self, device_id: str) -> Device:
        """Get system information for a device.

        Args:
            device_id: device ID (usually system-ip)

        Returns:
           Device object
        """
        devices = self.session.get_data(f"/dataservice/device/system/info?deviceId={device_id}")

        assert len(devices) == 1, "Expected system info response list to have one member"

        return create_dataclass(Device, devices[0])

    def get_device_wan_interfaces(self, device_id: str):
        wan_interfaces = self.session.get_data(f"/dataservice/device/control/waninterface?deviceId={device_id}")
        return [create_dataclass(WanInterface, wan_ifc) for wan_ifc in wan_interfaces]

    def get_colors(self, device_id: str) -> List[str]:
        url = "/dataservice/device/bfd/state/device/tlocInterfaceMap"
        colors_raw = DevicesAPI(self.session).session.get_json(url + f"?deviceId={device_id}")
        colors = list(colors_raw["intfList"].keys())

        return colors

    @contextmanager
    def enable_data_stream(self) -> Iterator:  # TODO check
        try:
            url_path = "/dataservice/settings/configuration/vmanagedatastream"
            data_stream_status = self.session.get_data(url_path)[0]
            query = {  # TODO Dict[str, obj]
                "enable": True,
                "ipType": "systemIp",
                "serverHostName": "systemIp",
                "vpn": "0",
            }
            url_path = "/dataservice/settings/configuration/vmanagedatastream"
            self.session.post(url=url_path, json=query)
            yield None
        finally:
            url_path = "/dataservice/settings/configuration/vmanagedatastream"
            self.session.post(url=url_path, json=data_stream_status)

    def get_bfd_sessions(self, device_id: str) -> List[BfdSessionData]:
        items = self.session.get_data(f"/dataservice/device/bfd/sessions?deviceId={device_id}")

        return [create_dataclass(BfdSessionData, item) for item in items]

    def wait_for_bfd_session_up(
        self,
        system_ip: str,
        sleep_seconds: int = 5,
        timeout_seconds: int = 60,
        exp_state: str = "up",
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


__all__ = ["Device"]
