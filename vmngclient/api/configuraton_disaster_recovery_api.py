from typing import List, Optional

from attr import define, field  # type: ignore

from vmngclient.dataclasses import DataclassBase
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass


@define(kw_only=True)
class ClusterInfoDevice(DataclassBase):
    hostname: str = field(metadata={FIELD_NAME: "host-name"})
    device_ip: str = field(metadata={FIELD_NAME: "deviceIP"})
    state: str  # might be good idea to have enum here
    is_current_vmanage: bool = field(metadata={FIELD_NAME: "isCurrentVManage"})


@define(kw_only=True)
class ClusterInfo(DataclassBase):
    primary: Optional[List[ClusterInfoDevice]] = field(default=None)
    secondary: Optional[List[ClusterInfoDevice]] = field(default=None)

    def list_all_devices(self) -> List[ClusterInfoDevice]:
        all_devices = []
        if self.primary:
            all_devices += self.primary
        if self.secondary:
            all_devices += self.secondary
        return all_devices

    def list_all_devices_ips(self) -> List[str]:
        return [device.device_ip for device in self.list_all_devices()]


class ConfigurationDisasterRecoveryApi:
    def __init__(self, session: vManageSession):
        self.session = session

    def get_cluster_info(self):
        response = self.session.get("dataservice/disasterrecovery/clusterInfo")
        return create_dataclass(ClusterInfo, response.payload.json.get("clusterInfo"))
