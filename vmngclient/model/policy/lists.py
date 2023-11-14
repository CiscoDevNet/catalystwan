from typing import List, Literal, Optional, Union

from pydantic.v1 import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.model.policy.lists_entries import (
    AppListEntry,
    AppProbeClassListEntry,
    ASPathListEntry,
    ClassMapListEntry,
    ColorListEntry,
    CommunityListEntry,
    DataIPv6PrefixListEntry,
    DataPrefixListEntry,
    FQDNListEntry,
    GeoLocationListEntry,
    IPSSignatureListEntry,
    IPv6PrefixListEntry,
    LocalAppListEntry,
    LocalDomainListEntry,
    MirrorListEntry,
    PolicerListEntry,
    PortListEntry,
    PreferredColorGroupListEntry,
    PrefixListEntry,
    ProtocolNameListEntry,
    SiteListEntry,
    SLAClassListEntry,
    TLOCListEntry,
    URLListEntry,
    VPNListEntry,
    ZoneListEntry,
)


class PolicyListHeader(BaseModel):
    name: str = Field(
        regex="^[a-zA-Z0-9_-]{1,32}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 32 characters",
    )
    description: Optional[str] = "Desc Not Required"


class DataPrefixList(PolicyListHeader):
    type: Literal["dataPrefix"] = "dataPrefix"
    entries: List[DataPrefixListEntry]


class SiteList(PolicyListHeader):
    type: Literal["site"] = "site"
    entries: List[SiteListEntry]


class VPNList(PolicyListHeader):
    type: Literal["vpn"] = "vpn"
    entries: List[VPNListEntry]


class ZoneList(PolicyListHeader):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry]


class FQDNList(PolicyListHeader):
    type: Literal["fqdn"] = "fqdn"
    entries: List[FQDNListEntry]


class GeoLocationList(PolicyListHeader):
    type: Literal["geoLocation"] = "geoLocation"
    entries: List[GeoLocationListEntry]


class PortList(PolicyListHeader):
    type: Literal["port"] = "port"
    entries: List[PortListEntry]


class ProtocolNameList(PolicyListHeader):
    type: Literal["protocolName"] = "protocolName"
    entries: List[ProtocolNameListEntry]


class LocalAppList(PolicyListHeader):
    type: Literal["localApp"] = "localApp"
    entries: List[LocalAppListEntry]


class AppList(PolicyListHeader):
    type: Literal["app"] = "app"
    entries: List[AppListEntry]


class ColorList(PolicyListHeader):
    type: Literal["color"] = "color"
    entries: List[ColorListEntry]


class DataIPv6PrefixList(PolicyListHeader):
    type: Literal["dataIpv6Prefix"] = "dataIpv6Prefix"
    entries: List[DataIPv6PrefixListEntry]


class LocalDomainList(PolicyListHeader):
    type: Literal["localDomain"] = "localDomain"
    entries: List[LocalDomainListEntry]


class IPSSignatureList(PolicyListHeader):
    type: Literal["ipsSignature"] = "ipsSignature"
    entries: List[IPSSignatureListEntry]


class URLWhiteList(PolicyListHeader):
    type: Literal["urlWhiteList"] = "urlWhiteList"
    entries: List[URLListEntry]


class URLBlackList(PolicyListHeader):
    type: Literal["urlBlackList"] = "urlBlackList"
    entries: List[URLListEntry]


class CommunityList(PolicyListHeader):
    type: Literal["community"] = "community"
    entries: List[CommunityListEntry]


class ExpandedCommunityList(PolicyListHeader):
    type: Literal["expandedCommunity"] = "expandedCommunity"
    entries: List[CommunityListEntry]


class PolicerList(PolicyListHeader):
    type: Literal["policer"] = "policer"
    entries: List[PolicerListEntry]


class ASPathList(PolicyListHeader):
    type: Literal["asPath"] = "asPath"
    entries: List[ASPathListEntry]


class ClassMapList(PolicyListHeader):
    type: Literal["class"] = "class"
    entries: List[ClassMapListEntry]


class MirrorList(PolicyListHeader):
    type: Literal["mirror"] = "mirror"
    entries: List[MirrorListEntry]


class AppProbeClassList(PolicyListHeader):
    type: Literal["appProbe"] = "appProbe"
    entries: List[AppProbeClassListEntry]


class SLAClassList(PolicyListHeader):
    type: Literal["sla"] = "sla"
    entries: List[SLAClassListEntry]


class TLOCList(PolicyListHeader):
    type: Literal["tloc"] = "tloc"
    entries: List[TLOCListEntry]


class PreferredColorGroupList(PolicyListHeader):
    type: Literal["preferredColorGroup"] = "preferredColorGroup"
    entries: List[PreferredColorGroupListEntry]


class PrefixList(PolicyListHeader):
    type: Literal["prefix"] = "prefix"
    entries: List[PrefixListEntry]


class IPv6PrefixList(PolicyListHeader):
    type: Literal["ipv6prefix"] = "ipv6prefix"
    entries: List[IPv6PrefixListEntry]


AllPolicyLists = Annotated[
    Union[
        DataPrefixList,
        SiteList,
        VPNList,
        ZoneList,
        FQDNList,
        GeoLocationList,
        PortList,
        ProtocolNameList,
        LocalAppList,
        AppList,
        ColorList,
        DataIPv6PrefixList,
        LocalDomainList,
        IPSSignatureList,
        URLWhiteList,
        URLBlackList,
        CommunityList,
        ExpandedCommunityList,
        PolicerList,
        ASPathList,
        ClassMapList,
        MirrorList,
        AppProbeClassList,
        SLAClassList,
        TLOCList,
        PreferredColorGroupList,
        PrefixList,
        IPv6PrefixList,
    ],
    Field(discriminator="type"),
]
