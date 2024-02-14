from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.policy_object.app_probe import AppProbeParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.application_list import ApplicationListParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.data_prefix import DataPrefixParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.expanded_community_list import (
    ExpandedCommunityParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.fowarding_class import FowardingClassParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.ipv6_data_prefix import IPv6DataPrefixParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.ipv6_prefix_list import IPv6PrefixListParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policier import PolicierParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.prefered_group_color import (
    PreferredColorGroupParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.prefix_list import PrefixListParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.sla_class import SLAClassParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.standard_community import (
    StandardCommunityParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.tloc_list import TlocParcel

AnyPolicyObjectParcel = Annotated[
    Union[
        AppProbeParcel,
        ApplicationListParcel,
        ColorParcel,
        DataPrefixParcel,
        ExpandedCommunityParcel,
        FowardingClassParcel,
        IPv6DataPrefixParcel,
        IPv6PrefixListParcel,
        PrefixListParcel,
        PolicierParcel,
        PreferredColorGroupParcel,
        SLAClassParcel,
        TlocParcel,
        StandardCommunityParcel,
    ],
    Field(discriminator="type"),
]

PAYLOAD_ENDPOINT_MAPPING = {
    AppProbeParcel: "app-probe",
    ApplicationListParcel: "app-list",
    ColorParcel: "color",
    DataPrefixParcel: "data-prefix",
    ExpandedCommunityParcel: "expanded-community",
    FowardingClassParcel: "class",
    IPv6DataPrefixParcel: "data-ipv6-prefix",
    IPv6PrefixListParcel: "ipv6-prefix",
    PrefixListParcel: "prefix",
    PolicierParcel: "policer",
    PreferredColorGroupParcel: "preferred-color-group",
    SLAClassParcel: "sla-class",
    TlocParcel: "tloc",
    StandardCommunityParcel: "standard-community",
}
