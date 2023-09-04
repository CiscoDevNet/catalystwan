from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel
from vmngclient.api.templates.models.cisco_banner_model import CiscoBannerModel
from vmngclient.api.templates.models.cisco_bfd_model import CiscoBFDModel
from vmngclient.api.templates.models.cisco_ntp_model import CiscoNTPModel
from vmngclient.api.templates.models.cisco_snmp_model import CiscoSNMPModel
from vmngclient.api.templates.models.cisco_system import CiscoSystemModel
from vmngclient.api.templates.models.cisco_vpn_interface_model import CiscoVpnInterfaceModel
from vmngclient.api.templates.models.cisco_vpn_model import CiscoVPNModel
from vmngclient.api.templates.models.omp_vsmart_model import OMPvSmart
from vmngclient.api.templates.models.security_vsmart_model import SecurityvSmart
from vmngclient.api.templates.models.system_vsmart_model import SystemVsmart

available_models = {
    "cisco_aaa": CiscoAAAModel,
    "cisco_bfd": CiscoBFDModel,
    "cisco_banner": CiscoBannerModel,
    "cisco_ntp": CiscoNTPModel,
    "omp_vsmart": OMPvSmart,
    "security_vsmart": SecurityvSmart,
    "system_vsmart": SystemVsmart,
    "cisco_vpn_interface": CiscoVpnInterfaceModel,
    "cisco_system": CiscoSystemModel,
    "cisco_vpn": CiscoVPNModel,
    "cisco_snmp": CiscoSNMPModel,
    "cisco_system": CiscoSystemModel,
}
