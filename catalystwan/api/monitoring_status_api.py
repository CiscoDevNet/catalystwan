# Copyright 2024 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from catalystwan.endpoints.monitoring_status import MonitoringStatus, Status, UpdateStatus
from catalystwan.typed_list import DataSequence

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class MonitoringStatusAPI:
    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self._endpoints = MonitoringStatus(session)

    def __str__(self) -> str:
        return str(self.session)

    def get_statistic_settings(self) -> DataSequence[Status]:
        """Get list of enabled statistics indexes

        Returns:
            DataSequence[EnabledIndex]: DataSequence of EnabledIndex objects
        """
        return self._endpoints.get_statistics_settings()

    def update_statistics_settings(self, payload: List[UpdateStatus]) -> DataSequence[Status]:
        """Update statistics indexes

        Args:
            payload (list[Status]): list of UpdateStatus objects

        Returns:
            DataSequence[Status]: DataSequence of Status objects
        """
        return self._endpoints.update_statistics_settings(payload)

    def get_disabled_devices_by_index(self, index_name: str) -> List[str]:
        """Get list of disabled devices for a statistics index

        Args:
            index_name (str): name of the statistics index

        Returns:
            List[str]: List of disables devices ips
        """
        return self._endpoints.get_disabled_device_list(index_name).root

    def update_disabled_devices_by_index(self, index_name: str, payload: List[str]) -> bool:
        """Update list of disabled devices for a statistics index

        Args:F
            index_name (str): name of the statistics index
            payload (list[str]): list of str objects

        Returns:
            bool: True if successful
        """
        return self._endpoints.update_statistics_device_list(index_name, payload).response

    def get_enabled_index_for_device(self, device_ip: str) -> List[str]:
        """Get list of enabled device for statistics index

        Args:
            device_ip (str): IP address of the device

        Returns:
            List[str]: List of enables indexes
        """
        return self._endpoints.get_enabled_index_for_device(device_ip).root
