#  type: ignore
from vmngclient.tests.templates.models.cisco_aaa import cisco_aaa
from vmngclient.tests.templates.models.omp_vsmart import default_omp, omp_2, omp_3

__all__ = [
    "default_omp",
    "omp_2",
    "omp_3",  # omp-vsmart
    "cisco_aaa",  # CiscoAAA
]
