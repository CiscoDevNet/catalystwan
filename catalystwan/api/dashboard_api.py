# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import create_dataclass
from catalystwan.utils.dashboard import (
    CertificatesStatus,
    Count,
    DeviceHealth,
    DeviceHealthOverview,
    DevicesHealth,
    LicensedDevices,
    TenantStatus,
    TransportHealth,
    TunnelHealth,
)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class DashboardAPI:
    """Dashboard API gathers information from vManage dashboard.

    Attributes:
        session (ManagerSession): logged in API client session

    Usage example:
        # Create session
        session = create_manager_session(...)
        # Get information about tenant status
        tenant_status = session.api.dashboard.get_tenant_status()
    """

    def __init__(self, session: ManagerSession):
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

    def get_bfd_connectivity_count(self) -> DataSequence[Count]:
        """
        Get information about bfd connectivity count.

        Returns:
            DataSequance of Count dataclass with bfd connectivity
        """
        response = self.session.get("/dataservice/device/bfd/sites/summary")

        bfd_response = response.dataseq(Count)
        for item in bfd_response:
            item.status_list = DataSequence(
                Count, [create_dataclass(Count, bfd_connection) for bfd_connection in item.status_list]  # type:ignore
            )

        return bfd_response

    def get_edges_inventory_count(self) -> DataSequence[Count]:
        """
        Get information about edges inventory.

        Returns:
            DataSequance of Count dataclass with edges inventory count
        """
        response = self.session.get("/dataservice/device/vedgeinventory/summary")

        edges_inventory = response.dataseq(Count)

        return edges_inventory

    def get_transport_interface_distribution(self) -> DataSequence[Count]:
        """
        Get information about transport interface distribution.

        Returns:
            DataSequance of Count dataclass with transport interface distribution
        """
        response = self.session.get("/dataservice/device/tlocutil")

        transport_interface = response.dataseq(Count)

        return transport_interface

    def get_tenant_status(self) -> DataSequence[TenantStatus]:
        """
        Get information about tenant status, including:
        - control status
        - site health
        - vEdge health
        - vSmart status

        Returns:
            DataSequance of TenantStatus dataclass with tenant status information
        """
        response = self.session.get("/dataservice/tenantstatus")

        transport_interface = response.dataseq(TenantStatus)

        return transport_interface

    def get_devices_health(self) -> DevicesHealth:
        """
        Get information about devices health

        Returns:
            DevicesHealth object
        """
        response = self.session.get_json("/dataservice/health/devices")
        devices_health = create_dataclass(DevicesHealth, response)

        devices_health.devices = DataSequence(
            DeviceHealth, [create_dataclass(DeviceHealth, device) for device in devices_health.devices]  # type: ignore
        )

        return devices_health

    def get_licensed_devices(self) -> DataSequence[LicensedDevices]:
        """
        Get information about licensed devices.

        Returns:
            DataSequance of LicensedDevices dataclass with licences information.
        """
        response = self.session.get("/dataservice/msla/monitoring/licensedDeviceCount")

        return response.dataseq(LicensedDevices)

    def get_devices_health_overview(self) -> DataSequence[DeviceHealthOverview]:
        """
        Get information about health overview devices.

        Returns:
            DataSequance of DeviceHealthOverview dataclass with health information.
        """
        response = self.session.get_json("/dataservice/health/devices/overview")

        return DataSequence(DeviceHealthOverview, [create_dataclass(DeviceHealthOverview, response)])

    def get_transport_health(self) -> DataSequence[TransportHealth]:
        """
        Get information about loss percentage, latency and jitter for all links and combinations of colors.

        Returns:
            DataSequance of TransportHealth dataclass with loss percentage, latency and jitter information.
        """
        response = self.session.get("/dataservice/statistics/approute/transport/summary/loss_percentage")

        return response.dataseq(TransportHealth)

    def get_tunnel_health(self) -> DataSequence[TunnelHealth]:
        """
        Get information about state, loss percentage, latency and jitter for tunnels.

        Returns:
            DataSequance of TunnelHealth dataclass with tunnel health information.
        """
        response = self.session.get("/dataservice/statistics/approute/tunnels/health/latency")

        return response.dataseq(TunnelHealth)
