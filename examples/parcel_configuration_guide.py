import logging
import sys
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network, IPv6Network
from typing import Any, List, Optional, Tuple

from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.models.common import InterfaceTypeEnum, TLOCColorEnum, WellKnownBGPCommunitiesEnum
from catalystwan.models.configuration.feature_profile.common import FeatureProfileInfo, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.interest_groups import (
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
    ProtocolTypeEnum,
    SecurityApplicationListParcel,
    SecurityDataPrefixParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    SLAClassCriteriaEnum,
    SLAClassParcel,
    StandardCommunityParcel,
    TlocParcel,
    URLAllowParcel,
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
    """
    This function creates various policy objects such as
        FQDN,
        Local Domain,
        IPS Signature,
        Allowed URL,
        Blocked URL,
        Security Port,
        Geolocation,
        Security Zone,
        Security Application List,
        Security Data Prefix,
        Protocol,
        Color,
        Data Prefix,
        IPv6 Data Prefix,
        Application Family,
        Preferred Color Group,
        Policier,
        Fowarding Class,
        Tloc,
        Standard Community,
        Expanded Community,
        App Probe, and
        SLA Class.

    Args:
        profile (FeatureProfileInfo): The feature profile to which the policy objects are to be added.
        api (PolicyObjectFeatureProfileAPI): The API object used to create and delete the policy objects.

    Returns:
        None: This function does not return any additional values.
    """
    items: List[Any] = []
    items_ids: List[Tuple[ParcelCreationResponse, Any]] = []

    # Security Groups

    # Create FQDN parcel and add FQDNs
    fqdn = FQDNDomainParcel(parcel_name="FQDNDomainParcelExmaple")
    fqdn.add_fqdn("www.cisco.com")
    fqdn.add_fqdn("www.aws.com")
    fqdn.add_fqdn("www.youtube.com")

    # Create Local Domain parcel and add Local Domains
    local_domain = LocalDomainParcel(parcel_name="LocalDomainParcelExample")
    local_domain.add_local_domain("www.google.com")
    local_domain.add_local_domain("www.ciscodevnet.com")

    # Create IPS Signature parcel and add signatures
    ips_signature = IPSSignatureParcel(parcel_name="IPSSignatureParcelExample")
    ips_signature.add_signature("30:1000")
    ips_signature.add_signature("60:3000")

    # Create Allowed URL parcel and add URLs
    url_allowed = URLAllowParcel(parcel_name="URLAllowParcelExample")
    url_allowed.add_url("https://www.cisco.com/")
    url_allowed.add_url("https://www.test.com/")

    # Create Blocked URL parcel and add URLs
    url_blocked = URLBlockParcel(parcel_name="URLBlockParcelExample")
    url_blocked.add_url("https://www.example.com/")

    # Create security port parcel and add ports
    security_port = SecurityPortParcel(parcel_name="SecurityPortParcelExmaple")
    security_port.add_port("10")
    security_port.add_port("50-100")
    security_port.add_port("400-999")

    # Create Geolocation parcel and add geolocations
    geolocation = GeoLocationListParcel(parcel_name="GeoLocationListParcelExample")
    geolocation.add_continent("AF")
    geolocation.add_country("BVT")
    geolocation.add_country("ATA")

    # Create Security Zone parcel and add interfaces
    security_zone = SecurityZoneListParcel(parcel_name="SecurityZoneListParcel")
    security_zone.add_interface(InterfaceTypeEnum.ETHERNET)
    security_zone.add_interface(InterfaceTypeEnum.TUNNEL)

    # Create Application parcel and add applications
    security_application_list = SecurityApplicationListParcel(parcel_name="SecurityApplListParcelExample")
    security_application_list.add_application("msn-messenger-ft")
    security_application_list.add_application("aol-messenger")
    security_application_list.add_application_family("app-fam-2")

    # Create Security data prefix parcel and add data prefixes
    security_data_prefix_parcel = SecurityDataPrefixParcel(parcel_name="SecurityDataPrefixExample")
    security_data_prefix_parcel.add_prefix(IPv4Network("10.0.0.0/16"))
    security_data_prefix_parcel.add_prefix(IPv4Network("30.0.0.0/16"))
    security_data_prefix_parcel.add_prefix(IPv4Network("50.0.0.0/16"))
    security_data_prefix_parcel.add_prefix(IPv4Network("60.0.0.0/16"))

    # Create Protocol parcel and add protocols
    protocol_list = ProtocolListParcel(parcel_name="ProtocolListParcelExample")
    protocol_list.add_protocol(ProtocolTypeEnum.EXEC)
    protocol_list.add_protocol(ProtocolTypeEnum.H323)
    protocol_list.add_protocol(ProtocolTypeEnum.BOOTPS)
    protocol_list.add_protocol(ProtocolTypeEnum.ACE_SVR)
    protocol_list.add_protocol(ProtocolTypeEnum.CISCO_SVCS)
    protocol_list.add_protocol(ProtocolTypeEnum.NTP)
    protocol_list.add_protocol(ProtocolTypeEnum.BOOTPC)

    # Policy Groups

    # Create Color parcel and add colors
    color_parcel = ColorParcel(parcel_name="ColorParcelExample")
    color_parcel.add_color(TLOCColorEnum.BIZ_INTERNET)
    color_parcel.add_color(TLOCColorEnum.METRO_ETHERNET)
    color_parcel.add_color(TLOCColorEnum.PUBLIC_INTERNET)

    # Create Data prefix parcel and add data prefixes
    data_prefix_parcel = DataPrefixParcel(parcel_name="DataPrefixExample")
    data_prefix_parcel.add_data_prefix(IPv4Network("10.0.0.0/16"))
    data_prefix_parcel.add_data_prefix(IPv4Network("50.0.0.0/32"))

    # Create Prefix parcel and add prefixes
    prefix_list_parcel = PrefixListParcel(parcel_name="PrefixListExample")
    prefix_list_parcel.add_prefix(IPv4Network("10.0.0.0/16"))
    prefix_list_parcel.add_prefix(IPv4Network("50.0.0.0/32"))

    # Create IPv6 data prefix parcel and add IPv6 prefixes
    ipv6_data_prefix = IPv6DataPrefixParcel(parcel_name="IPv6DataPrefixExample")
    ipv6_data_prefix.add_prefix(IPv6Network("2000:0:0:0::/128"))
    ipv6_data_prefix.add_prefix(IPv6Network("2001:0:0:0::/128"))
    ipv6_data_prefix.add_prefix(IPv6Network("2002:0:0:0::/128"))

    # Create IPv6 prefix parcel and add IPv6 prefixes
    ipv6_prefix_list = IPv6PrefixListParcel(parcel_name="IPv6PrefixListExample")
    ipv6_prefix_list.add_prefix(IPv6Network("2000:0:0:0::/64"))
    ipv6_prefix_list.add_prefix(IPv6Network("2001:0:0:0::/64"))
    ipv6_prefix_list.add_prefix(IPv6Network("2002:0:0:0::/64"))

    # Create Application family parcel and add application families
    application_list_parcel = ApplicationListParcel(parcel_name="AppListExample")
    application_list_parcel.add_application_family("app-fam-2")
    application_list_parcel.add_application_family("sugarcrm")

    # Create Preferred color parcel and add preferred colors
    preferred_group_color = PreferredColorGroupParcel(parcel_name="PreferredColorGroupParcelExmaple")
    preferred_group_color.add_primary(
        color_preference=[TLOCColorEnum.BIZ_INTERNET, TLOCColorEnum.MPLS],
        path_preference=PathPreferenceEnum.DIRECT_PATH,
    )
    preferred_group_color.add_secondary(
        color_preference=[TLOCColorEnum.BRONZE, TLOCColorEnum.SILVER], path_preference=PathPreferenceEnum.DIRECT_PATH
    )
    preferred_group_color.add_tertiary(
        color_preference=[TLOCColorEnum.METRO_ETHERNET], path_preference=PathPreferenceEnum.MULTI_HOP_PATH
    )

    # Create Policier parcel and add policiers
    policier = PolicierParcel(parcel_name="PolicierParcelExmaple")
    policier.add_entry(burst=17000, exceed=PolicerExceedActionEnum.DROP, rate=1000)

    # Create Fowarding Class parcel and add fowarding classes
    fowarding_class = FowardingClassParcel(parcel_name="FowardingClassParcelExmaple")
    fowarding_class.add_queue("4")

    # Create Tloc Parcel and add tlocs
    tloc_list = TlocParcel(parcel_name="TlocParcelExample")
    tloc_list.add_entry(
        tloc=IPv4Address("40.0.0.0"), color=TLOCColorEnum.PRIVATE3, encapsulation=EncapEnum.GRE, preference="1000"
    )
    tloc_list.add_entry(
        tloc=IPv4Address("50.0.0.0"), color=TLOCColorEnum.CUSTOM1, encapsulation=EncapEnum.GRE, preference="10000"
    )

    # Create Standard Community Parcel and add standard communities
    standard_community = StandardCommunityParcel(parcel_name="StandardCommunityParcelExample")
    standard_community.add_community(WellKnownBGPCommunitiesEnum.INTERNET)
    standard_community.add_community(WellKnownBGPCommunitiesEnum.LOCAL_AS)
    standard_community.add_community(WellKnownBGPCommunitiesEnum.NO_ADVERTISE)

    # Create Expanded Community Parcel and add expanded communities
    expanded_community = ExpandedCommunityParcel(parcel_name="ExpandedCommunityParcel")
    expanded_community.add_community("CommunityList1")
    expanded_community.add_community("CommunityList2")
    expanded_community.add_community("CommunityList3")

    # Create App Probe Parcel and add app probes
    app_probe = AppProbeParcel(parcel_name="AppProbeParcelExample")
    app_probe.add_fowarding_class("FowardingClassParcelExmaple")
    app_probe.add_map(color=TLOCColorEnum.CUSTOM1, dscp=33)
    app_probe.add_map(color=TLOCColorEnum.BLUE, dscp=40)
    app_probe.add_map(color=TLOCColorEnum.PUBLIC_INTERNET, dscp=43)

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

    sla = SLAClassParcel(parcel_name="SLAClassParcelExample")
    sla.add_entry(app_probe_class_id=_id.id, jitter=20, latency=50, loss=100)
    sla.add_fallback(
        criteria=SLAClassCriteriaEnum.JITTER_LATENCY_LOSS, latency_variance=10, jitter_variance=10, loss_variance=10
    )

    items_ids.append((api.create(profile, sla), sla.__class__))

    input("Press enter to delete...")

    for _id, item_type in reversed(items_ids):
        api.delete(profile, item_type, _id.id)


def retrive_groups_of_interest(profile: FeatureProfileInfo, api: PolicyObjectFeatureProfileAPI):
    print(api.get(profile, ApplicationListParcel))  # Get all Application List Parcels


def run_demo(args: CmdArguments):
    """
    Runs a demo of the Catalyst WAN API.

    Args:
        args (CmdArguments): The command line arguments.

    Returns:
        None: This function does not return any additional values.
    """
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
    """
    Load the command line arguments for the script.

    Returns:
        CmdArguments: The command line arguments.
    """
    url = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    return CmdArguments(url, int(port), user, password)


if __name__ == "__main__":
    arguments = load_arguments()
    run_demo(arguments)
