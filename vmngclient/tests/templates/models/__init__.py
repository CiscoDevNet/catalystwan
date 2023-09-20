#  type: ignore
from vmngclient.tests.templates.models.cisco_aaa import cisco_aaa, complex_aaa_model
from vmngclient.tests.templates.models.cisco_banner import banner_model
from vmngclient.tests.templates.models.cisco_bfd import bfd_model
from vmngclient.tests.templates.models.cisco_vpn import basic_cisco_vpn, complex_vpn_model
from vmngclient.tests.templates.models.omp_vsmart import default_omp, omp_2, omp_3

__all__ = [
    "default_omp",
    "omp_2",
    "omp_3",
    "cisco_aaa",
    "complex_aaa_model",
    "basic_cisco_vpn",
    "complex_vpn_model",
    "banner_model",
    "bfd_model",
]
