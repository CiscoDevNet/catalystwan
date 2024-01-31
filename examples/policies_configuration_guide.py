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
from typing import List, Optional, Tuple
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
    PolicerList,
    PrefixList,
    RegionList,
    SiteList,
    SLAClassList,
    TLOCList,
    VPNList,
    VPNMembershipPolicy,
)

logger = logging.getLogger(__name__)


@dataclass
class CmdArguments:
    url: str
    port: int
    user: str
    password: str
    device_template: Optional[str] = None


def configure_groups_of_interest(api: PolicyAPI) -> List[Tuple[type, UUID]]:
    created_items: List[Tuple[type, UUID]] = []

    # Configure Application
    app_list = AppList(name="MyApplications")
    app_list.add_app("abc-news")
    app_list.add_app_family("application-service")
    app_list_id = api.lists.create(app_list)
    created_items.append((AppList, app_list_id))

    # Configure Color
    color_list = ColorList(name="MyColors")
    color_list.add_color("biz-internet")
    color_list.add_color("public-internet")
    color_list_id = api.lists.create(color_list)
    created_items.append((ColorList, color_list_id))

    # Configure Community
    community_list = CommunityList(name="MyCommunities")
    community_list.add_community(1000, 10000)
    community_list.add_well_known_community("no-advertise")
    community_list_id = api.lists.create(community_list)
    created_items.append((CommunityList, community_list_id))

    expanded_community_list = ExpandedCommunityList(name="MyExpandedCommunities")
    expanded_community_list.add_community(1000, 9999999)
    expanded_community_list.add_well_known_community("internet")
    expanded_community_list_id = api.lists.create(expanded_community_list)
    created_items.append((ExpandedCommunityList, expanded_community_list_id))

    # Configure Data Prefix
    data_prefix_list = DataPrefixList(name="MyDataPrefixes")
    data_prefix_list.add_prefix(IPv4Network("12.0.0.0/16"))
    data_prefix_list.add_prefix(IPv4Network("12.1.0.0/16"))
    data_prefix_list_id = api.lists.create(data_prefix_list)
    created_items.append((DataPrefixList, data_prefix_list_id))

    data_ipv6_prefix_list = DataIPv6PrefixList(name="MyDataIPv6Prefixes")
    data_ipv6_prefix_list.add_prefix(IPv6Network("2001:db8::1000/124"))
    data_ipv6_prefix_list.add_prefix(IPv6Network("2001:db9::1000/124"))
    data_ipv6_prefix_list_id = api.lists.create(data_ipv6_prefix_list)
    created_items.append((DataIPv6PrefixList, data_ipv6_prefix_list_id))

    # Configure Policer
    policer = PolicerList(name="MyPolicer")
    policer.police(2**17, 8, "remark")
    policer_id = api.lists.create(policer)
    created_items.append((PolicerList, policer_id))

    # Configure Prefix
    prefix_list = PrefixList(name="MyPrefixes")
    prefix_list.add_prefix(IPv4Network("10.0.0.0/16"))
    prefix_list.add_prefix(IPv4Network("11.0.0.0/16"), ge=2)
    prefix_list_id = api.lists.create(prefix_list)
    created_items.append((PrefixList, prefix_list_id))

    # Configure Site
    site_list = SiteList(name="MySites")
    site_list.add_site_range((300, 400))
    site_list.add_sites({200, 202})
    site_list_id = api.lists.create(site_list)
    created_items.append((SiteList, site_list_id))

    # Configure App Probe Class
    class_map = ClassMapList(name="MyClassMap")
    class_map.assign_queue(1)
    class_map_id = api.lists.create(class_map)
    created_items.append((ClassMapList, class_map_id))

    app_probe_class = AppProbeClassList(name="MyAppProbeClass")
    app_probe_class.assign_forwarding_class("MyClassMap").add_color_mapping("3g", 5)
    app_probe_class_id = api.lists.create(app_probe_class)
    created_items.append((AppProbeClassList, app_probe_class_id))

    # Configure SLA Class
    sla_class = SLAClassList(name="MySLAClass")
    sla_class.assign_app_probe_class(app_probe_class_id, latency=10, loss=1, jitter=5)
    sla_class.add_fallback_jitter_criteria(10)
    sla_class.add_fallback_loss_criteria(5)
    sla_class_id = api.lists.create(sla_class)
    created_items.append((SLAClassList, sla_class_id))

    # Configure TLOC
    tloc_list = TLOCList(name="MyTLOCList")
    tloc_list.add_tloc(IPv4Address("10.0.0.55"), color="blue", encap="gre")
    tloc_list.add_tloc(IPv4Address("10.0.0.56"), color="silver", encap="ipsec", preference=5678)
    tloc_list_id = api.lists.create(tloc_list)
    created_items.append((TLOCList, tloc_list_id))

    # Configure Region
    region_list = RegionList(name="MyRegions")
    region_list.add_regions({1, 2})
    region_list.add_region_range((3, 6))
    region_list_id = api.lists.create(region_list)
    created_items.append((RegionList, region_list_id))

    # Configure VPN
    vpn_list = VPNList(name="MyVPNList")
    vpn_list.add_vpns({100, 200})
    vpn_list.add_vpn_range((1000, 2000))
    vpn_list_id = api.lists.create(vpn_list)
    created_items.append((VPNList, vpn_list_id))

    return created_items


def create_vpn_membership_policy(api: PolicyAPI) -> Tuple[type, UUID]:
    site_list = api.lists.get(SiteList).first().list_id
    vpn_list = api.lists.get(VPNList).first().list_id
    policy = VPNMembershipPolicy(name="MyVPNMembershipPolicy")
    policy.add_site(site_list, [vpn_list])
    policy_id = api.definitions.create(policy)
    return (VPNMembershipPolicy, policy_id)


def delete_created_items(api: PolicyAPI, items: List[Tuple[type, UUID]]) -> None:
    for _type, _uuid in reversed(items):
        api.delete_any(_type, _uuid)


def run_demo(args: CmdArguments):
    from vmngclient.session import create_vManageSession

    with create_vManageSession(url=args.url, port=args.port, username=args.user, password=args.password) as session:
        api = session.api.policy
        """1. Configure Groups of Interest for Centralized Policy"""
        configured_items = configure_groups_of_interest(api)
        """2. Configure Topology and VPN Membership"""
        # TODO
        """3. Import Existing Topology"""
        # TODO
        """4. Create VPN Membership Policy"""
        configured_items.append(create_vpn_membership_policy(api))
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
