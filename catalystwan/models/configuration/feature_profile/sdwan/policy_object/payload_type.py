from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.policy_object.app_probe import AppProbePayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.application_list import ApplicationListPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.data_prefix import DataPrefixPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.expanded_community_list import (
    ExpandedCommunityPayload,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.fowarding_class import FowardingClassPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.ipv6_data_prefix import IPv6DataPrefixPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.ipv6_prefix_list import IPv6PrefixListPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policier import PolicierPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.prefered_group_color import (
    PreferredColorGroupPayload,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.prefix_list import PrefixListPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.sla_class import SLAClassPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.tloc_list import TlocPayload

AnyPolicyObjectPayload = Annotated[
    Union[
        AppProbePayload,
        ApplicationListPayload,
        ColorPayload,
        DataPrefixPayload,
        ExpandedCommunityPayload,
        FowardingClassPayload,
        IPv6DataPrefixPayload,
        IPv6PrefixListPayload,
        PrefixListPayload,
        PolicierPayload,
        PreferredColorGroupPayload,
        SLAClassPayload,
        TlocPayload,
    ],
    Field(discriminator="type"),
]
