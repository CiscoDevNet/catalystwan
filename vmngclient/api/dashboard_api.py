from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.dashboard import CertificatesStatus, Count

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class DashboardAPI:
    """Dashboard API gathers information from vManage dashboard.

    Attributes:
        session (vManageSession): logged in API client session
    """

    def __init__(self, session: vManageSession):
        self.session = session

    def get_vmanages_count(self) -> DataSequence[Count]:
        """
        Get information about number of vmanages.

        Returns:
            DataSequance of Count dataclass with vManages
        """
        vmanages = self.session.get_data("/dataservice/clusterManagement/health/summary")

        vmanages = DataSequence(Count, [create_dataclass(Count, vmanage) for vmanage in vmanages])
        for vmanage in vmanages:
            vmanage.status_list = DataSequence(Count, [create_dataclass(Count, item) for item in vmanage.status_list])

        return vmanages

    def get_devices_count(self) -> DataSequence[Count]:
        """
        Get information about number of devices (does not include vManages).

        Returns:
            DataSequance of Count dataclass with devices
        """
        devices = self.session.get_data("/dataservice/network/connectionssummary")

        devices = DataSequence(Count, [create_dataclass(Count, device) for device in devices])
        for device in devices:
            device.status_list = DataSequence(Count, [create_dataclass(Count, item) for item in device.status_list])

        return devices

    def get_certificates_status(self) -> DataSequence[CertificatesStatus]:
        """
        Get information about status of certificates.

        Returns:
            DataSequance of CertificatesStatus dataclass with devices
        """
        devices = self.session.get_data("/dataservice/certificate/stats/summary")

        return DataSequence(CertificatesStatus, [create_dataclass(CertificatesStatus, device) for device in devices])

    def get_control_statuses_count(self) -> DataSequence[Count]:
        """
        Get information about control statuses.

        Returns:
            DataSequance of Count dataclass with control statuses
        """
        statuses = self.session.get_data("/dataservice/device/control/count")

        statuses = DataSequence(Count, [create_dataclass(Count, status) for status in statuses])
        for status in statuses:
            status.status_list = DataSequence(Count, [create_dataclass(Count, item) for item in status.status_list])

        return statuses
