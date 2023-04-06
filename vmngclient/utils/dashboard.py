from enum import Enum
from typing import List, Optional, Union

from attr import define, field  # type: ignore

from vmngclient.dataclasses import DataclassBase
from vmngclient.utils.creation_tools import FIELD_NAME


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
    details_url: str = field(metadata={FIELD_NAME: "detailsURL"})
    count: Optional[int] = field(default=None)
    status: Optional[str] = field(default=None)
    name: Optional[
        Union[DeviceName, StatusName, BfdConnectivityName, InventoryName, PercentageDistributionName]
    ] = field(default=None, converter=name_converter)
    message: Optional[str] = field(default=None)
    status_list: Optional[List["Count"]] = field(default=None, metadata={FIELD_NAME: "statusList"})
    list: Optional[str] = field(default=None)
    value: Optional[int] = field(default=None)
    percentageDistribution: Optional[PercentageDistribution] = field(default=None)

    @value.validator  # type: ignore
    def value_or_count_provided(self, attribute, value):
        if value is None and self.count is None:
            raise ValueError("For 'Count' dataclass 'value' or 'count' attribute must be provided.")


@define
class CertificatesStatus(DataclassBase):
    invalid: int
    warning: int
    revoked: int
