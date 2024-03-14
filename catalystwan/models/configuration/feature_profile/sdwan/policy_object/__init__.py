# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .policy.app_probe import AppProbeMapItem, AppProbeParcel
from .policy.application_list import ApplicationFamilyListEntry, ApplicationListEntry, ApplicationListParcel
from .policy.color_list import ColorEntry, ColorParcel
from .policy.data_prefix import DataPrefixEntry, DataPrefixParcel
from .policy.expanded_community_list import ExpandedCommunityParcel
from .policy.fowarding_class import FowardingClassParcel, FowardingClassQueueEntry
from .policy.ipv6_data_prefix import IPv6DataPrefixEntry, IPv6DataPrefixParcel
from .policy.ipv6_prefix_list import IPv6PrefixListEntry, IPv6PrefixListParcel
from .policy.policer import PolicerEntry, PolicerParcel
from .policy.prefered_group_color import Preference, PreferredColorGroupEntry, PreferredColorGroupParcel
from .policy.prefix_list import PrefixListEntry, PrefixListParcel
from .policy.sla_class import FallbackBestTunnel, SLAAppProbeClass, SLAClassCriteria, SLAClassListEntry, SLAClassParcel
from .policy.standard_community import StandardCommunityEntry, StandardCommunityParcel
from .policy.tloc_list import TlocEntry, TlocParcel
from .security.application_list import (
    SecurityApplicationFamilyListEntry,
    SecurityApplicationListEntry,
    SecurityApplicationListParcel,
)
from .security.data_prefix import SecurityDataPrefixEntry, SecurityDataPrefixParcel
from .security.fqdn import FQDNDomainParcel, FQDNListEntry
from .security.geolocation_list import GeoLocationListEntry, GeoLocationListParcel
from .security.ips_signature import IPSSignatureListEntry, IPSSignatureParcel
from .security.local_domain import LocalDomainListEntry, LocalDomainParcel
from .security.protocol_list import ProtocolListEntry, ProtocolListParcel
from .security.security_port import SecurityPortListEntry, SecurityPortParcel
from .security.url import BaseURLListEntry, URLAllowParcel, URLBlockParcel, URLParcel
from .security.zone import SecurityZoneListEntry, SecurityZoneListParcel

AnyPolicyObjectParcel = Annotated[
    Union[
        URLParcel,
        ApplicationListParcel,
        AppProbeParcel,
        ColorParcel,
        DataPrefixParcel,
        ExpandedCommunityParcel,
        FowardingClassParcel,
        FQDNDomainParcel,
        GeoLocationListParcel,
        IPSSignatureParcel,
        IPv6DataPrefixParcel,
        IPv6PrefixListParcel,
        LocalDomainParcel,
        PolicerParcel,
        PreferredColorGroupParcel,
        PrefixListParcel,
        ProtocolListParcel,
        SecurityApplicationListParcel,
        SecurityDataPrefixParcel,
        SecurityPortParcel,
        SecurityZoneListParcel,
        SLAClassParcel,
        StandardCommunityParcel,
        TlocParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = (
    "AnyPolicyObjectParcel",
    "ApplicationFamilyListEntry",
    "ApplicationListEntry",
    "ApplicationListParcel",
    "AppProbeEntry",
    "AppProbeMapItem",
    "AppProbeParcel",
    "BaseURLListEntry",
    "ColorEntry",
    "ColorParcel",
    "DataPrefixEntry",
    "DataPrefixParcel",
    "ExpandedCommunityParcel",
    "FallbackBestTunnel",
    "FowardingClassParcel",
    "FowardingClassQueueEntry",
    "FQDNDomainParcel",
    "FQDNListEntry",
    "GeoLocationListEntry",
    "GeoLocationListParcel",
    "IPSSignatureListEntry",
    "IPSSignatureParcel",
    "IPv6DataPrefixEntry",
    "IPv6DataPrefixParcel",
    "IPv6PrefixListEntry",
    "IPv6PrefixListParcel",
    "LocalDomainListEntry",
    "LocalDomainParcel",
    "PolicerEntry",
    "PolicerParcel",
    "Preference",
    "PreferredColorGroupEntry",
    "PreferredColorGroupParcel",
    "PrefixListEntry",
    "PrefixListParcel",
    "ProtocolListEntry",
    "ProtocolListParcel",
    "SecurityApplicationFamilyListEntry",
    "SecurityApplicationListEntry",
    "SecurityApplicationListParcel",
    "SecurityDataPrefixEntry",
    "SecurityDataPrefixParcel",
    "SecurityPortListEntry",
    "SecurityPortParcel",
    "SecurityZoneListEntry",
    "SecurityZoneListParcel",
    "SLAAppProbeClass",
    "SLAClassCriteria",
    "SLAClassListEntry",
    "SLAClassParcel",
    "StandardCommunityEntry",
    "StandardCommunityParcel",
    "TlocEntry",
    "TlocParcel",
    "URLParcel",
    "URLAllowParcel",
    "URLBlockParcel",
)


def __dir__() -> "List[str]":
    return list(__all__)
