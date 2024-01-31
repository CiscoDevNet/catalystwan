# mypy: ignore-errors
"""
This example demonstrates usage of PolicyAPI in vmngclient
Code below provides same results as obtained after executing workflow manually via WEB-UI according to:
'Policies Configuration Guide for vEdge Routers, Cisco SD-WAN Release 20'
https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/policies/vedge-20-x/policies-book/centralized-policy.html

1.  Configure Groups of Interest for Centralized Policy
2.  Configure Topology and VPN Membership
3.  Import Existing Topology
4.  Create a VPN Membership Policy
5.  Configure Traffic Rules
6.  Match Parameters - Control Policy
7.  Match Parameters - Data Policy
8.  Action Parameters - Control Policy
9.  Action Parameters - Data Policy
10. Apply Policies to Sites and VPNs
11. NAT Fallback on Cisco IOS XE Catalyst SD-WAN Devices
12. Activate a Centralized Policy

To run example provide (url, port, username, password) to reachable vmanage instance as command line arguments:
python examples/policies_configuration_guide.py 127.0.0.1 433 admin p4s$w0rD
"""

import logging
import sys
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network, IPv6Network
from typing import List, Optional, Sequence
from uuid import UUID

from vmngclient.api.policy_api import PolicyAPI
from vmngclient.models.policy import (
    AppList,
    AppProbeClassList,
    ClassMapList,
    ColorList,
    CommunityList,
    DataIPv6PrefixList,
    DataPrefixList,
    ExpandedCommunityList,
    HubAndSpokePolicy,
    MeshPolicy,
    PolicerList,
    PrefixList,
    RegionList,
    SiteList,
    SLAClassList,
    TLOCList,
    VPNList,
    VPNMembershipPolicy,
)
from vmngclient.models.policy.definitions.control import ControlPolicy

logger = logging.getLogger(__name__)


@dataclass
class CmdArguments:
    url: str
    port: int
    user: str
    password: str
    device_template: Optional[str] = None


@dataclass
class ConfigItem:
    type_: type
    name: str
    id_: UUID


def find_item(items: Sequence[ConfigItem], name: str, type_: Optional[type] = None) -> UUID:
    for item in items:
        if item.name == name:
            if type_ is not None and item.type_ != type_:
                continue
            return item.id_
    raise KeyError("Cannot find item: {name}")


def configure_groups_of_interest(api: PolicyAPI) -> List[ConfigItem]:
    created_items: List[ConfigItem] = []

    # Configure Application
    app_list = AppList(name="MyApplications")
    app_list.add_app("abc-news")
    app_list.add_app_family("application-service")
    app_list_id = api.lists.create(app_list)
    created_items.append(ConfigItem(AppList, app_list.name, app_list_id))

    # Configure Color
    color_list = ColorList(name="MyColors")
    color_list.add_color("biz-internet")
    color_list.add_color("public-internet")
    color_list_id = api.lists.create(color_list)
    created_items.append(ConfigItem(ColorList, color_list.name, color_list_id))

    # Configure Community
    community_list = CommunityList(name="MyCommunities")
    community_list.add_community(1000, 10000)
    community_list.add_well_known_community("no-advertise")
    community_list_id = api.lists.create(community_list)
    created_items.append(ConfigItem(CommunityList, community_list.name, community_list_id))

    expanded_community_list = ExpandedCommunityList(name="MyExpandedCommunities")
    expanded_community_list.add_community(1000, 9999999)
    expanded_community_list.add_well_known_community("internet")
    expanded_community_list_id = api.lists.create(expanded_community_list)
    created_items.append(ConfigItem(ExpandedCommunityList, expanded_community_list.name, expanded_community_list_id))

    # Configure Data Prefix
    data_prefix_list = DataPrefixList(name="MyDataPrefixes")
    data_prefix_list.add_prefix(IPv4Network("12.0.0.0/16"))
    data_prefix_list.add_prefix(IPv4Network("12.1.0.0/16"))
    data_prefix_list_id = api.lists.create(data_prefix_list)
    created_items.append(ConfigItem(DataPrefixList, data_prefix_list.name, data_prefix_list_id))

    data_ipv6_prefix_list = DataIPv6PrefixList(name="MyDataIPv6Prefixes")
    data_ipv6_prefix_list.add_prefix(IPv6Network("2001:db8::1000/124"))
    data_ipv6_prefix_list.add_prefix(IPv6Network("2001:db9::1000/124"))
    data_ipv6_prefix_list_id = api.lists.create(data_ipv6_prefix_list)
    created_items.append(ConfigItem(DataIPv6PrefixList, data_ipv6_prefix_list.name, data_ipv6_prefix_list_id))

    # Configure Policer
    policer = PolicerList(name="MyPolicer")
    policer.police(2**17, 8, "remark")
    policer_id = api.lists.create(policer)
    created_items.append(ConfigItem(PolicerList, policer.name, policer_id))

    # Configure Prefix
    prefix_list = PrefixList(name="MyPrefixes")
    prefix_list.add_prefix(IPv4Network("10.0.0.0/16"))
    prefix_list.add_prefix(IPv4Network("11.0.0.0/16"), ge=2)
    prefix_list_id = api.lists.create(prefix_list)
    created_items.append(ConfigItem(PrefixList, prefix_list.name, prefix_list_id))

    # Configure Sites
    site_list = SiteList(name="MySites")
    site_list.add_site_range((300, 400))
    site_list.add_sites({200, 202})
    site_list_id = api.lists.create(site_list)
    created_items.append(ConfigItem(SiteList, site_list.name, site_list_id))

    hub_site_list = SiteList(name="MyHubSite")
    hub_site_list.add_sites({90})
    hub_site_list_id = api.lists.create(hub_site_list)
    created_items.append(ConfigItem(SiteList, hub_site_list.name, hub_site_list_id))

    spoke_sites_1_list = SiteList(name="MySpokeSites-1")
    spoke_sites_1_list.add_site_range((190, 290))
    spoke_site_list_id = api.lists.create(spoke_sites_1_list)
    created_items.append(ConfigItem(SiteList, spoke_sites_1_list.name, spoke_site_list_id))

    spoke_sites_2_list = SiteList(name="MySpokeSites-2")
    spoke_sites_2_list.add_sites({291, 299})
    spoke_site_list_id = api.lists.create(spoke_sites_2_list)
    created_items.append(ConfigItem(SiteList, spoke_sites_2_list.name, spoke_site_list_id))

    mesh_sites_1_list = SiteList(name="MyMeshSites-1")
    mesh_sites_1_list.add_site_range((50, 60))
    mesh_sites_1_list_id = api.lists.create(mesh_sites_1_list)
    created_items.append(ConfigItem(SiteList, mesh_sites_1_list.name, mesh_sites_1_list_id))

    mesh_sites_2_list = SiteList(name="MyMeshSites-2")
    mesh_sites_2_list.add_site_range((62, 69))
    mesh_sites_2_list_id = api.lists.create(mesh_sites_2_list)
    created_items.append(ConfigItem(SiteList, mesh_sites_2_list.name, mesh_sites_2_list_id))

    # Configure App Probe Class
    class_map = ClassMapList(name="MyClassMap")
    class_map.assign_queue(1)
    class_map_id = api.lists.create(class_map)
    created_items.append(ConfigItem(ClassMapList, class_map.name, class_map_id))

    app_probe_class = AppProbeClassList(name="MyAppProbeClass")
    app_probe_class.assign_forwarding_class("MyClassMap").add_color_mapping("3g", 5)
    app_probe_class_id = api.lists.create(app_probe_class)
    created_items.append(ConfigItem(AppProbeClassList, app_probe_class.name, app_probe_class_id))

    # Configure SLA Class
    sla_class = SLAClassList(name="MySLAClass")
    sla_class.assign_app_probe_class(app_probe_class_id, latency=10, loss=1, jitter=5)
    sla_class.add_fallback_jitter_criteria(10)
    sla_class.add_fallback_loss_criteria(5)
    sla_class_id = api.lists.create(sla_class)
    created_items.append(ConfigItem(SLAClassList, sla_class.name, sla_class_id))

    # Configure TLOC
    tloc_list = TLOCList(name="MyTLOCList")
    tloc_list.add_tloc(IPv4Address("10.0.0.55"), color="blue", encap="gre")
    tloc_list.add_tloc(IPv4Address("10.0.0.56"), color="silver", encap="ipsec", preference=5678)
    tloc_list_id = api.lists.create(tloc_list)
    created_items.append(ConfigItem(TLOCList, tloc_list.name, tloc_list_id))

    # Configure Region
    region_list = RegionList(name="MyRegions")
    region_list.add_regions({1, 2})
    region_list.add_region_range((3, 6))
    region_list_id = api.lists.create(region_list)
    created_items.append(ConfigItem(RegionList, region_list.name, region_list_id))

    # Configure VPNs
    vpn_list = VPNList(name="MyVPNList")
    vpn_list.add_vpns({100, 200})
    vpn_list.add_vpn_range((1000, 2000))
    vpn_list_id = api.lists.create(vpn_list)
    created_items.append(ConfigItem(VPNList, vpn_list.name, vpn_list_id))

    hub_and_spoke_vpn = VPNList(name="MyHubAndSpokeVPN")
    hub_and_spoke_vpn.add_vpns({150})
    hub_and_spoke_vpn_id = api.lists.create(hub_and_spoke_vpn)
    created_items.append(ConfigItem(VPNList, hub_and_spoke_vpn.name, hub_and_spoke_vpn_id))

    mesh_vpn = VPNList(name="MyMeshVPN")
    mesh_vpn.add_vpns({151})
    mesh_vpn_id = api.lists.create(mesh_vpn)
    created_items.append(ConfigItem(VPNList, mesh_vpn.name, mesh_vpn_id))

    export_vpn = VPNList(name="MyExportVPN")
    export_vpn.add_vpns({11})
    export_vpn_id = api.lists.create(export_vpn)
    created_items.append(ConfigItem(VPNList, export_vpn.name, export_vpn_id))

    return created_items


def create_vpn_membership_policy(api: PolicyAPI, items: Sequence[ConfigItem]) -> ConfigItem:
    # find applicable groups of interest
    policy = VPNMembershipPolicy(name="MyVPNMembershipPolicy")
    site_list_id = find_item(items, "MySites")
    vpn_list_id = find_item(items, "MyVPNList")
    # define VPN membership group policy
    policy.add_site(site_list_id, [vpn_list_id])
    policy_id = api.definitions.create(policy)
    return ConfigItem(VPNMembershipPolicy, policy.name, policy_id)


def create_hub_and_spoke_topology(api: PolicyAPI, items: Sequence[ConfigItem]) -> ConfigItem:
    # find applicable groups of interest
    hub_and_spoke_vpn = find_item(items, "MyHubAndSpokeVPN")
    hub_site = find_item(items, "MyHubSite")
    spoke_sites_1 = find_item(items, "MySpokeSites-1")
    spoke_sites_2 = find_item(items, "MySpokeSites-2")
    # define hub-and-spoke topology policy
    policy = HubAndSpokePolicy.from_vpn_list("MyHubAndSpokePolicy", hub_and_spoke_vpn)
    policy.add_hub_and_spoke("MyHubAndSpokeSites", [hub_site], [spoke_sites_1, spoke_sites_2])
    policy_id = api.definitions.create(policy)
    return ConfigItem(HubAndSpokePolicy, policy.name, policy_id)


def create_mesh_topology(api: PolicyAPI, items: Sequence[ConfigItem]) -> ConfigItem:
    # find applicable groups of interest
    mesh_vpn = find_item(items, "MyMeshVPN")
    mesh_sites_1 = find_item(items, "MyMeshSites-1")
    mesh_sites_2 = find_item(items, "MyMeshSites-2")
    # define mesh topology policy
    policy = MeshPolicy.from_vpn_list("MyMeshPolicy", mesh_vpn)
    policy.add_region("MyMeshRegion", [mesh_sites_1, mesh_sites_2])
    policy_id = api.definitions.create(policy)
    return ConfigItem(MeshPolicy, policy.name, policy_id)


def create_custom_control_topology(api: PolicyAPI, items: Sequence[ConfigItem]) -> ConfigItem:
    # define custom control (route & TLOC) topology policy
    policy = ControlPolicy(name="MyControlPolicy")

    # add first route sequence
    route_1 = policy.add_route_sequence(base_action="accept")
    route_1.match_color_list(find_item(items, "MyColors"))
    route_1.match_community_list(find_item(items, "MyCommunities"))
    route_1.match_expanded_community_list(find_item(items, "MyExpandedCommunities"))
    route_1.match_omp_tag(4321)
    route_1.match_origin("ospf-inter-area")
    route_1.match_originator(IPv4Address("10.0.0.123"))
    route_1.match_path_type("direct-path")
    route_1.match_preference(5432)
    route_1.match_prefix_list(find_item(items, "MyPrefixes"))
    route_1.match_region(7, "border-router")
    route_1.associate_affinity_action(3)
    route_1.associate_community_action("local-AS")
    route_1.associate_export_to_action(find_item(items, "MyExportVPN"))
    route_1.associate_omp_tag_action(4)
    route_1.associate_preference_action(5)
    route_1.associate_service_action("IDP", 19, tloc_list_id=find_item(items, "MyTLOCList"))

    # add second route sequence
    route_2 = policy.add_route_sequence("Route-2", base_action="accept")
    route_2.match_region_list(find_item(items, "MyRegions"))
    route_2.associate_tloc_action("primary")

    # add TLOC sequence
    tloc = policy.add_tloc_sequence(base_action="accept")
    tloc.match_carrier("carrier1")
    tloc.match_color_list(find_item(items, "MyColors"))
    tloc.match_domain_id(6543)
    tloc.match_group_id(7654)
    tloc.match_omp_tag(8765)
    tloc.match_preference(9876)
    tloc.match_region_list(find_item(items, "MyRegions"), "edge-router")
    tloc.match_site(20)

    # commit policy to sdwan manager
    policy_id = api.definitions.create(policy)
    return ConfigItem(ControlPolicy, policy.name, policy_id)


def delete_created_items(api: PolicyAPI, items: List[ConfigItem]) -> None:
    for item in reversed(items):
        api.delete_any(item.type_, item.id_)


def run_demo(args: CmdArguments):
    from vmngclient.session import create_vManageSession

    with create_vManageSession(url=args.url, port=args.port, username=args.user, password=args.password) as session:
        api = session.api.policy
        try:
            """1. Configure Groups of Interest for Centralized Policy"""
            configured_items = configure_groups_of_interest(api)
            """2. Configure Topology and VPN Membership"""
            configured_items.append(create_hub_and_spoke_topology(api, configured_items))
            configured_items.append(create_mesh_topology(api, configured_items))
            configured_items.append(create_custom_control_topology(api, configured_items))
            """3. Import Existing Topology"""
            # TODO
            """4. Create VPN Membership Policy"""
            configured_items.append(create_vpn_membership_policy(api, configured_items))
        except Exception as e:
            logger.exception(e)
        """Cleanup"""
        input("press enter to delete created items...")
        delete_created_items(api, configured_items)


def load_arguments() -> CmdArguments:
    url = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    return CmdArguments(url, int(port), user, password)


if __name__ == "__main__":
    arguments = load_arguments()
    run_demo(arguments)
