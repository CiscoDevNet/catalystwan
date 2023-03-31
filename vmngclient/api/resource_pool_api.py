from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vmngclient.dataclasses import ResourcePoolData
from vmngclient.typed_list import DataSequence

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class ResourcePoolAPI:
    """API methods of Resource Pool.

    Attributes:
        session: logged in API client session
    """

    URL = "/dataservice/resourcepool/resource/vpn"

    def __init__(self, session: vManageSession):
        self.session = session

    def get(self, tenant_id: str, tenant_vpn: int) -> DataSequence[ResourcePoolData]:
        parameters = {"tenantId": tenant_id, "tenant_vpn": tenant_vpn}
        response = self.session.get(url=ResourcePoolAPI.URL, params=parameters)
        return response.dataseq(ResourcePoolData)

    def create(self) -> DataSequence[ResourcePoolData]:
        response = self.session.put(url="/dataservice/resourcepool/resource/vpn")
        return response.dataseq(ResourcePoolData)

    def delete(self, tenant_id: str, tenant_vpn: int) -> bool:
        parameters = {"tenantId": tenant_id, "tenant_vpn": tenant_vpn}
        response = self.session.delete(url=ResourcePoolAPI.URL, params=parameters)
        if response:
            return True
        return False
