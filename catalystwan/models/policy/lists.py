# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Network, IPv6Network
from typing import Any, List, Literal, Optional, Set, Tuple
from uuid import UUID

from pydantic import BaseModel, Field

from catalystwan.models.common import InterfaceType, TLOCColor, WellKnownBGPCommunities
from catalystwan.models.policy.lists_entries import (
    AppListEntry,
    AppProbeClassListEntry,
    ASPathListEntry,
    ClassMapListEntry,
    ColorGroupPreference,
    ColorListEntry,
    CommunityListEntry,
    DataIPv6PrefixListEntry,
    DataPrefixListEntry,
    EncapType,
    FQDNListEntry,
    GeoLocationListEntry,
    IPSSignatureListEntry,
    IPv6PrefixListEntry,
    LocalAppListEntry,
    LocalDomainListEntry,
    MirrorListEntry,
    PathPreference,
    PolicerExceedAction,
    PolicerListEntry,
    PortListEntry,
    PreferredColorGroupListEntry,
    PrefixListEntry,
    ProtocolNameListEntry,
    RegionListEntry,
    SiteListEntry,
    SLAClassListEntry,
    TLOCListEntry,
    URLListEntry,
    VPNListEntry,
    ZoneListEntry,
)


class PolicyListBase(BaseModel):
    name: str = Field(
        pattern="^[a-zA-Z0-9_-]{1,32}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 32 characters",
    )
    description: Optional[str] = "Desc Not Required"
    entries: List[Any]

    def _add_entry(self, entry: Any, single: bool = False) -> None:
        if self.entries and single:
            self.entries[0] = entry
            del self.entries[1:]
        else:
            self.entries.append(entry)


class DataPrefixList(PolicyListBase):
    type: Literal["dataPrefix"] = "dataPrefix"
    entries: List[DataPrefixListEntry] = []

    def add_prefix(self, ip_prefix: IPv4Network) -> None:
        self._add_entry(DataPrefixListEntry(ip_prefix=ip_prefix))


class SiteList(PolicyListBase):
    type: Literal["site"] = "site"
    entries: List[SiteListEntry] = []

    def add_sites(self, sites: Set[int]):
        for site in sites:
            self._add_entry(SiteListEntry(site_id=str(site)))

    def add_site_range(self, site_range: Tuple[int, int]):
        entry = SiteListEntry(site_id=f"{site_range[0]}-{site_range[1]}")
        self._add_entry(entry)


class VPNList(PolicyListBase):
    type: Literal["vpn"] = "vpn"
    entries: List[VPNListEntry] = []

    def add_vpns(self, vpns: Set[int]):
        for vpn in vpns:
            self._add_entry(VPNListEntry(vpn=str(vpn)))

    def add_vpn_range(self, vpn_range: Tuple[int, int]):
        entry = VPNListEntry(vpn=f"{vpn_range[0]}-{vpn_range[1]}")
        self._add_entry(entry)


class ZoneList(PolicyListBase):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=str(vpn)) for vpn in vpns]

    def assign_interfaces(self, ifs: Set[InterfaceType]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]


class FQDNList(PolicyListBase):
    type: Literal["fqdn"] = "fqdn"
    entries: List[FQDNListEntry] = []


class GeoLocationList(PolicyListBase):
    type: Literal["geoLocation"] = "geoLocation"
    entries: List[GeoLocationListEntry] = []


class PortList(PolicyListBase):
    type: Literal["port"] = "port"
    entries: List[PortListEntry] = []


class ProtocolNameList(PolicyListBase):
    type: Literal["protocolName"] = "protocolName"
    entries: List[ProtocolNameListEntry] = []


class LocalAppList(PolicyListBase):
    type: Literal["localApp"] = "localApp"
    entries: List[LocalAppListEntry] = []


class AppList(PolicyListBase):
    type: Literal["app"] = "app"
    entries: List[AppListEntry] = []

    def add_app(self, app: str) -> None:
        self._add_entry(AppListEntry(app=app))

    def add_app_family(self, app_family: str) -> None:
        self._add_entry(AppListEntry(app_family=app_family))


class ColorList(PolicyListBase):
    type: Literal["color"] = "color"
    entries: List[ColorListEntry] = []

    def add_color(self, color: TLOCColor) -> None:
        self._add_entry(ColorListEntry(color=color))


class DataIPv6PrefixList(PolicyListBase):
    type: Literal["dataIpv6Prefix"] = "dataIpv6Prefix"
    entries: List[DataIPv6PrefixListEntry] = []

    def add_prefix(self, ipv6_prefix: IPv6Network) -> None:
        self._add_entry(DataIPv6PrefixListEntry(ipv6_prefix=ipv6_prefix))


class LocalDomainList(PolicyListBase):
    type: Literal["localDomain"] = "localDomain"
    entries: List[LocalDomainListEntry] = []


class IPSSignatureList(PolicyListBase):
    type: Literal["ipsSignature"] = "ipsSignature"
    entries: List[IPSSignatureListEntry] = []


class URLAllowList(PolicyListBase):
    type: Literal["urlWhiteList"] = "urlWhiteList"
    entries: List[URLListEntry] = []


class URLBlockList(PolicyListBase):
    type: Literal["urlBlackList"] = "urlBlackList"
    entries: List[URLListEntry] = []


class _CommunityListBase(PolicyListBase):
    entries: List[CommunityListEntry] = []

    def add_well_known_community(self, community: WellKnownBGPCommunities) -> None:
        self._add_entry(CommunityListEntry(community=community))

    def add_community(self, as_number: int, community_number: int) -> None:
        self._add_entry(CommunityListEntry(community=f"{as_number}:{community_number}"))


class CommunityList(_CommunityListBase):
    type: Literal["community"] = "community"


class ExpandedCommunityList(_CommunityListBase):
    type: Literal["expandedCommunity"] = "expandedCommunity"


class PolicerList(PolicyListBase):
    type: Literal["policer"] = "policer"
    entries: List[PolicerListEntry] = []

    def police(self, burst: int, rate: int, exceed: PolicerExceedAction = "drop") -> None:
        # Policer list must have only single entry!
        entry = PolicerListEntry(burst=str(burst), exceed=exceed, rate=str(rate))
        self._add_entry(entry, single=True)


class ASPathList(PolicyListBase):
    type: Literal["asPath"] = "asPath"
    entries: List[ASPathListEntry] = []


class ClassMapList(PolicyListBase):
    type: Literal["class"] = "class"
    entries: List[ClassMapListEntry] = []

    def assign_queue(self, queue: int) -> None:
        # Class map list must have only one entry!
        entry = ClassMapListEntry(queue=str(queue))
        self._add_entry(entry, single=True)


class MirrorList(PolicyListBase):
    type: Literal["mirror"] = "mirror"
    entries: List[MirrorListEntry] = []


class AppProbeClassList(PolicyListBase):
    type: Literal["appProbe"] = "appProbe"
    entries: List[AppProbeClassListEntry] = []

    def assign_forwarding_class(self, name: str) -> AppProbeClassListEntry:
        # App probe class list must have only one entry!
        entry = AppProbeClassListEntry(forwarding_class=name)
        self._add_entry(entry, single=True)
        return entry


class SLAClassList(PolicyListBase):
    type: Literal["sla"] = "sla"
    entries: List[SLAClassListEntry] = []

    def assign_app_probe_class(
        self,
        app_probe_class_id: UUID,
        latency: Optional[int] = None,
        loss: Optional[int] = None,
        jitter: Optional[int] = None,
    ) -> SLAClassListEntry:
        # SLA class list must have only one entry!
        _latency = str(latency) if latency is not None else None
        _loss = str(loss) if loss is not None else None
        _jitter = str(jitter) if jitter is not None else None
        entry = SLAClassListEntry(latency=_latency, loss=_loss, jitter=_jitter, app_probe_class=app_probe_class_id)
        self._add_entry(entry, single=True)
        return entry

    def add_fallback_jitter_criteria(self, jitter_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_jitter_criteria(jitter_variance)

    def add_fallback_latency_criteria(self, latency_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_latency_criteria(latency_variance)

    def add_fallback_loss_criteria(self, loss_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_loss_criteria(loss_variance)


class TLOCList(PolicyListBase):
    type: Literal["tloc"] = "tloc"
    entries: List[TLOCListEntry] = []

    def add_tloc(self, tloc: IPv4Address, color: TLOCColor, encap: EncapType, preference: Optional[int] = None) -> None:
        _preference = str(preference) if preference is not None else None
        self.entries.append(TLOCListEntry(tloc=tloc, color=color, encap=encap, preference=_preference))


class PreferredColorGroupList(PolicyListBase):
    type: Literal["preferredColorGroup"] = "preferredColorGroup"
    entries: List[PreferredColorGroupListEntry] = []

    def assign_color_groups(
        self,
        primary: Tuple[Set[TLOCColor], PathPreference],
        secondary: Optional[Tuple[Set[TLOCColor], PathPreference]] = None,
        tertiary: Optional[Tuple[Set[TLOCColor], PathPreference]] = None,
    ) -> PreferredColorGroupListEntry:
        primary_preference = ColorGroupPreference.from_color_set_and_path(*primary)
        secondary_preference = (
            ColorGroupPreference.from_color_set_and_path(*secondary) if secondary is not None else None
        )
        tertiary_preference = ColorGroupPreference.from_color_set_and_path(*tertiary) if tertiary is not None else None
        entry = PreferredColorGroupListEntry(
            primary_preference=primary_preference,
            secondary_preference=secondary_preference,
            tertiary_preference=tertiary_preference,
        )
        if self.entries:
            self.entries[0] = entry
        else:
            self.entries.append(entry)
        return entry


class PrefixList(PolicyListBase):
    type: Literal["prefix"] = "prefix"
    entries: List[PrefixListEntry] = []

    def add_prefix(self, prefix: IPv4Network, ge: Optional[int] = None, le: Optional[int] = None) -> None:
        _ge = str(ge) if ge is not None else None
        _le = str(le) if le is not None else None
        self._add_entry(PrefixListEntry(ip_prefix=prefix, ge=_ge, le=_le))


class IPv6PrefixList(PolicyListBase):
    type: Literal["ipv6prefix"] = "ipv6prefix"
    entries: List[IPv6PrefixListEntry] = []


class RegionList(PolicyListBase):
    type: Literal["region"] = "region"
    entries: List[RegionListEntry] = []

    def add_regions(self, regions: Set[int]):
        for region in regions:
            self._add_entry(RegionListEntry(region_id=str(region)))

    def add_region_range(self, region_range: Tuple[int, int]):
        entry = RegionListEntry(region_id=f"{region_range[0]}-{region_range[1]}")
        self._add_entry(entry)
