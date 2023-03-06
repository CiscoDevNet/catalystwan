from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.api.basic_api import DevicesAPI
from vmngclient.api.tenant_api import TenantsAPI

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIContainter:
    def __init__(self, session: vManageSession):
        self.tenants = TenantsAPI(session)
        self.devices = DevicesAPI(session)
