from typing import Any, Callable, Dict, List, Mapping, NamedTuple, Optional, Sequence, Type

from catalystwan.models.common import int_range_serializer
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
    PolicerParcel,
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
    for entry in in_.entries:
        out.add_prefix(entry.ipv6_prefix)
    return out


def data_prefix(in_: DataPrefixList) -> DataPrefixParcel:
    out = DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_data_prefix(entry.ip_prefix)
    return out


def expanded_community(in_: ExpandedCommunityList) -> ExpandedCommunityParcel:
    out = ExpandedCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_community(entry.community)
    return out


def fqdn(in_: FQDNList) -> FQDNDomainParcel:
    out = FQDNDomainParcel(**_get_parcel_name_desc(in_))
    out.from_fqdns([entry.pattern for entry in in_.entries])
    return out


def geo_location(in_: GeoLocationList) -> GeoLocationListParcel:
    out = GeoLocationListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.country is not None:
            out.add_country(entry.country)
        if entry.continent is not None:
            out.add_continent(entry.continent)
    return out


def ips_signature(in_: IPSSignatureList) -> IPSSignatureParcel:
    out = IPSSignatureParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_signature(f"{entry.generator_id}:{entry.signature_id}")
    return out


def prefix_ipv6(in_: IPv6PrefixList) -> IPv6PrefixListParcel:
    out = IPv6PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(ipv6_network=entry.ipv6_prefix, ge=entry.ge, le=entry.le)
    return out


# TODO: def local_app(in_: LocalAppList):
def local_domain(in_: LocalDomainList) -> LocalDomainParcel:
    out = LocalDomainParcel(**_get_parcel_name_desc(in_))
    out.from_local_domains([entry.name_server for entry in in_.entries])
    return out


# TODO: def mirror_list(in_: MirrorList):
def policer(in_: PolicerList) -> PolicerParcel:
    out = PolicerParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_entry(burst=entry.burst, exceed=entry.exceed, rate=entry.rate)
    return out


def port(in_: PortList) -> SecurityPortParcel:
    out = SecurityPortParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_port(int_range_serializer(entry.port))
    return out


def preferred_color_group(in_: PreferredColorGroupList) -> PreferredColorGroupParcel:
    out = PreferredColorGroupParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_primary(
            color_preference=list(entry.primary_preference.color_preference),
            path_preference=entry.primary_preference.path_preference,
        )
        if entry.secondary_preference is not None:
            out.add_secondary(
                color_preference=list(entry.secondary_preference.color_preference),
                path_preference=entry.secondary_preference.path_preference,
            )
        if entry.tertiary_preference is not None:
            out.add_tertiary(
                color_preference=list(entry.tertiary_preference.color_preference),
                path_preference=entry.tertiary_preference.path_preference,
            )
    return out


def prefix(in_: PrefixList) -> PrefixListParcel:
    out = PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ip_prefix)
    return out


def protocol(in_: ProtocolNameList) -> ProtocolListParcel:
    out = ProtocolListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_protocol(entry.protocol_name)
    return out


# TODO: def region(in_: RegionList):
# TODO: def site(in_: SiteList):
def sla_class(in_: SLAClassList) -> SLAClassParcel:
    out = SLAClassParcel(**_get_parcel_name_desc(in_))
    # TODO: requires app probe id
    return out


def tloc(in_: TLOCList) -> TlocParcel:
    out = TlocParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        _preference = str(entry.preference) if entry.preference is not None else None
        out.add_entry(tloc=entry.tloc, color=entry.color, encapsulation=entry.encap, preference=_preference)
    return out


def url_allow(in_: URLAllowList) -> URLAllowParcel:
    out = URLAllowParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return out


def url_block(in_: URLBlockList) -> URLBlockParcel:
    out = URLBlockParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return out


# TODO: def vpn(in_: VPNList): needs to be converted to item from service profile
def zone(in_: ZoneList) -> SecurityZoneListParcel:
    out = SecurityZoneListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.interface is not None:
            out.add_interface(entry.interface)
        if entry.vpn is not None:
            out.add_vpn(int_range_serializer(entry.vpn))
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


def _find_converter(in_: Input) -> Optional[Callable[[Any], Output]]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    return None


def convert(in_: Input) -> Optional[Output]:
    if converter := _find_converter(in_):
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
