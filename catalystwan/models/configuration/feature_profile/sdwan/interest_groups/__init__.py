from typing import Dict, Mapping, Union

from pydantic import Field
from typing_extensions import Annotated

from .policy.app_probe import AppProbeEntry as AppProbeEntry
from .policy.app_probe import AppProbeMapItem as AppProbeMapItem
from .policy.app_probe import AppProbeParcel as AppProbeParcel
from .policy.application_list import ApplicationFamilyListEntry as ApplicationFamilyListEntry
from .policy.application_list import ApplicationListEntry as ApplicationListEntry
from .policy.application_list import ApplicationListParcel
from .policy.color_list import ColorEntry as ColorEntry
from .policy.color_list import ColorParcel as ColorParcel
from .policy.data_prefix import DataPrefixEntry as DataPrefixEntry
from .policy.data_prefix import DataPrefixParcel as DataPrefixParcel
from .policy.expanded_community_list import ExpandedCommunityParcel as ExpandedCommunityParcel
from .policy.fowarding_class import FowardingClassParcel as FowardingClassParcel
from .policy.fowarding_class import FowardingClassQueueEntry as FowardingClassQueueEntry
from .policy.ipv6_data_prefix import IPv6DataPrefixEntry as IPv6DataPrefixEntry
from .policy.ipv6_data_prefix import IPv6DataPrefixParcel as IPv6DataPrefixParcel
from .policy.ipv6_prefix_list import IPv6PrefixListEntry as IPv6PrefixListEntry
from .policy.ipv6_prefix_list import IPv6PrefixListParcel as IPv6PrefixListParcel
from .policy.policier import PolicierEntry as PolicierEntry
from .policy.policier import PolicierParcel as PolicierParcel
from .policy.prefered_group_color import Preference as Preference
from .policy.prefered_group_color import PreferredColorGroupEntry as PreferredColorGroupEntry
from .policy.prefered_group_color import PreferredColorGroupParcel as PreferredColorGroupParcel
from .policy.prefix_list import PrefixListEntry as PrefixListEntry
from .policy.prefix_list import PrefixListParcel as PrefixListParcel
from .policy.sla_class import FallbackBestTunnel as FallbackBestTunnel
from .policy.sla_class import SLAAppProbeClass as SLAAppProbeClass
from .policy.sla_class import SLAClassCriteriaEnum as SLAClassCriteriaEnum
from .policy.sla_class import SLAClassListEntry as SLAClassListEntry
from .policy.sla_class import SLAClassParcel as SLAClassParcel
from .policy.standard_community import StandardCommunityEntry as StandardCommunityEntry
from .policy.standard_community import StandardCommunityParcel as StandardCommunityParcel
from .policy.tloc_list import TlocEntry as TlocEntry
from .policy.tloc_list import TlocParcel as TlocParcel
from .security.application_list import SecurityApplicationFamilyListEntry as SecurityApplicationFamilyListEntry
from .security.application_list import SecurityApplicationListEntry as SecurityApplicationListEntry
from .security.application_list import SecurityApplicationListParcel as SecurityApplicationListParcel
from .security.data_prefix import SecurityDataPrefixEntry as SecurityDataPrefixEntry
from .security.data_prefix import SecurityDataPrefixParcel as SecurityDataPrefixParcel
from .security.fqdn import FQDNDomainParcel as FQDNDomainParcel
from .security.fqdn import FQDNListEntry as FQDNListEntry
from .security.geolocation_list import GeoLocationListEntry as GeoLocationListEntry
from .security.geolocation_list import GeoLocationListParcel as GeoLocationListParcel
from .security.ips_signature import IPSSignatureListEntry as IPSSignatureListEntry
from .security.ips_signature import IPSSignatureParcel as IPSSignatureParcel
from .security.local_domain import LocalDomainListEntry as LocalDomainListEntry
from .security.local_domain import LocalDomainParcel as LocalDomainParcel
from .security.protocol_list import ProtocolListEntry as ProtocolListEntry
from .security.protocol_list import ProtocolListParcel as ProtocolListParcel
from .security.security_port import SecurityPortListEntry as SecurityPortListEntry
from .security.security_port import SecurityPortParcel as SecurityPortParcel
from .security.url import BaseURLListEntry as BaseURLListEntry
from .security.url import URLAllowParcel as URLAllowParcel
from .security.url import URLBlockParcel as URLBlockParcel
from .security.zone import SecurityZoneListEntry as SecurityZoneListEntry
from .security.zone import SecurityZoneListParcel as SecurityZoneListParcel

AnyInterestGroupParcel = Annotated[
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
        LocalDomainParcel,
        FQDNDomainParcel,
        IPSSignatureParcel,
        URLAllowParcel,
        URLBlockParcel,
        SecurityPortParcel,
        ProtocolListParcel,
        GeoLocationListParcel,
        SecurityZoneListParcel,
        SecurityApplicationListParcel,
        SecurityDataPrefixParcel,
    ],
    Field(discriminator="type"),
]

INTEREST_GROUP_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
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
    LocalDomainParcel: "security-localdomain",
    FQDNDomainParcel: "security-fqdn",
    IPSSignatureParcel: "security-ipssignature",
    URLAllowParcel: "security-urllist",
    URLBlockParcel: "security-urllist",
    SecurityPortParcel: "security-port",
    ProtocolListParcel: "security-protocolname",
    GeoLocationListParcel: "security-geolocation",
    SecurityZoneListParcel: "security-zone",
    SecurityApplicationListParcel: "security-localapp",
    SecurityDataPrefixParcel: "security-data-ip-prefix",
}
