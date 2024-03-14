# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import Any, List, Literal, Optional, Set, Tuple
from uuid import UUID

from pydantic import BaseModel, Field

from catalystwan.models.common import InterfaceType, TLOCColor
from catalystwan.models.policy.lists_entries import (
    EncapType,
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
            self._add_entry(VPNListEntry(vpn=(vpn, None)))

    def add_vpn_range(self, vpn_range: Tuple[int, int]):
        self._add_entry(VPNListEntry(vpn=vpn_range))


class ZoneList(PolicyListBase):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=(vpn, None)) for vpn in vpns]

    def assign_interfaces(self, ifs: Set[InterfaceType]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]


class ProtocolNameList(PolicyListBase):
    type: Literal["protocolName"] = "protocolName"
    entries: List[ProtocolNameListEntry] = []


class URLAllowList(PolicyListBase):
    type: Literal["urlWhiteList"] = "urlWhiteList"
    entries: List[URLListEntry] = []


class URLBlockList(PolicyListBase):
    type: Literal["urlBlackList"] = "urlBlackList"
    entries: List[URLListEntry] = []


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


class RegionList(PolicyListBase):
    type: Literal["region"] = "region"
    entries: List[RegionListEntry] = []

    def add_regions(self, regions: Set[int]):
        for region in regions:
            self._add_entry(RegionListEntry(region_id=str(region)))

    def add_region_range(self, region_range: Tuple[int, int]):
        entry = RegionListEntry(region_id=f"{region_range[0]}-{region_range[1]}")
        self._add_entry(entry)
