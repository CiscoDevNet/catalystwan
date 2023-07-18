# type: ignore
from vmngclient.api.templates.models.cisco_aaa_model import (
    CiscoAAAModel,
    DomainStripping,
    RadiusGroup,
    RadiusServer,
    User,
)

users = [
    User(name="admin", password="str", secret="zyx", privilege="15"),
    User(name="user", password="rnd", secret="dnr", privilege="14"),
]


cisco_aaa = CiscoAAAModel(
    name="iuo",
    description="zyx",
    device_models=["vedge-C8000V"],
    user=users,
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(
            group_name="xyz", vpn=1, source_interface="GIG11", server=[RadiusServer(address="1.1.1.1", key="21")]
        )
    ],
    domain_stripping=DomainStripping.NO,
)

cisco_aaa_device_specific = CiscoAAAModel(
    name="cisco_aaa_device_specific",
    description="caaadp",
    device_models=["vedge-C8000V"],
    user=users,
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(
            group_name="xyz", vpn=1, source_interface="GIG11", server=[RadiusServer(address="1.1.1.1", key="21")]
        )
    ],
    domain_stripping=DomainStripping.NO,
)
