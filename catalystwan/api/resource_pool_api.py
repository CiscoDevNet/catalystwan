# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from catalystwan.dataclasses import ResourcePoolData
from catalystwan.typed_list import DataSequence

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class ResourcePoolAPI:
    """API methods of Resource Pool.

    Attributes:
        session: logged in API client session
    Usage example:
        # Create session
        session = create_manager_session(...)
        # Create device vpn
        resource_poold_data = session.api.resource_pool.create()
    """

    URL = "/dataservice/resourcepool/resource/vpn"

    def __init__(self, session: ManagerSession):
        self.session = session

    def get(self, tenant_id: str, tenant_vpn: int) -> DataSequence[ResourcePoolData]:
        """Get device vpn for tenant.

        Args:
            tenant_id: The tenant id.
            tenant_vpn: The number of tenant vpn.

        Returns:
            DataSequence[ResourcePoolData] for tenant.

        TODO note - tenant id doesn't work, need to enter tenant organization name.
        """
        parameters = {"tenantId": tenant_id, "tenantVpn": tenant_vpn}
        response = self.session.get(url=ResourcePoolAPI.URL, params=parameters)
        return response.dataseq(ResourcePoolData)

    def create(self) -> DataSequence[ResourcePoolData]:
        """Create device vpn.

        Returns:
            DataSequence[ResourcePoolData].
        """
        response = self.session.put(url=ResourcePoolAPI.URL)
        logger.info("Create Resource poll vpn.")
        return response.dataseq(ResourcePoolData)

    def delete(self, tenant_id: str, tenant_vpn: int) -> bool:
        """Delete device vpn for tenant.

        Args:
            tenant_id: The tenant id.
            tenant_vpn: The number of tenant vpn.

        Returns:
            bool: True if all ok, False like something wrong

        TODO note - tenant id doesn't work, need to enter tenant organization name.
        """
        parameters = {"tenantId": tenant_id, "tenant_vpn": tenant_vpn}
        response = self.session.delete(url=ResourcePoolAPI.URL, params=parameters)
        return response.ok
