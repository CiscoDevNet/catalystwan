from typing import List, Literal, Optional, Set, Tuple, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.model.common import InterfaceTypeEnum
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
        pattern="^[a-zA-Z0-9_-]{1,32}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 32 characters",
    )
    description: Optional[str] = "Desc Not Required"


class DataPrefixList(PolicyListHeader):
    type: Literal["dataPrefix"] = "dataPrefix"
    entries: List[DataPrefixListEntry]


class SiteList(PolicyListHeader):
    type: Literal["site"] = "site"
    entries: List[SiteListEntry] = []

    def add_sites(self, sites: Set[int]):
        for site in sites:
            self.entries.append(SiteListEntry(site_id=str(site)))  # type: ignore[call-arg]

    def add_site_range(self, site_range: Tuple[int, int]):
        entry = SiteListEntry(site_id=f"{site_range[0]}-{site_range[1]}")  # type: ignore[call-arg]
        self.entries.append(entry)


class VPNList(PolicyListHeader):
    type: Literal["vpn"] = "vpn"
    entries: List[VPNListEntry] = []

    def add_vpns(self, vpns: Set[int]):
        for vpn in vpns:
            self.entries.append(VPNListEntry(vpn=str(vpn)))  # type: ignore[call-arg]

    def add_vpn_range(self, vpn_range: Tuple[int, int]):
        entry = VPNListEntry(vpn=f"{vpn_range[0]}-{vpn_range[1]}")  # type: ignore[call-arg]
        self.entries.append(entry)


class ZoneList(PolicyListHeader):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=str(vpn)) for vpn in vpns]  # type: ignore[call-arg]

    def assign_interfaces(self, ifs: Set[InterfaceTypeEnum]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]  # type: ignore[call-arg]


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
    entries: List[ClassMapListEntry] = []

    def add_queue(self, queue: int) -> None:
        self.entries.append(ClassMapListEntry(queue=str(queue)))


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
        AppList,
        AppProbeClassList,
        ASPathList,
        ClassMapList,
        ColorList,
        CommunityList,
        DataIPv6PrefixList,
        DataPrefixList,
        ExpandedCommunityList,
        FQDNList,
        GeoLocationList,
        IPSSignatureList,
        IPv6PrefixList,
        LocalAppList,
        LocalDomainList,
        MirrorList,
        PolicerList,
        PortList,
        PreferredColorGroupList,
        PrefixList,
        ProtocolNameList,
        SiteList,
        SLAClassList,
        TLOCList,
        URLBlackList,
        URLWhiteList,
        VPNList,
        ZoneList,
    ],
    Field(discriminator="type"),
]
