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
from ipaddress import IPv4Network, IPv6Network
from typing import List, Tuple

from vmngclient.api.policy_api import PolicyAPI

logger = logging.getLogger(__name__)


@dataclass
class CmdArguments:
    url: str
    port: int
    user: str
    password: str
    device_template: str = None


def configure_groups_of_interest(api: PolicyAPI) -> List[Tuple[type, str]]:
    created_items: List[Tuple[type, str]] = []

    # Configure Application
    from vmngclient.models.policy.lists import AppList

    app_list = AppList(name="MyApplications")
    app_list.add_app("abc-news")
    app_list.add_app_family("application-service")
    app_list_id = api.lists.create(app_list)
    created_items.append((AppList, app_list_id))

    # Configure Color
    from vmngclient.models.policy.lists import ColorList

    color_list = ColorList(name="MyColors")
    color_list.add_color("biz-internet")
    color_list_id = api.lists.create(color_list)
    created_items.append((ColorList, color_list_id))

    # Configure Community
    from vmngclient.models.policy.lists import CommunityList, ExpandedCommunityList

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
    from vmngclient.models.policy.lists import DataIPv6PrefixList, DataPrefixList

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
    from vmngclient.models.policy.lists import PolicerList

    policer_list = PolicerList(name="MyPolicers")
    policer_list.police(2**17, 8, "remark")
    policer_list_id = api.lists.create(policer_list)
    created_items.append((PolicerList, policer_list_id))

    # Configure Prefix
    from vmngclient.models.policy.lists import PrefixList

    prefix_list = PrefixList(name="MyPrefixes")
    prefix_list.add_prefix(IPv4Network("10.0.0.0/16"))
    prefix_list.add_prefix(IPv4Network("11.0.0.0/16"), ge=2)
    prefix_list_id = api.lists.create(prefix_list)
    created_items.append((PrefixList, prefix_list_id))

    # Configure Site
    from vmngclient.models.policy.lists import SiteList

    site_list = SiteList(name="MySites")
    site_list.add_site_range((300, 400))
    site_list.add_sites({200, 202})
    site_list_id = api.lists.create(site_list)
    created_items.append((SiteList, site_list_id))

    # Configure App Probe Class
    from vmngclient.models.policy.lists import AppProbeClassList, ClassMapList

    class_map_list = ClassMapList(name="BulkClass")
    class_map_list.set_queue(1)
    class_map_list_id = api.lists.create(class_map_list)
    created_items.append((ClassMapList, class_map_list_id))

    app_probe_class_list = AppProbeClassList(name="MyAppProbeClasses")
    app_probe_class_list.assign_forwarding_class("BulkClass").add_color_mapping("3g", 5)
    app_probe_class_list_id = api.lists.create(app_probe_class_list)
    created_items.append((AppProbeClassList, app_probe_class_list_id))

    # Configure SLA Class
    # Configure TLOC
    # Configure VPN
    return created_items


def run_demo(args: CmdArguments):
    from vmngclient.session import create_vManageSession

    with create_vManageSession(url=args.url, port=args.port, username=args.user, password=args.password) as session:
        api = session.api.policy
        """1. Configure Groups of Interest for Centralized Policy"""
        groups_of_iterest = configure_groups_of_interest(api)
        """Cleanup"""
        input("press enter to delete created items...")
        for item in groups_of_iterest:
            api.lists.delete(*item)


def load_arguments() -> CmdArguments:
    url = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    return CmdArguments(url, int(port), user, password)


if __name__ == "__main__":
    arguments = load_arguments()
    run_demo(arguments)
