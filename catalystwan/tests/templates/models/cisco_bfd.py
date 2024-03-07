# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_bfd_model import CiscoBFDModel, Color, ColorType

bfd_model = CiscoBFDModel(  # type: ignore
    template_name="cisco_bfd",
    template_description="na",
    multiplier=100,
    poll_interval=50,
    default_dscp=50,
    color=[
        Color(  # type: ignore
            color=ColorType.BIZ_INTERNET, hello_interval=50, multipler=100, pmtu_discovery=False, dscp=100
        ),
        Color(color=ColorType.SILVER, hello_interval=150, multipler=10, dscp=20),  # type: ignore
    ],
)
