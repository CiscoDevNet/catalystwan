from typing import Optional

from vmngclient.api.basic_api import Device
from vmngclient.dataclasses import TenantInfo, TierInfo
from vmngclient.session import vManageSession
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass


# TODO tests
class TenantsAPI:
    def __init__(self, session: vManageSession):
        self.session = session

    def get_tenants(self, device_id: Optional[Device] = None) -> DataSequence:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Args:
            device_id: Lists all tenants associated with a vSmart.

        Returns:
            DataSequence[TenantInfo]
        """

        if device_id:
            raise NotImplementedError()

        response = self.session.get_data("/dataservice/tenant")
        tenants = [create_dataclass(TenantInfo, tenant_info) for tenant_info in response]

        return DataSequence(TenantInfo, tenants)

    def get_tiers(self) -> DataSequence:
        """TODO"""

        response = self.session.get_data("dataservice/device/tier")
        tiers = [create_dataclass(TierInfo, tier) for tier in response]

        return DataSequence(TierInfo, tiers)
