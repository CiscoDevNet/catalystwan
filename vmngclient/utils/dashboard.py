from enum import Enum
from typing import Dict, List, Optional, Union

from attr import define, field  # type: ignore

from vmngclient.dataclasses import DataclassBase
from vmngclient.utils.creation_tools import FIELD_NAME


class DeviceName(Enum):
    VMANAGE: str = "vManage"
    VBOND: str = "vBond"
    VSMART: str = "vSmart"
    EDGE: str = "WAN Edge"


class StatusName(Enum):
    CONTROL_STATUS: str = "Control Status"
    CONTROL_UP: str = "Control up"
    PARTIAL_CONTROL: str = "Partial"
    CONTROL_DOWN: str = "Control down"


def name_converter(name):
    for enum_type in (StatusName, DeviceName):
        try:
            return enum_type(name)
        except ValueError:
            pass

    raise ValueError(f"'{name}' is not a valid name.")


@define
class Count(DataclassBase):
    name: Union[DeviceName, StatusName] = field(converter=name_converter)
    count: int
    details_url: str = field(metadata={FIELD_NAME: "detailsURL"})
    status: str
    message: Optional[str] = field(default=None)
    status_list: Union[Optional[List[Dict[str, Union[str, int]]]], "Count"] = field(
        default=None, metadata={FIELD_NAME: "statusList"}
    )


@define
class CertificatesStatus(DataclassBase):
    invalid: int
    warning: int
    revoked: int
