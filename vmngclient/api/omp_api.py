from typing import List

from vmngclient.dataclasses import (
    OmpAdvertisedRouteData,
    OmpAdvertisedTlocData,
    OmpPeerData,
    OmpReceivedRouteData,
    OmpReceivedTlocData,
    OmpServiceData,
    OmpSummaryData,
)
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass


class OmpAPI:
    """OMP API methods of vManage for get common omp data.

    Attributes:
        session (vManageSession): logged in API client session
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def get_omp_peers(self, device_id: str) -> List[OmpPeerData]:
        """Gets OMP peers for a device.

        Args:
            device_id (str): device ID (usually system-ip)

        Returns:
            List[OmpPeerData]: OmpPeerData object
        """
        items = self.session.get_data(f"/dataservice/device/omp/peers?deviceId={device_id}")
        return [create_dataclass(OmpPeerData, item) for item in items]

    def get_advertised_routes(self, device_id: str) -> List[OmpAdvertisedRouteData]:
        """Gets OMP advertised routes data for a device.

        Args:
            device_id (str): device ID (usually system-ip)

        Returns:
            List[OmpAdvertisedRouteData]: OmpAdvertisedRouteData objects
        """
        items = self.session.get_data(f"/dataservice/device/omp/routes/advertised?deviceId={device_id}")
        return [create_dataclass(OmpAdvertisedRouteData, item) for item in items]

    def get_received_routes(self, device_id: str) -> List[OmpReceivedRouteData]:
        """Gets OMP received routes data for a device.

        Args:
            device_id (str): device ID (usually system-ip)

        Returns:
            List[OmpReceivedRouteData]: OmpReceivedRouteData objects
        """
        items = self.session.get_data(f"/dataservice/device/omp/routes/received?deviceId={device_id}")
        return [create_dataclass(OmpReceivedRouteData, item) for item in items]

    def get_advertised_tlocs(self, device_id: str) -> List[OmpAdvertisedTlocData]:
        """Gets OMP advertised TLOCs data for a device.

        Args:
            device_id (str): device_id: device ID (usually system-ip)

        Returns:
            List[OmpAdvertisedTlocData]: OmpAdvertisedTlocData objects
        """
        items = self.session.get_data(f"/dataservice/device/omp/tlocs/advertised?deviceId={device_id}")
        return [create_dataclass(OmpAdvertisedTlocData, item) for item in items]

    def get_received_tlocs(self, device_id: str) -> List[OmpReceivedTlocData]:
        """Gets OMP received TLOCs for a device.

        Args:
            device_id (str): device ID (usually system-ip)

        Returns:
            List[OmpReceivedTlocData]: OmpReceivedTlocData objects
        """
        items = self.session.get_data(f"/dataservice/device/omp/tlocs/received?deviceId={device_id}")
        return [create_dataclass(OmpReceivedTlocData, item) for item in items]

    def get_services(self, device_id: str) -> List[OmpServiceData]:
        """Gets OMP services data for a device.

        Args:
            device_id (str): device ID (usually system-ip)

        Returns:
            List[OmpServiceData]: OmpServiceData objects
        """
        items = self.session.get_data(f"/dataservice/device/omp/services?deviceId={device_id}")
        return [create_dataclass(OmpServiceData, item) for item in items]

    def get_omp_summary(self, device_id: str) -> List[OmpSummaryData]:
        """Gets OMP summaries data for a device.

        Args:
            device_id (str): device ID (usually system-ip)

        Returns:
            List[OmpSummaryData]: OmpSummaryData objects
        """
        items = self.session.get_data(f"/dataservice/device/omp/summary?deviceId={device_id}")
        return [create_dataclass(OmpSummaryData, item) for item in items]
