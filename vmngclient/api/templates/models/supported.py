from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel
from vmngclient.api.templates.models.omp_vsmart_model import OMPvSmart
from vmngclient.api.templates.models.security_vsmart_model import SecurityvSmart
from vmngclient.api.templates.models.system_vsmart_model import SystemVsmart

available_models = {
    "cisco_aaa": CiscoAAAModel,
    "omp_vsmart": OMPvSmart,
    "security_vsmart": SecurityvSmart,
    "system_vsmart": SystemVsmart,
}
