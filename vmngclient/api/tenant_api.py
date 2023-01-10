from typing import List, Optional

from vmngclient.api.basic_api import Device
from vmngclient.dataclasses import TenantInfo
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass


class TenantAPI:
    # TODO tests
    def __init__(self, session: vManageSession):
        self.session = session

    def get(self, device_id: Optional[Device] = None) -> List[TenantInfo]:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Args:
            device_id: Lists all tenants associated with a vSmart.

        Returns:
            List[TenantInfo]
        """
        if device_id:
            raise NotImplementedError()
        response = self.session.get_data("/dataservice/tenant")
        return [create_dataclass(TenantInfo, tenant_info) for tenant_info in response]
