from enum import Enum

from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel
from vmngclient.api.templates.models.omp_vsmart_model import OMPvSmart
from vmngclient.api.templates.models.security_vsmart_model import SecurityvSmart
from vmngclient.api.templates.models.system_vsmart_model import SystemVsmart


class FeatureTemplateType(Enum):
    cisco_aaa: str = "cedge_aaa"
    omp_vsmart: str = "omp-vsmart"
    security_vsmart: str = "security-vsmart"
    system_vsmart: str = "system-vsmart"


supported_models = [CiscoAAAModel, OMPvSmart, SecurityvSmart, SystemVsmart]
