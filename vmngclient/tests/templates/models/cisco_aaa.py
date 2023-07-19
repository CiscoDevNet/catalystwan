from vmngclient.api.templates.models.cisco_aaa_model import (
    CiscoAAAModel,
    DomainStripping,
    RadiusGroup,
    RadiusServer,
    User,
)
from vmngclient.utils.device_model import DeviceModel

users = [
    User(name="admin", password="str", secret="zyx", privilege="15"),
    User(name="user", password="rnd", secret="dnr", privilege="14"),
]

# CiscoAAAModel(domain-stripping="?")
cisco_aaa = CiscoAAAModel(
    name="iuo",
    description="zyx",
    device_models=[DeviceModel.VEDGE_C8000V],
    user=users,
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(  # type: ignore
            group_name="xyz", vpn=1, source_interface="GIG11", server=[RadiusServer(address="1.1.1.1", key="21")]
        )
    ],
    domain_stripping=DomainStripping.NO,  # type: ignore
)

cisco_aaa_device_specific = CiscoAAAModel(
    name="cisco_aaa_device_specific",
    description="caaadp",
    device_models=[DeviceModel.VEDGE_C8000V],
    user=users,
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(  # type: ignore
            group_name="xyz", vpn=1, source_interface="GIG11", server=[RadiusServer(address="1.1.1.1", key="21")]
        )
    ],
    domain_stripping=DomainStripping.NO,
)
