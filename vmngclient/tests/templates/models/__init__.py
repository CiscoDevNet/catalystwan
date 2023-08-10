#  type: ignore
not_my_data = set(globals())
not_my_data.add("not_my_data")

from vmngclient.tests.templates.models.cisco_aaa import cisco_aaa
# from vmngclient.tests.templates.models.omp_vsmart import default_omp, omp_2, omp_3
from vmngclient.tests.templates.models.cisco_system import default_cisco_system

__all__ = list(set(locals()) - not_my_data)
print(locals()['cisco_system'])
