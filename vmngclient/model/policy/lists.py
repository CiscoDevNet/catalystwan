from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.model.policy.lists_entries import (
    DataPrefixListEntry,
    FQDNListEntry,
    GeoLocationListEntry,
    LocalAppListEntry,
    PortListEntry,
    ProtocolNameListEntry,
    SiteListEntry,
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
    entries: List


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
    ],
    Field(discriminator="type"),
]
