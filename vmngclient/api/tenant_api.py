from typing import List, Optional

from vmngclient.api.basic_api import Device
from vmngclient.dataclasses import TenantInfo, TierInfo
from vmngclient.exceptions import InvalidOperationError
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass


class TierNameNotFoundError(Exception):
    pass


class TenantNameNotFoundError(Exception):
    pass


# TODO tests
class TenantsAPI:
    def __init__(self, session: vManageSession):
        self.session = session

    def get_tenants(
        self, device_id: Optional[Device] = None, name: Optional[str] = None, organization_name: Optional[str] = None
    ) -> List[TenantInfo]:
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
        tenants = [create_dataclass(TenantInfo, tenant_info) for tenant_info in response]
        if any([name, organization_name]) is False:
            return tenants

        # TODO
        if name:
            return list(filter(lambda tenant: tenant.name == name, tenants))

        if organization_name:
            return list(filter(lambda tenant: tenant.organization_name == organization_name, tenants))
        return []

    def get_tenant(self, name: Optional[str] = None, organization_name: Optional[str] = None) -> TenantInfo:
        if any([name, organization_name]) is False:
            raise ValueError("Argument `name` must be not null.")

        tenants = self.get_tenants(name=name, organization_name=organization_name)
        if not tenants:
            raise TenantNameNotFoundError

        if len(tenants) > 1:
            raise InvalidOperationError("The input sequence contains more than one element.")

        return tenants[0]

    def get_tiers(self, name: Optional[str] = None) -> List[TierInfo]:
        """TODO"""

        response = self.session.get_data("dataservice/device/tier")
        tiers = [create_dataclass(TierInfo, tier) for tier in response]

        if name is None:
            return tiers

        filtered_tiers = list(filter(lambda tier: tier.name == name, tiers))
        return filtered_tiers

    def get_tier(self, name: Optional[str] = None) -> TierInfo:
        """Gets tier with

        Args:
            name: Name of the tier. Defaults to None.

        Raises:
            TierNameNotFoundError: TODO
            InvalidOperationError: Thrown when two or more objects

        Returns:
            TierInfo: _description_
        """
        if name is None:
            raise ValueError("Argument `name` must be not null.")

        tiers = self.get_tiers(name)
        if not tiers:
            raise TierNameNotFoundError

        if len(tiers) > 1:
            raise InvalidOperationError("The input sequence contains more than one element.")

        return tiers[0]
