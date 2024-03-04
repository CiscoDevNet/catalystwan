# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from attr import define, field  # type: ignore

from catalystwan.dataclasses import DataclassBase
from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import FIELD_NAME, create_dataclass
from catalystwan.utils.personality import Personality
from catalystwan.utils.reachability import Reachability


class DeviceName(Enum):
    VMANAGE: str = "vManage"
    VBOND: str = "vBond"
    VSMART: str = "vSmart"
    EDGE: str = "WAN Edge"
    VEDGE: str = "vEdge"


class StatusName(Enum):
    CONTROL_STATUS: str = "Control Status"
    CONTROL_UP: str = "Control up"
    PARTIAL_CONTROL: str = "Partial"
    CONTROL_DOWN: str = "Control down"


class BfdConnectivityName(Enum):
    FULL: str = "Full WAN Connectivity"
    PARTIAL: str = "Partial WAN Connectivity"
    NO_CONNECTIVITY: str = "No WAN Connectivity"


class InventoryName(Enum):
    TOTAL: str = "Total"
    AUTHORIZED: str = "Authorized"
    DEPLOYED: str = "Deployed"
    STAGING: str = "Staging"


class PercentageDistributionName(Enum):
    BELOW_10_MBPS: str = "less_than_10_mbps"
    BETWEEN_10_AND_100_MBPS: str = "10_mbps_100_mbps"
    BETWEEN_100_AND_500_MBPS: str = "100_mbps_500_mbps"
    ABOVE_500_MBPS: str = "greater_than_500_mbps"


class PercentageDistribution(Enum):
    BELOW_10_MBPS: str = "< 10 Mbps"
    BETWEEN_10_AND_100_MBPS: str = "10 Mbps - 100 Mbps"
    BETWEEN_100_AND_500_MBPS: str = "100 Mbps - 500 Mbps"
    ABOVE_500_MBPS: str = "> 500 Mbps"


class HealthColor(Enum):
    GREEN: str = "green"
    YELLOW: str = "yellow"
    RED: str = "red"


def name_converter(name):
    if name is None:
        return None
    for enum_type in (StatusName, DeviceName, BfdConnectivityName, InventoryName, PercentageDistributionName):
        try:
            return enum_type(name)
        except ValueError:
            pass

    raise ValueError(f"'{name}' is not a valid name.")


@define
class Count(DataclassBase):
    """Dataclass used to handle endpoints that return count of something

    Example:
        Endpoint '/dataservice/clusterManagement/health/summary' returns count of vmanages, which
            contains details_url, name, count, status and status_list
    """

    details_url: str = field(metadata={FIELD_NAME: "detailsURL"})
    count: Optional[int] = field(default=None)
    status: Optional[str] = field(default=None)
    name: Optional[
        Union[DeviceName, StatusName, BfdConnectivityName, InventoryName, PercentageDistributionName]
    ] = field(default=None, converter=name_converter)
    message: Optional[str] = field(default=None)
    status_list: Optional[DataSequence[Count]] = field(default=None, metadata={FIELD_NAME: "statusList"})
    list: Optional[str] = field(default=None)
    value: Optional[int] = field(default=None)
    percentageDistribution: Optional[PercentageDistribution] = field(default=None)

    @value.validator  # type: ignore
    def value_or_count_provided(self, attribute, value):
        """Count dataclass requires count or value attribute in order to show the number of thing it is displaying"""
        if value is None and self.count is None:
            raise ValueError("For 'Count' dataclass 'value' or 'count' attribute must be provided.")


@define
class CertificatesStatus(DataclassBase):
    """Number of certificates with given status"""

    invalid: int
    warning: int
    revoked: Optional[int] = field(default=None)


@define
class ControlStatus(DataclassBase):
    """Number of given control statuses"""

    up: int = field(metadata={FIELD_NAME: "controlUp"})
    partial: int
    down: int = field(metadata={FIELD_NAME: "controlDown"})


@define
class SiteHealth(DataclassBase):
    """Number connectivity to devices on sites with given health"""

    full_connectivity: int = field(metadata={FIELD_NAME: "fullConnectivity"})
    partial_connectivity: int = field(metadata={FIELD_NAME: "partialConnectivity"})
    no_connectivity: int = field(metadata={FIELD_NAME: "noConnectivity"})


@define
class vEdgeHealth(DataclassBase):
    """Number of vEdges with given health"""

    normal: int
    warning: int
    error: int


@define
class vSmartStatus(DataclassBase):
    """Number of vSmarts with given status"""

    up: int
    down: int


@define
class TenantStatus(DataclassBase):
    id: str = field(metadata={FIELD_NAME: "tenantId"})
    name: str = field(metadata={FIELD_NAME: "tenantName"})
    control_status: ControlStatus = field(
        metadata={FIELD_NAME: "controlStatus"}, converter=lambda x: create_dataclass(ControlStatus, x)
    )
    site_health: SiteHealth = field(
        metadata={FIELD_NAME: "siteHealth"}, converter=lambda x: create_dataclass(SiteHealth, x)
    )
    vedge_health: vEdgeHealth = field(
        metadata={FIELD_NAME: "vEdgeHealth"}, converter=lambda x: create_dataclass(vEdgeHealth, x)
    )
    vsmart_status: vSmartStatus = field(
        metadata={FIELD_NAME: "vSmartStatus"}, converter=lambda x: create_dataclass(vSmartStatus, x)
    )


@define
class DeviceHealth(DataclassBase):
    name: str
    personality: Personality = field(converter=Personality)
    uuid: str
    reachability: Reachability = field(converter=Reachability)
    longitude: float
    latitude: float
    health: HealthColor = field(converter=HealthColor)
    qoe: int
    location: str
    site_id: str
    system_ip: str
    device_type: Personality = field(converter=Personality)
    local_system_ip: str
    device_model: str
    software_version: str
    cpu_load: float
    memory_utilization: float
    control_connections: int
    control_connections_up: int
    vsmart_control_connections: int
    expected_vsmart_connections: int
    has_geo_data: bool
    uptime_date: int
    device_groups: List[str]
    connected_vmanages: List[str]
    bfd_sessions_up: int
    bfd_sessions: int
    omp_peers: int
    omp_peers_up: int
    board_serial_number: int
    chassis_number: str
    vpn_ids: Any


@define
class DevicesHealth(DataclassBase):
    total_devices: int
    devices: DataSequence[DeviceHealth]


@define
class LicensedDevices(DataclassBase):
    """Number of total and licensed devices"""

    total_devices: int = field(metadata={FIELD_NAME: "totalDevices"})
    licensed_devices: int = field(metadata={FIELD_NAME: "licensedDevice"})


@define
class DeviceHealthOverview(DataclassBase):
    """Number of devices with given health overview"""

    good: int
    fair: int
    poor: int


@define
class TransportHealth(DataclassBase):
    """Contains information about loss percentage, latency and jitter for a given color."""

    entry_time: int
    jitter: int
    color: str
    loss_percentage: float
    latency: int
    app_probe_class: str
    summary_time: int


@define
class TunnelHealth(DataclassBase):
    """Contains information about health for a given tunnel."""

    name: str
    remote_color: str
    remote_system_ip: str
    local_color: str
    local_system_ip: str
    vqoe_score: float
    jitter: float
    rx_octets: float
    loss_percentage: float
    latency: float
    state: str
    tx_octets: int
    health: HealthColor = field(converter=HealthColor)
