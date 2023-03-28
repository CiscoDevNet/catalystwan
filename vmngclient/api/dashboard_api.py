from typing import TYPE_CHECKING

from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.dashboard import CertificatesStatus, Count

if TYPE_CHECKING:
    # from vmngclient.session import vManageSession
    pass


class DashboardAPI:
    """Dashboard API gathers information from vManage dashboard.

    Attributes:
        session (vManageSession): logged in API client session
    """

    def __init__(self, session):
        self.session = session

    def get_vmanages(self) -> DataSequence[Count]:
        """
        Get information about number of vmanages.

        Returns:
            DataSequance of Count dataclass with vManages
        """
        vmanages = self.session.get_data("/dataservice/clusterManagement/health/summary")

        return DataSequence(Count, [create_dataclass(Count, vmanage) for vmanage in vmanages])

    def get_devices(self) -> DataSequence[Count]:
        """
        Get information about number of devices (does not include vManages).

        Returns:
            DataSequance of Count dataclass with devices
        """
        devices = self.session.get_data("/dataservice/network/connectionssummary")

        return DataSequence(Count, [create_dataclass(Count, device) for device in devices])

    def get_certificates_status(self) -> DataSequence[CertificatesStatus]:
        """
        Get information about status of certificates.

        Returns:
            DataSequance of CertificatesStatus dataclass with devices
        """
        devices = self.session.get_data("/dataservice/certificate/stats/summary")

        return DataSequence(CertificatesStatus, [create_dataclass(CertificatesStatus, device) for device in devices])

    def get_control_statuses(self) -> DataSequence[Count]:
        """
        Get information abot control statuses.

        Returns:
            DataSequance of Count dataclass with control statuses
        """
        statuses = self.session.get_data("/dataservice/device/control/count")

        statuses = DataSequence(Count, [create_dataclass(Count, status) for status in statuses])
        for status in statuses:
            status.status_list = DataSequence(Count, [create_dataclass(Count, item) for item in status.status_list])

        return statuses
