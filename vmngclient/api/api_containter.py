from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.api.tenant_api import TenantsAPI
from vmngclient.api.template_api import TemplatesAPI

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIContainter:
    def __init__(self, session: vManageSession):
        self.tenants = TenantsAPI(session)
        self.templates = TemplatesAPI(session)
