from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from vmngclient.endpoints.monitoring_status import DisabledDevice, EnabledIndex, MonitoringStatus, Status, UpdateStatus
from vmngclient.typed_list import DataSequence

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


def status_ok(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        return True if response.status_code in [200, 204] else False

    return wrapper


class MonitoringStatusAPI:
    URL_DEVICE = "/dataservice/statistics/settings/status/device"
    URL_DISABLED_DEVICES = "/dataservice/statistics/settings/disable/devicelist"

    def __init__(self, session: vManageSession) -> None:
        self.session = session
        self.endpoint = MonitoringStatus(session)

    def __str__(self) -> str:
        return str(self.session)

    def get_statistic_settings(self) -> DataSequence[Status]:
        """Get list of enabled statistics indexes

        Returns:
            DataSequence[EnabledIndex]: DataSequence of EnabledIndex objects
        """
        return self.endpoint.get_statistics_settings()

    def update_statistics_settings(self, payload: List[UpdateStatus]) -> DataSequence[Status]:
        """Update statistics indexes

        Args:
            payload (list[Status]): list of UpdateStatus objects

        Returns:
            DataSequence[Status]: DataSequence of Status objects
        """
        return self.endpoint.update_statistics_settings(payload)

    def get_disabled_devices_by_index(self, index_name: str):
        """Get list of disabled devices for a statistics index

        Args:
            index_name (str): name of the statistics index

        Returns:
            DataSequence[EnabledIndex]: DataSequence of EnabledIndex objects
        """
        url_path = f"{MonitoringStatusAPI.URL_DISABLED_DEVICES}/{index_name}"
        items = self.session.get_json(url_path)
        return DataSequence.from_flatlist(DisabledDevice, "ip_address", items)

    @status_ok
    def update_disabled_devices_by_index(self, index_name: str, payload: List[str]):
        """Update list of disabled devices for a statistics index

        Args:
            index_name (str): name of the statistics index
            payload (list[str]): list of str objects

        Returns:
            DataSequence[EnabledIndex]: DataSequence of EnabledIndex objects
        """
        url_path = f"{MonitoringStatusAPI.URL_DISABLED_DEVICES}/{index_name}"
        parameters = {"indexName": index_name}
        return self.session.put(url=url_path, params=parameters, json=payload)

    def get_enabled_index_for_device(self, device_ip: str) -> DataSequence[EnabledIndex]:
        """Get list of enabled device for statistics index

        Args:
            device_ip (str): IP address of the device

        Returns:
            DataSequence[EnabledIndex]: DataSequence of EnabledIndex objects
        """
        items = self.session.get_json(url=f"{MonitoringStatusAPI.URL_DEVICE}?deviceId={device_ip}")
        return DataSequence.from_flatlist(EnabledIndex, "indexName", items)
