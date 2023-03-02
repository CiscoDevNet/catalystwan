from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from vmngclient.dataclasses import Device, TenantInfo, TierInfo

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.typed_list import DataSequence


class TenantsAPI:
    def __init__(self, session: vManageSession):
        self.session = session

    def get_tenants(self, device_id: Optional[Device] = None) -> DataSequence[TenantInfo]:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Args:
            device_id: Lists all tenants associated with a vSmart.

        Returns:
            DataSequence[TenantInfo]
        """

        if device_id:
            raise NotImplementedError()

        response = self.session.get("/dataservice/tenant")
        tenants = response.dataseq(TenantInfo)

        return tenants

    def get_tiers(self) -> DataSequence[TierInfo]:
        response = self.session.get(url="dataservice/device/tier")
        tiers = response.dataseq(TierInfo)

        return tiers
