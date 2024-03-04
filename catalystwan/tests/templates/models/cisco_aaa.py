# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore
from catalystwan.api.templates.models.cisco_aaa_model import (
    CiscoAAAModel,
    DomainStripping,
    RadiusGroup,
    RadiusServer,
    TacacsGroup,
    TacacsServer,
    User,
)
from catalystwan.utils.device_model import DeviceModel

users = [
    User(name="admin", password="str", secret="zyx", privilege="15"),  # pragma: allowlist secret
    User(name="user", password="rnd", secret="dnr", privilege="14"),  # pragma: allowlist secret
]

# CiscoAAAModel(domain-stripping="?")
cisco_aaa = CiscoAAAModel(
    template_name="iuo",
    template_description="zyx",
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
    template_name="cisco_aaa_device_specific",
    template_description="caaadp",
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

complex_aaa_model = CiscoAAAModel(
    template_name="complex_aaa",
    template_description="na",
    user=[
        User(name="test1", password="*****", secret="secret", privilege="1"),  # pragma: allowlist secret
        User(name="test2", password="*****", secret="secret", privilege="15"),  # pragma: allowlist secret
    ],
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(
            group_name="group1",
            vpn=10,
            source_interface="Gig1",
            server=[
                RadiusServer(address="1.1.1.1", key="test_key", secret_key="secret_key")  # pragma: allowlist secret
            ],
        ),
        RadiusGroup(
            group_name="group2",
            vpn=11,
            source_interface="Gig2",
            server=[
                RadiusServer(
                    address="1.1.2.1",
                    key="test_key2",
                    secret_key="secret_key2",  # pragma: allowlist secret
                )
            ],
        ),
    ],
    domain_stripping=DomainStripping.RIGHT_TO_LEFT,
    tacacs=[
        TacacsGroup(
            group_name="group1",
            vpn=0,
            source_interface="Gig0",
            server=[TacacsServer(address="1.1.1.1", key="key", secret_key="secret_key")],  # pragma: allowlist secret
        )
    ],
)
