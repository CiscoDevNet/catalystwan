# Copyright 2024 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_aaa_model import CiscoAAAModel
from catalystwan.api.templates.models.cisco_banner_model import CiscoBannerModel
from catalystwan.api.templates.models.cisco_bfd_model import CiscoBFDModel
from catalystwan.api.templates.models.cisco_logging_model import CiscoLoggingModel
from catalystwan.api.templates.models.cisco_ntp_model import CiscoNTPModel
from catalystwan.api.templates.models.cisco_omp_model import CiscoOMPModel
from catalystwan.api.templates.models.cisco_ospf import CiscoOSPFModel
from catalystwan.api.templates.models.cisco_secure_internet_gateway import CiscoSecureInternetGatewayModel
from catalystwan.api.templates.models.cisco_snmp_model import CiscoSNMPModel
from catalystwan.api.templates.models.cisco_system import CiscoSystemModel
from catalystwan.api.templates.models.cisco_vpn_interface_model import CiscoVpnInterfaceModel
from catalystwan.api.templates.models.cisco_vpn_model import CiscoVPNModel
from catalystwan.api.templates.models.omp_vsmart_model import OMPvSmart
from catalystwan.api.templates.models.security_vsmart_model import SecurityvSmart
from catalystwan.api.templates.models.system_vsmart_model import SystemVsmart

available_models = {
    "cisco_aaa": CiscoAAAModel,
    "cisco_bfd": CiscoBFDModel,
    "cisco_banner": CiscoBannerModel,
    "cisco_ntp": CiscoNTPModel,
    "cisco_ospf": CiscoOSPFModel,
    "cisco_logging": CiscoLoggingModel,
    "omp_vsmart": OMPvSmart,
    "security_vsmart": SecurityvSmart,
    "system_vsmart": SystemVsmart,
    "cisco_vpn_interface": CiscoVpnInterfaceModel,
    "cisco_system": CiscoSystemModel,
    "cisco_vpn": CiscoVPNModel,
    "cisco_snmp": CiscoSNMPModel,
    "cisco_system": CiscoSystemModel,
    "cisco_secure_internet_gateway": CiscoSecureInternetGatewayModel,
    "cisco_omp": CiscoOMPModel,
}
