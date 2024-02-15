import logging
import sys
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network, IPv6Address
from typing import Any, List, Optional, Tuple

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.models.common import InterfaceTypeEnum, TLOCColorEnum, WellKnownBGPCommunitiesEnum
from catalystwan.models.configuration.feature_profile.common import FeatureProfileInfo, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.interest_groups import (
    ApplicationListEntry,
    ApplicationListParcel,
    AppProbeEntry,
    AppProbeMapItem,
    AppProbeParcel,
    ColorEntry,
    ColorParcel,
    DataPrefixEntry,
    DataPrefixParcel,
    ExpandedCommunityParcel,
    FallbackBestTunnel,
    FowardingClassParcel,
    FowardingClassQueueEntry,
    FQDNDomainParcel,
    FQDNListEntry,
    GeoLocationListEntry,
    GeoLocationListParcel,
    IPSSignatureListEntry,
    IPSSignatureParcel,
    IPv6DataPrefixEntry,
    IPv6DataPrefixParcel,
    IPv6PrefixListEntry,
    IPv6PrefixListParcel,
    LocalDomainListEntry,
    LocalDomainParcel,
    PolicierEntry,
    PolicierParcel,
    Preference,
    PreferredColorGroupEntry,
    PreferredColorGroupParcel,
    PrefixListEntry,
    PrefixListParcel,
    ProtocolListEntry,
    ProtocolListParcel,
    ProtocolTypeEnum,
    SecurityApplicationFamilyListEntry,
    SecurityApplicationListEntry,
    SecurityApplicationListParcel,
    SecurityDataPrefixEntry,
    SecurityDataPrefixParcel,
    SecurityPortListEntry,
    SecurityPortParcel,
    SecurityZoneListEntry,
    SecurityZoneListParcel,
    SLAAppProbeClass,
    SLAClassCriteriaEnum,
    SLAClassListEntry,
    SLAClassParcel,
    StandardCommunityEntry,
    StandardCommunityParcel,
    TlocEntry,
    TlocParcel,
    URLAllowListEntry,
    URLAllowParcel,
    URLBlockListEntry,
    URLBlockParcel,
)
from catalystwan.models.policy.lists_entries import EncapEnum, PathPreferenceEnum, PolicerExceedActionEnum

logger = logging.getLogger(__name__)

PROFILE_NAME = "Default_Policy_Object_Profile"


@dataclass
class CmdArguments:
    url: str
    port: int
    user: str
    password: str
    device_template: Optional[str] = None


def configure_groups_of_interest(profile: FeatureProfileInfo, api: PolicyObjectFeatureProfileAPI):
    items: List[Any] = []
    items_ids: List[Tuple[ParcelCreationResponse, Any]] = []

    # Security Groups
    fqdn = FQDNDomainParcel(
        parcel_name="FQDNDomainParcelExmaple",
        entries=[FQDNListEntry(pattern=as_global("www.cisco.com")), FQDNListEntry(pattern=as_global("www.aws.com"))],
    )
    local_domain = LocalDomainParcel(
        parcel_name="LocalDomainParcelExample", entries=[LocalDomainListEntry(name_server=as_global("www.google.com"))]
    )
    ips_signature = IPSSignatureParcel(
        parcel_name="IPSSignatureParcelExample",
        entries=[IPSSignatureListEntry(generator_id=as_global("30"), signature_id=as_global("1000"))],
    )
    url_allowed = URLAllowParcel(
        parcel_name="URLAllowParcelExample", entries=[URLAllowListEntry(pattern=as_global("https://www.cisco.com/"))]
    )
    url_blocked = URLBlockParcel(
        parcel_name="URLBlockParcelExample", entries=[URLBlockListEntry(pattern=as_global("https://www.example.com/"))]
    )
    security_port = SecurityPortParcel(
        parcel_name="SecurityPortParcelExmaple",
        entries=[
            SecurityPortListEntry(port=as_global("10")),
            SecurityPortListEntry(port=as_global("50-100")),
            SecurityPortListEntry(port=as_global("400-999")),
        ],
    )
    geolocation = GeoLocationListParcel(
        parcel_name="GeoLocationListParcelExample",
        entries=[
            GeoLocationListEntry(country=as_global("BVT")),
            GeoLocationListEntry(country=as_global("ATA")),
            GeoLocationListEntry(continent=as_global("AF")),
        ],
    )
    security_zone = SecurityZoneListParcel(
        parcel_name="SecurityZoneListParcel",
        entries=[
            SecurityZoneListEntry(interface=as_global(InterfaceTypeEnum.FAST_ETHERNET)),
            SecurityZoneListEntry(interface=as_global(InterfaceTypeEnum.FIVE_GIGABIT_ETHERNET)),
        ],
    )
    security_application_list = SecurityApplicationListParcel(
        parcel_name="SecurityApplListParcelExample",
        entries=[
            SecurityApplicationFamilyListEntry(app_list_family=as_global("app-fam-2")),
            SecurityApplicationListEntry(app_list=as_global("msn-messenger-ft")),
            SecurityApplicationListEntry(app_list=as_global("aol-messenger")),
        ],
    )
    security_data_prefix_parcel = SecurityDataPrefixParcel(
        parcel_name="SecurityDataPrefixExample",
        entries=[
            SecurityDataPrefixEntry(ip_prefix=as_global(IPv4Network("10.0.0.0/16"))),
            SecurityDataPrefixEntry(ip_prefix=as_global(IPv4Network("30.0.0.0/16"))),
            SecurityDataPrefixEntry(ip_prefix=as_global(IPv4Network("50.0.0.0/16"))),
        ],
    )
    protocol_list = ProtocolListParcel(
        parcel_name="ProtocolListParcelExample",
        entries=[
            ProtocolListEntry(protocol=as_global(ProtocolTypeEnum.APPLEQTC)),
            ProtocolListEntry(protocol=as_global(ProtocolTypeEnum.CISCO_SVCS)),
            ProtocolListEntry(protocol=as_global(ProtocolTypeEnum.CDDBP)),
            ProtocolListEntry(protocol=as_global(ProtocolTypeEnum.EXEC)),
            ProtocolListEntry(protocol=as_global(ProtocolTypeEnum.HSRP)),
        ],
    )

    # Policy Groups
    color_parcel = ColorParcel(
        parcel_name="ColorParcelExample",
        entries=[ColorEntry(color=as_global(TLOCColorEnum.LTE)), ColorEntry(color=as_global(TLOCColorEnum.GREEN))],
    )
    data_prefix_parcel = DataPrefixParcel(
        parcel_name="DataPrefixExample",
        entries=[DataPrefixEntry(ipv4_address=as_global(IPv4Address("10.0.0.0")), ipv4_prefix_length=as_global(16))],
    )
    prefix_list_parcel = PrefixListParcel(
        parcel_name="PrefixListExample",
        entries=[PrefixListEntry(ipv4_address=as_global(IPv4Address("10.0.0.0")), ipv4_prefix_length=as_global(16))],
    )
    ipv6_data_prefix = IPv6DataPrefixParcel(
        parcel_name="IPv6DataPrefixExample",
        entries=[
            IPv6DataPrefixEntry(ipv6_address=as_global(IPv6Address("2000:0:0:0::")), ipv6_prefix_length=as_global(32))
        ],
    )
    ipv6_prefix_list = IPv6PrefixListParcel(
        parcel_name="IPv6PrefixListExample",
        entries=[
            IPv6PrefixListEntry(ipv6_address=as_global(IPv6Address("2000:0:0:0::")), ipv6_prefix_length=as_global(32))
        ],
    )
    application_list_parcel = ApplicationListParcel(
        parcel_name="AppListExample",
        entries=[
            ApplicationListEntry(app_list=as_global("3com-amp3")),
            ApplicationListEntry(app_list=as_global("sugarcrm")),
        ],
    )
    preferred_group_color = PreferredColorGroupParcel(
        parcel_name="PreferredColorGroupParcelExmaple",
        entries=[
            PreferredColorGroupEntry(
                primary_preference=Preference(
                    color_preference=as_global([TLOCColorEnum.BIZ_INTERNET, TLOCColorEnum.MPLS]),
                    path_preference=as_global(PathPreferenceEnum.DIRECT_PATH),
                ),
                secondary_preference=Preference(
                    color_preference=as_global([TLOCColorEnum.BRONZE]),
                    path_preference=as_global(PathPreferenceEnum.DIRECT_PATH),
                ),
                tertiary_preference=Preference(
                    color_preference=as_global([TLOCColorEnum.METRO_ETHERNET]),
                    path_preference=as_global(PathPreferenceEnum.MULTI_HOP_PATH),
                ),
            )
        ],
    )
    policier = PolicierParcel(
        parcel_name="PolicierParcelExmaple",
        entries=[
            PolicierEntry(burst=as_global(17000), exceed=as_global(PolicerExceedActionEnum.DROP), rate=as_global(1000))
        ],
    )
    fowarding_class = FowardingClassParcel(
        parcel_name="FowardingClassParcelExmaple", entries=[FowardingClassQueueEntry(queue=as_global("4"))]
    )
    tloc_list = TlocParcel(
        parcel_name="TlocParcelExample",
        entries=[
            TlocEntry(
                tloc=as_global(IPv4Address("20.0.0.0")),
                color=as_global(TLOCColorEnum.PRIVATE3),
                encapsulation=as_global(EncapEnum.GRE),
                preference=as_global("1000"),
            ),
            TlocEntry(
                tloc=as_global(IPv4Address("30.0.0.0")),
                color=as_global(TLOCColorEnum.CUSTOM1),
                encapsulation=as_global(EncapEnum.GRE),
                preference=as_global("10000"),
            ),
        ],
    )
    standard_community = StandardCommunityParcel(
        parcel_name="StandardCommunityParcelExample",
        entries=[
            StandardCommunityEntry(standard_community=as_global(WellKnownBGPCommunitiesEnum.LOCAL_AS)),
            StandardCommunityEntry(standard_community=as_global(WellKnownBGPCommunitiesEnum.NO_ADVERTISE)),
        ],
    )
    expanded_community = ExpandedCommunityParcel(
        parcel_name="ExpandedCommunityParcel",
        expandedCommunityList=as_global(["CommunityList", "CommunityList2", "CommunityList3"]),
    )
    app_probe = AppProbeParcel(
        parcel_name="AppProbeParcelExample",
        entries=[
            AppProbeEntry(
                forwarding_class_name=as_global("FowardingClassParcelExmaple"),
                map=[
                    AppProbeMapItem(color=as_global(TLOCColorEnum.CUSTOM1), dscp=as_global(33)),
                    AppProbeMapItem(color=as_global(TLOCColorEnum.BLUE), dscp=as_global(40)),
                    AppProbeMapItem(color=as_global(TLOCColorEnum.PUBLIC_INTERNET), dscp=as_global(43)),
                ],
            )
        ],
    )

    items.append(fqdn)
    items.append(local_domain)
    items.append(ips_signature)
    items.append(url_allowed)
    items.append(url_blocked)
    items.append(security_port)
    items.append(geolocation)
    items.append(security_zone)
    items.append(security_application_list)
    items.append(security_data_prefix_parcel)
    items.append(protocol_list)
    items.append(color_parcel)
    items.append(data_prefix_parcel)
    items.append(ipv6_data_prefix)
    items.append(application_list_parcel)
    items.append(prefix_list_parcel)
    items.append(ipv6_prefix_list)
    items.append(preferred_group_color)
    items.append(policier)
    items.append(fowarding_class)
    items.append(tloc_list)
    items.append(standard_community)
    items.append(expanded_community)
    items.append(app_probe)

    for item in items:
        print(item.model_dump_json(by_alias=True, indent=4))

    for item in items:
        items_ids.append((api.create(profile, item), item.__class__))

    _id, _ = items_ids[-1]

    sla = SLAClassParcel(
        parcel_name="SLAClassParcelExample",
        entries=[
            SLAClassListEntry(
                app_probe_class=SLAAppProbeClass(ref_id=as_global(_id.id)),
                jitter=as_global(20),
                latency=as_global(50),
                loss=as_global(100),
                fallback_best_tunnel=FallbackBestTunnel(
                    criteria=as_global(SLAClassCriteriaEnum.JITTER_LOSS_LATENCY),
                    jitter_variance=as_global(10),
                    latency_variance=as_global(10),
                    loss_variance=as_global(10),
                ),
            )
        ],
    )

    items_ids.append((api.create(profile, sla), sla.__class__))

    input("Press enter to delete...")

    for _id, item_type in reversed(items_ids):
        api.delete(profile, item_type, _id.id)


def retrive_groups_of_interest(profile: FeatureProfileInfo, api: PolicyObjectFeatureProfileAPI):
    print(api.get(profile, ApplicationListParcel))  # Get all Application List Parcels


def run_demo(args: CmdArguments):
    from catalystwan.session import create_manager_session

    with create_manager_session(
        url=args.url, port=args.port, username=args.user, password=args.password, logger=logger
    ) as session:
        api = PolicyObjectFeatureProfileAPI(session)
        profile = (
            ConfigurationFeatureProfile(session)
            .get_sdwan_feature_profiles()
            .filter(profile_name=PROFILE_NAME)
            .single_or_default()
        )
        configure_groups_of_interest(profile, api)
        retrive_groups_of_interest(profile, api)


def load_arguments() -> CmdArguments:
    url = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    return CmdArguments(url, int(port), user, password)


if __name__ == "__main__":
    arguments = load_arguments()
    run_demo(arguments)
