from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.primitives.client_api import ClientAPI
from vmngclient.primitives.multitenant_apis_provider_api import MultitenantAPIsProviderAPI

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIPrimitiveContainter:
    def __init__(self, session: vManageSession):
        self.client_api = ClientAPI(session)
        self.multitenant_apis_provider_api = MultitenantAPIsProviderAPI(session)
