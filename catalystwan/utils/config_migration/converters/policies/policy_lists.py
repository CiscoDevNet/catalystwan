from typing import Any, Callable, Dict, List, Mapping, NamedTuple, Optional, Sequence, Type

from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AnyPolicyObjectParcel,
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
    PolicierParcel,
    PreferredColorGroupParcel,
    PrefixListParcel,
    ProtocolListParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    SLAClassParcel,
    StandardCommunityParcel,
    TlocParcel,
    URLAllowParcel,
    URLBlockParcel,
)
from catalystwan.models.policy import (
    AnyPolicyList,
    AppList,
    AppProbeClassList,
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
    LocalDomainList,
    PolicerList,
    PortList,
    PreferredColorGroupList,
    PrefixList,
    ProtocolNameList,
    SLAClassList,
    TLOCList,
    URLAllowList,
    URLBlockList,
    ZoneList,
)


def _get_parcel_name_desc(policy_list: AnyPolicyList) -> Dict[str, Any]:
    return dict(parcel_name=policy_list.name, parcel_description=policy_list.description)


def app_probe(in_: AppProbeClassList) -> AppProbeParcel:
    out = AppProbeParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_fowarding_class(entry.forwarding_class)
    return out


def app_list(in_: AppList) -> ApplicationListParcel:
    out = ApplicationListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.app is not None:
            out.add_application(entry.app)
        if entry.app_family is not None:
            out.add_application_family(entry.app_family)
    return out


# TODO: def as_path(in_: ASPathList):


def class_map(in_: ClassMapList) -> FowardingClassParcel:
    out = FowardingClassParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_queue(entry.queue)
    return out


def color(in_: ColorList) -> ColorParcel:
    out = ColorParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_color(entry.color)
    return out


def community(in_: CommunityList) -> StandardCommunityParcel:
    out = StandardCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_community(entry.community)
    return out


def data_prefix_ipv6(in_: DataIPv6PrefixList) -> IPv6DataPrefixParcel:
    out = IPv6DataPrefixParcel(**_get_parcel_name_desc(in_))
    return out


def data_prefix(in_: DataPrefixList) -> DataPrefixParcel:
    out = DataPrefixParcel(**_get_parcel_name_desc(in_))
    return out


def expanded_community(in_: ExpandedCommunityList) -> ExpandedCommunityParcel:
    out = ExpandedCommunityParcel(**_get_parcel_name_desc(in_))
    return out


def fqdn(in_: FQDNList) -> FQDNDomainParcel:
    out = FQDNDomainParcel(**_get_parcel_name_desc(in_))
    return out


def geo_location(in_: GeoLocationList) -> GeoLocationListParcel:
    out = GeoLocationListParcel(**_get_parcel_name_desc(in_))
    return out


def ips_signature(in_: IPSSignatureList) -> IPSSignatureParcel:
    out = IPSSignatureParcel(**_get_parcel_name_desc(in_))
    return out


def prefix_ipv6(in_: IPv6PrefixList) -> IPv6PrefixListParcel:
    out = IPv6PrefixListParcel(**_get_parcel_name_desc(in_))
    return out


# TODO: def local_app(in_: LocalAppList):
def local_domain(in_: LocalDomainList) -> LocalDomainParcel:
    out = LocalDomainParcel(**_get_parcel_name_desc(in_))
    return out


# TODO: def mirror_list(in_: MirrorList):
def policer(in_: PolicerList) -> PolicierParcel:
    out = PolicierParcel(**_get_parcel_name_desc(in_))
    return out


def port(in_: PortList) -> SecurityPortParcel:
    out = SecurityPortParcel(**_get_parcel_name_desc(in_))
    return out


def preferred_color_group(in_: PreferredColorGroupList) -> PreferredColorGroupParcel:
    out = PreferredColorGroupParcel(**_get_parcel_name_desc(in_))
    return out


def prefix(in_: PrefixList) -> PrefixListParcel:
    out = PrefixListParcel(**_get_parcel_name_desc(in_))
    return out


def protocol(in_: ProtocolNameList) -> ProtocolListParcel:
    out = ProtocolListParcel(**_get_parcel_name_desc(in_))
    return out


# TODO: def region(in_: RegionList):
# TODO: def site(in_: SiteList):
def sla_class(in_: SLAClassList) -> SLAClassParcel:
    out = SLAClassParcel(**_get_parcel_name_desc(in_))
    return out


def tloc(in_: TLOCList) -> TlocParcel:
    out = TlocParcel(**_get_parcel_name_desc(in_))
    return out


def url_allow(in_: URLAllowList) -> URLAllowParcel:
    out = URLAllowParcel(**_get_parcel_name_desc(in_))
    return out


def url_block(in_: URLBlockList) -> URLBlockParcel:
    out = URLBlockParcel(**_get_parcel_name_desc(in_))
    return out


# TODO: def vpn(in_: VPNList):
def zone(in_: ZoneList) -> SecurityZoneListParcel:
    out = SecurityZoneListParcel(**_get_parcel_name_desc(in_))
    return out


Input = AnyPolicyList
Output = AnyPolicyObjectParcel


class ConvertAllResult(NamedTuple):
    output: List[Output] = []
    left: List[Input] = []


CONVERTERS: Mapping[Type[Input], Callable[[Any], Output]] = {
    AppProbeClassList: app_probe,
    AppList: app_list,
    ClassMapList: class_map,
    ColorList: color,
    CommunityList: community,
    DataIPv6PrefixList: data_prefix_ipv6,
    DataPrefixList: data_prefix,
    ExpandedCommunityList: expanded_community,
    FQDNList: fqdn,
    GeoLocationList: geo_location,
    IPSSignatureList: ips_signature,
    IPv6PrefixList: prefix_ipv6,
    LocalDomainList: local_domain,
    PolicerList: policer,
    PortList: port,
    PreferredColorGroupList: preferred_color_group,
    PrefixList: prefix,
    ProtocolNameList: protocol,
    SLAClassList: sla_class,
    TLOCList: tloc,
    URLAllowList: url_allow,
    URLBlockList: url_block,
    ZoneList: zone,
}


def convert(in_: Input) -> Optional[Output]:
    if converter := CONVERTERS.get(type(in_)):
        return converter(in_)
    return None


def convert_all(inputs: Sequence[Input]) -> ConvertAllResult:
    result = ConvertAllResult()
    for i in inputs:
        if (output := convert(i)) and output is not None:
            result.output.append(output)
        else:
            result.left.append(i)
    return result
