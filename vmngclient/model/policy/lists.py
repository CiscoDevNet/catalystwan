from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.model.policy.lists_entries import (
    AppListEntry,
    ASPathListEntry,
    ColorListEntry,
    CommunityListEntry,
    DataIPv6PrefixListEntry,
    DataPrefixListEntry,
    FQDNListEntry,
    GeoLocationListEntry,
    IPSSignatureListEntry,
    LocalAppListEntry,
    LocalDomainListEntry,
    PolicerListEntry,
    PortListEntry,
    ProtocolNameListEntry,
    SiteListEntry,
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
    ],
    Field(discriminator="type"),
]
