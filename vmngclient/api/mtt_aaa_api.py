import logging

from vmngclient.dataclasses import TenantAAA, TenantRadiusServer, TenantTacacsServer
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import asdict, create_dataclass

logger = logging.getLogger(__name__)


class AAAConfigNotPresent(Exception):
    pass


class TenantAaaAPI:
    """
    Used to configure  mtt tenant management users remote servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def add_aaa(self, tenant_aaa: TenantAAA) -> bool:
        """ "
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
        response = self.session.put(url=url_path, json=data)
        return True if response.status_code == 200 else False


class TenantRadiusAPI:
    """
    Used to configure  mtt tenant remote aaa radius servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def add_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        Create RADIUS for tenant
        :param radius_server:
        :return:
        """
        url_path = "/dataservice/admin/radius"
        data = asdict(radius_server)  # type: ignore
        response = self.session.post(url=url_path, json=data)
        return True if response.status_code == 200 else False

    def put_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        edit radius server
        :param radius_server:
        :return:
        """
        url_path = "/dataservice/admin/radius"
        data = asdict(radius_server)  # type: ignore
        response = self.session.put(url=url_path, json=data)
        return True if response.status_code == 200 else False

    def delete_radius(self) -> bool:
        """
        edit radius server
        :param radius_server:
        :return: True|False
        """
        url_path = "/dataservice/admin/radius"
        response = self.session.delete(url_path)
        return True if response.status_code == 204 else False

    def get_radius(self) -> TenantRadiusServer:
        """
        Retrieve Radius server
        :return: TenantRadiusServer
        """
        url_path = "/dataservice/admin/radius"
        data = self.session.get_data(url_path)
        return create_dataclass(TenantRadiusServer, data)


class TenantTacacsAPI:
    """
    Used to configure mtt tenant remote aaa TACACS servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def add_tacacs(self, tacacs_server: TenantTacacsServer) -> bool:
        """
        Create TACACS for tenant
        :param tacacs_server:
        :return:
        """
        url_path = "/dataservice/admin/tacacs"
        data = asdict(tacacs_server)  # type: ignore
        response = self.session.post(url=url_path, json=data)
        return True if response.status_code == 200 else False

    def put_tacacs(self, tacacs_server: TenantTacacsServer) -> bool:
        """
        Update tacacs server
        :param tacacs_server:
        :return:
        """
        url_path = "/dataservice/admin/tacacs"
        data = asdict(tacacs_server)  # type: ignore
        response = self.session.put(url=url_path, json=data)
        return True if response.status_code == 200 else False

    def delete_tacacs(self) -> bool:
        """
        Deletes tacacs server
        :param tacacs_server:
        :return: True|False
        """
        url_path = "/dataservice/admin/tacacs"
        response = self.session.delete(url_path)
        return True if response.status_code == 204 else False

    def get_tacacs(self) -> TenantTacacsServer:
        """
        Retrieves Tacacs server
        :return: TenantTacacsServer
        """
        url_path = "/dataservice/admin/tacacs"
        data = self.session.get_data(url_path)
        return create_dataclass(TenantTacacsServer, data)
