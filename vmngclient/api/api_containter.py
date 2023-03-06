from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.api.admin_tech_api import AdminTechAPI
from vmngclient.api.alarms_api import AlarmsAPI
from vmngclient.api.basic_api import DevicesAPI, DeviceStateAPI
from vmngclient.api.logs_api import LogsAPI
from vmngclient.api.mtt_aaa_api import TenantAaaAPI
from vmngclient.api.omp_api import OmpAPI
from vmngclient.api.packet_capture_api import PacketCaptureAPI
from vmngclient.api.speedtest_api import SpeedtestAPI
from vmngclient.api.template_api import TemplatesAPI
from vmngclient.api.tenant_api import TenantsAPI
from vmngclient.api.tenant_backup_restore_api import TenantBackupRestoreAPI
from vmngclient.api.versions_utils import RepositoryAPI

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class APIContainter:
    def __init__(self, session: vManageSession):
        self.tenants = TenantsAPI(session)
        self.admin_tech = AdminTechAPI(session)
        self.alarms = AlarmsAPI(session)
        self.devices = DevicesAPI(session)
        self.device_state = DeviceStateAPI(session)
        self.logs = LogsAPI(session)
        self.tenant_aaa = TenantAaaAPI(session)
        self.omp = OmpAPI(session)
        self.packet_capture = PacketCaptureAPI(session)
        self.speedtest = SpeedtestAPI(session)
        self.templates = TemplatesAPI(session)
        self.tenant_backup = TenantBackupRestoreAPI(session)
        self.repository = RepositoryAPI(session)
