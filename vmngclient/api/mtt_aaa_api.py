import logging

from vmngclient.dataclasses import TenantAAA, TenantRadiusServer, TenantTacacsServer
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import asdict, create_dataclass

logger = logging.getLogger(__name__)


class AAAConfigNotPresent(Exception):
    pass


def status_ok(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        return True if response.status_code == 200 else False

    return wrapper


class TenantAaaAPI:
    """
    Used to configure  mtt tenant management users remote servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session
        self.url_path = "/dataservice/admin/aaa"

    def __str__(self) -> str:
        return str(self.session)

    def aaa_exists(self) -> bool:
        return True if self.session.get_data(self.url_path) else False

    @status_ok
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
        data = asdict(tenant_aaa)  # type: ignore
        return self.session.post(url=self.url_path, json=data)

    def get_aaa(self) -> TenantAAA:
        """
        Returns the Tenant AAA
        :param aaa:
        :return:
        """
        tenant_aaa = self.session.get_data(self.url_path)
        logger.debug(f"Tenant AAA: {tenant_aaa}")
        return create_dataclass(TenantAAA, tenant_aaa)

    @status_ok
    def del_aaa(self) -> bool:
        """
        Delete aaa works only for tenants
        :return:
        """
        id = self.session.get_tenant_id()
        logger.debug(f"Deleting AAA on {id}.")
        if not self.aaa_exists():
            raise AAAConfigNotPresent(f"No AAA config present for Tenant id={id}")
        return self.session.delete(self.url_path)

    @status_ok
    def put_aaa(self, tenant_AAA: TenantAAA) -> bool:
        """
        Updated the AAA for tenant
        :return:
        """
        data = asdict(tenant_AAA)  # type: ignore
        return self.session.put(url=self.url_path, json=data)


class TenantRadiusAPI:
    """
    Used to configure  mtt tenant remote aaa radius servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session
        self.url_path = "/dataservice/admin/radius"

    def __str__(self) -> str:
        return str(self.session)

    @status_ok
    def add_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        Create RADIUS for tenant
        :param radius_server:
        :return:
        """
        data = asdict(radius_server)  # type: ignore
        return self.session.post(url=self.url_path, json=data)

    @status_ok
    def put_radius(self, radius_server: TenantRadiusServer) -> bool:
        """
        edit radius server
        :param radius_server:
        :return:
        """
        data = asdict(radius_server)  # type: ignore
        return self.session.put(url=self.url_path, json=data)

    @status_ok
    def delete_radius(self) -> bool:
        """
        edit radius server
        :param radius_server:
        :return: True|False
        """
        return self.session.delete(self.url_path)

    def get_radius(self) -> TenantRadiusServer:
        """
        Retrieve Radius server
        :return: TenantRadiusServer
        """
        data = self.session.get_data(self.url_path)
        return create_dataclass(TenantRadiusServer, data)


class TenantTacacsAPI:
    """
    Used to configure mtt tenant remote aaa TACACS servers
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session
        self.url_path = "/dataservice/admin/tacacs"

    def __str__(self) -> str:
        return str(self.session)

    @status_ok
    def add_tacacs(self, tacacs_server: TenantTacacsServer) -> bool:
        """
        Create TACACS for tenant
        :param tacacs_server:
        :return:
        """
        data = asdict(tacacs_server)  # type: ignore
        return self.session.post(url=self.url_path, json=data)

    @status_ok
    def put_tacacs(self, tacacs_server: TenantTacacsServer) -> bool:
        """
        Update tacacs server
        :param tacacs_server:
        :return:
        """
        data = asdict(tacacs_server)  # type: ignore
        return self.session.put(url=self.url_path, json=data)

    @status_ok
    def delete_tacacs(self) -> bool:
        """
        Deletes tacacs server
        :param tacacs_server:
        :return: True|False
        """
        return self.session.delete(self.url_path)

    def get_tacacs(self) -> TenantTacacsServer:
        """
        Retrieves Tacacs server
        :return: TenantTacacsServer
        """
        data = self.session.get_data(self.url_path)
        return create_dataclass(TenantTacacsServer, data)
