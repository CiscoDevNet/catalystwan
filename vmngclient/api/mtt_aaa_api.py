import logging
from typing import List, Union, cast

from vmngclient.session import vManageSession
from vmngclient.dataclasses import TenantAAA, TenantRadiusServer, TenantTacacsServer
from vmngclient.utils.creation_tools import asdict, create_dataclass

logger = logging.getLogger(__name__)


class AaaAPI:
    """
    Used to configure  mtt tenant management users remote servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def add_aaa(self, tenant_aaa: TenantAAA) -> bool:
        """"
        TenantAAA:
            "authOrder": [ "local", "radius", "tacacs"],
            "authFallback": true,
            "adminAuthOrder": false,
            "auditDisable": false,
            "accounting": false,
            "radiusServers": "server1"

        returns bool depending on the api post call
        """
        url_path = "/dataservice/admin/aaa"
        data = asdict(tenant_aaa)  # type: ignore

        response = self.session.post(url=url_path, json=data)
        logger.info(response)
        return True if response.status_code == 200 else False

    def get_aaa(self) -> TenantAAA:
        """
        Returns the Tenant AAA
        :param aaa:
        :return:
        """
        url_path = "/dataservice/admin/aaa"
        tenant_aaa = self.session.get_data(url_path)
        logger.debug(f"Tenant AAA: {tenant_aaa}")
        return create_dataclass(TenantAAA, tenant_aaa)

    def del_aaa(self) -> bool:
        """
        Delete aaa works only for tenants
        :return:
        """
        url_path = "/dataservice/admin/aaa"
        logger.debug(f"Deleting AAA on {self.session.get_tenant_id()}.")
        response = self.session.delete(url_path)
        return True if response.status_code == 200 else False

    def put_aaa(self, tenant_AAA: TenantAAA) -> bool:
        """
        Updated the AAA for tenant
        :return:
        """
        url_path = "/dataservice/admin/aaa"
        data = asdict(tenant_AAA)  # type: ignore
        response = self.session.put(url_path, data)
        return True if response.status_code == 200 else False

    def add_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        Create RADIUS for tenant
        :param radius_server:
        :return:
        """
        url_path = "/dataservice/admin/radius"
        data = asdict(radius_server)  # type: ignore
        response = self.session.post(url=url_path, json=data)
        logger.info(response)
        return True if response.status_code == 200 else False

    def put_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        edit radius server
        :param radius_server:
        :return:
        """
        url_path = "/dataservice/admin/radius"
        data = asdict(radius_server)  # type: ignore
        response = self.session.put(url_path, data)
        logger.info(response)
        return True if response.status_code == 200 else False

    def delete_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        edit radius server
        :param radius_server:
        :return: True|False
        """
        url_path = "/dataservice/admin/radius"
        data = asdict(radius_server)  # type: ignore
        response = self.session.put(url_path, data)
        logger.info(response)
        return True if response.status_code == 204 else False

    def get_radius(self) -> TenantRadiusServer:
        """

        :return:
        """
        url_path = "/dataservice/admin/radius"
        data = self.session.get_data(url_path)[0]
        return create_dataclass(TenantRadiusServer, data)



