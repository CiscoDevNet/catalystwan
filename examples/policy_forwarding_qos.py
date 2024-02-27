# Copyright 2023 Cisco Systems, Inc. and its affiliates

"""
This example demonstrates usage of PolicyAPI in catalystwan
Code below provides same results as obtained after executing workflow manually via WEB-UI according to:
'Forwarding and QoS Configuration Guide for vEdge Routers, Cisco SD-WAN Release 20'
https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/qos/vEdge-20-x/qos-book/forwarding-qos.html#Cisco_Concept.dita_aa3e0d07-462e-463f-8f45-681f38f61ab0
I.   Map Each Forwarding Class to an Output Queue
II.  Configure Localized Policy
    A. Enable Cloud QoS
    B. Configure QoS Scheduler
    C. Create Re-write Policy
III. Apply Localized Policy to the Device Template
IV.  Apply QoS and Re-write Policy to WAN Interface Feature Template
V.   Define Centralized Traffic Data QoS Policy to Classify Traffic into Proper Queue
VI.  Apply Centralized Policy

To run example provide (url, port, username, password) to reachable Manager instance as command line arguments:
python examples/policy_forwarding_qos.py 127.0.0.1 433 admin p4s$w0rD
"""

import logging
import sys
from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID

logger = logging.getLogger(__name__)


@dataclass
class CmdArguments:
    url: str
    port: int
    user: str
    password: str
    device_template: Optional[str] = None


def run_demo(args: CmdArguments):
    from catalystwan.exceptions import CatalystwanException
    from catalystwan.session import create_manager_session

    with create_manager_session(url=args.url, port=args.port, username=args.user, password=args.password) as session:
        api = session.api.policy
        """ I. Map Each Forwarding Class to an Output Queue:
            1. From the Cisco Manager menu, choose Configuration > Policies.
            2. From the Custom Options drop-down, select Lists under Localized Policy.
            3. Select the Class Map from the list types.
            4. Click the New Class List. The Class List pop-up page is displayed.
            5. Enter a name for the class. Select a required queue from the Queue drop-down list.
            6. Click Save.
            7. Repeat the last three steps to add more class lists as required.
                The following are example class lists and queue mappings:
                Table 1. Class List and Queue Mappings
                +-------------------+-------+
                |       Class       | Queue |
                +-------------------+-------+
                | VOICE             |     0 |
                | CRITICAL_DATA     |     1 |
                | BULK              |     2 |
                | DEFAULT           |     3 |
                | INTERACTIVE_VIDEO |     4 |
                | CONTROL_SIGNALING |     5 |
                +-------------------+-------+
        """
        logger.info("I. Map Each Forwarding Class to an Output Queue")
        from catalystwan.models.policy import ClassMapList

        pol_dict: Dict[
            str, UUID
        ] = {}  # this variable will hold a dictionary of created policy references by names used in examples
        for i, name in enumerate(
            ["VOICE", "CRITICAL_DATA", "BULK", "DEFAULT", "INTERACTIVE_VIDEO", "CONTROL_SIGNALING"]
        ):
            class_map = ClassMapList(name=name)
            class_map.assign_queue(i)
            pol_dict[name] = api.lists.create(class_map)

        """ II.A. Configure Localized Policy: Enable Cloud QoS
            1. From the Cisco Manager menu, choose Configuration > Policies.
            2. Click Localized Policy.
            3. Create a customized localized policy following the steps below:
            4. Click Add Policy.
            5. In the Add Policy page, continue to click Next till you navigate to Policy Overview page.
            6. In the Policy Overview page, enter Policy Name and Description for your localized policy.
            7. In the Policy Overview page, select the Cloud QoS checkbox to enable QoS on the transport side
            and select the Cloud QoS Service side checkbox to enable QoS on the service side.
        """
        logger.info("II.A. Configure Localized Policy: Enable Cloud QoS")
        from catalystwan.models.policy import LocalizedPolicy

        loc_pol = LocalizedPolicy(policy_name="My-Localized-Policy", policy_description="desc text")
        loc_pol.policy_definition.settings.cloud_qos = True
        loc_pol.policy_definition.settings.cloud_qos_service_side = True

        """ II.B. Configure Localized Policy: Configure QoS Scheduler
            1. Click Forwarding Class/QoS. When you navigate to the Forwarding Classes/QoS page,
            QoS Map is selected by default.
            2. Click Add QoS Map, and then click Create New.
            3. Enter the name and description for the QoS mapping.
            4. Queue 0 has already been defined by default and cannot be modified. Click the Add Queue.
            5. Select a required queue from the Queue drop-down.
            6. Slide the Bandwidth% and Buffer% bar and set the value as required.
            7. From the Drops drop-down, select the required drop type.
            8. Click Save Queue.
            9. Repeat the last three steps to add more queue as required.
                The following are the examples for queue and sample Bandwidth/Buffer configurations:
                Table 2. Bandwidth and buffer values and drop algorithm
                +-------+------------------+--------------------+
                | Queue | Bandwidth/Buffer |       Drops        |
                +-------+------------------+--------------------+
                |     1 | 30/30            | Random Early (RED) |
                |     2 | 10/10            | Random Early (RED) |
                |     3 | 20/20            | Random Early (RED) |
                |     4 | 20/20            | Random Early (RED) |
                |     5 | 10/10            | Tail Drop          |
                +-------+------------------+--------------------+
                QoS queue 0 should now be left at 10% Bandwidth and Buffer.
            10. Click Save Policy.
        """
        logger.info("II.B. Configure Localized Policy: Configure QoS Scheduler")
        from catalystwan.models.policy import QoSMapPolicy

        qos_map = QoSMapPolicy(name="My-QosMap-Policy")
        qos_map.add_scheduler(queue=1, class_map_ref=pol_dict["CRITICAL_DATA"], bandwidth=30, buffer=30)
        qos_map.add_scheduler(queue=2, class_map_ref=pol_dict["BULK"], bandwidth=10, buffer=10)
        qos_map.add_scheduler(queue=3, class_map_ref=pol_dict["DEFAULT"], bandwidth=20, buffer=20)
        qos_map.add_scheduler(queue=4, class_map_ref=pol_dict["INTERACTIVE_VIDEO"], bandwidth=20, buffer=20)
        qos_map.add_scheduler(
            queue=5, class_map_ref=pol_dict["CONTROL_SIGNALING"], bandwidth=10, buffer=10, drops="tail-drop"
        )
        pol_dict["My-QosMap-Policy"] = api.definitions.create(qos_map)

        """ II.C. Configure Localized Policy: Create Re-write Policy
            1. Click Policy Rewrite to add a rewrite policy.
            2. From the Add Rewrite Policy drop-down, select Create New.
            3. Enter a name and description for the rewrite rule.
            4. Click Add Rewrite Rule.
            5. In the Add Rule pop-up page:
            6. Select a class from the Class drop-down.
            7. Select the priority (Low or High) from the Priority drop-down.
            8. Low priority is supported only for Cisco IOS XE SD-WAN devices.
            9. Enter the DSCP value (0 through 63) in the DSCP field.
            10. Enter the class of service (CoS) value (0 through 7) in the Layer 2 Class of Service field.
            11.Click Save Rule.
            Repeat the previous 5 and 6 steps to add more QoS Rewrite rules as required.
                The following are example rewrite rule information:
                Table 3. QoS Rewrite Information
                +-------------------+----------+------+--------------------------+
                |       Class       | Priority | DSCP | Layer 2 Class of Service |
                +-------------------+----------+------+--------------------------+
                | BULK              | Low      |   10 |                        1 |
                | BULK              | High     |   10 |                        1 |
                | DEFAULT           | Low      |    0 |                        0 |
                | DEFAULT           | High     |    0 |                        0 |
                | CONTROL_SIGNALING | Low      |   18 |                        2 |
                | CONTROL_SIGNALING | High     |   18 |                        2 |
                | CRITICAL_DATA     | Low      |   18 |                        2 |
                | CRITICAL_DATA     | High     |   18 |                        2 |
                | INTERACTIVE_VIDEO | Low      |   34 |                        4 |
                | INTERACTIVE_VIDEO | High     |   34 |                        4 |
                +-------------------+----------+------+--------------------------+
            12. Click Save Policy.
            13. Click Save Policy Changes to save the changes to the localized master policy.
        """
        logger.info("II.C. Configure Localized Policy: Create Re-write Policy")
        from catalystwan.models.policy import RewritePolicy

        rw_pol = RewritePolicy(name="My-Rewrite-Policy")
        rw_pol.add_rule(class_map_ref=pol_dict["BULK"], plp="low", dscp=10, l2cos=1)
        rw_pol.add_rule(class_map_ref=pol_dict["BULK"], plp="high", dscp=10, l2cos=1)
        rw_pol.add_rule(class_map_ref=pol_dict["DEFAULT"], plp="low", dscp=0, l2cos=0)
        rw_pol.add_rule(class_map_ref=pol_dict["DEFAULT"], plp="high", dscp=0, l2cos=0)
        rw_pol.add_rule(class_map_ref=pol_dict["CONTROL_SIGNALING"], plp="low", dscp=18, l2cos=2)
        rw_pol.add_rule(class_map_ref=pol_dict["CONTROL_SIGNALING"], plp="high", dscp=18, l2cos=2)
        rw_pol.add_rule(class_map_ref=pol_dict["CRITICAL_DATA"], plp="low", dscp=18, l2cos=2)
        rw_pol.add_rule(class_map_ref=pol_dict["CRITICAL_DATA"], plp="high", dscp=18, l2cos=2)
        rw_pol.add_rule(class_map_ref=pol_dict["BULK"], plp="low", dscp=10, l2cos=4)
        rw_pol.add_rule(class_map_ref=pol_dict["BULK"], plp="high", dscp=10, l2cos=4)
        pol_dict["My-Rewrite-Policy"] = api.definitions.create(rw_pol)
        loc_pol.add_rewrite_rule(pol_dict["My-Rewrite-Policy"])
        pol_dict["My-Localized-Policy"] = api.localized.create(loc_pol)

        """ III.Apply Localized Policy to the Device Template
            1. From the Cisco Manager menu, choose Configuration > Templates
            2. Click Device Templates and select the desired template.
            3. Click …, and click Edit.
            4. Click Additional Templates.
            5. From the Policy drop-down, choose the Localized Policy that is created in the previous steps.
            6. Click Update.
                ** Note **
                Once the localized policy has been added to the device template,selecting the Update option immediately
                pushes a configuration change to all of the devices that are attached to this device template.
                If more than one device is attached to the device template,
                you will receive a warning that you are changing multiple devices.
            7. Click Next, and then Configure Devices.
            8. Wait for the validation process and push configuration from Cisco Manager to the device
        """
        logger.info("III.Apply Localized Policy to the Device Template")
        if args.device_template is None:
            logger.info("Pre-defined existing device template name not provided, skipping III")
        else:
            try:
                from catalystwan.api.templates.device_template.device_template import DeviceTemplate

                device_template = DeviceTemplate.get(args.device_template, session)
                device_template.policy_id = str(pol_dict["My-Localized-Policy"])
                session.api.templates.edit(device_template)
            except CatalystwanException:
                logger.warning("Failed to attach My-Localized-Policy to Device Template")

        """ V. Define Centralized Traffic Data QoS Policy to Classify Traffic into Proper Queue
            1. From the Cisco Manager menu, choose Configuration > Policies.
            2. Click Centralized Policy.
            3. For the desired policy in the list, click ..., and select Edit.
                (Optionally) If the desired policy is not available in the list,
                then you may create the customized centralized policy following the steps below:
                a. Click Add Policy.
                b. In the Add Policy page, continue to click Next till you navigate to Configure Traffic Rules page.
            4. Click Traffic Rules, then click Traffic Data.
            5. Click Add Policy drop-down.
            6. Click Create New. The Add Data Policy window displays.
            7. Enter a Name and the Description.
            8. Click Sequence Type. The Add Data Policy popup opens.
            9. Select QoS type of data policy.
            10. Click Sequence Rule. The Match/Action page opens, with Match selected by default.
            11. From the Match box, select the desired policy match type.
                Then select or enter the value for that match condition.
                Configure additional match conditions for the sequence rule, as desired.
            12. To select actions to take on matching data traffic, click Actions box.
            13. By default, Accept is enabled. Select Forwarding Class from actions.
            14. In the Forwarding Class field, and enter the class value (maximum of 32 characters).
            15. Click Save Match and Actions.
            16. Click Save Data Policy.
            17. If your are creating a new centralized policy,
                then click Next and navigate to Add policies to Sites and VPNs page.
                a. Enter a Policy Name and Description for your centralized policy.
                b. Click Save Data Policy.
        """
        logger.info("V. Define Centralized Traffic Data QoS Policy to Classify Traffic into Proper Queue")
        from catalystwan.models.policy import CentralizedPolicy, TrafficDataPolicy

        centralized_pol = CentralizedPolicy(policy_name="My-Centralized-Policy")
        data_pol = TrafficDataPolicy(name="My-Traffic-Data-Policy")
        data_pol_seq = data_pol.add_ipv4_sequence(base_action="accept")
        data_pol_seq.associate_forwarding_class_action(fwclass="CONTROL_SIGNALING")
        pol_dict["My-Traffic-Data-Policy"] = api.definitions.create(data_pol)

        """VI. Apply Centralized Policy
        1. Click Policy Application to apply the centralized policy.
        2. Click Traffic Data.
        3. Click New Site List and VPN list.
        4. Choose the direction for applying the policy (From Service, From Tunnel, or All),
            choose one or more site lists, and choose one or more VPN lists.
        5. Click Add.
        6. Click Save Policy Changes.
        7. A window pops up indicating the policy will be applied to the Cisco vSmart controller.
        8. Click Activate.
        9. Cisco Manager pushes the configuration to the Cisco vSmart controller and indicates success.
        """
        logger.info("VI. Apply Centralized Policy ...")
        pol_application = centralized_pol.add_traffic_data_policy(pol_dict["My-Traffic-Data-Policy"])

        from catalystwan.models.policy import SiteList, VPNList

        site_list = SiteList(name="My-Site-List")
        site_list.add_sites({4, 5})
        pol_dict["My-Site-List"] = api.lists.create(site_list)
        vpn_list = VPNList(name="My-VPN-List")
        vpn_list.add_vpn_range((100, 300))
        pol_dict["My-VPN-List"] = api.lists.create(vpn_list)

        pol_application.assign_to([pol_dict["My-VPN-List"]], "tunnel", site_lists=[pol_dict["My-Site-List"]])
        pol_dict["My-Centralized-Policy"] = api.centralized.create(centralized_pol)

        try:
            policy_activate_task = api.centralized.activate(pol_dict["My-Centralized-Policy"])
            policy_activate_task.wait_for_completed()
        except CatalystwanException:
            logger.warning("My-Centralized-Policy activation failed! are vSmarts in Manager mode?")

        """End of procedure, below is user prompt to check created policies and delete everything afterwards"""

        logger.info(api.localized.preview(pol_dict["My-Localized-Policy"]))
        logger.info(
            "Check contents of 'My-Localized-Policy' in browser: "
            f"\u001b[36;1m{session.get_full_url('/#/app/config/policy/localizedPolicy/policies')}\u001b[0m"
        )
        logger.info(
            "Check contents of 'My-Centralized-Policy' in browser: "
            f"\u001b[36;1m{session.get_full_url('/#/app/config/policy/centralizedPolicy/policies')}\u001b[0m"
        )
        input("Press Enter to remove created items ...")
        if api.centralized.get(pol_dict["My-Centralized-Policy"]).is_policy_activated:
            deactivation_task = api.centralized.deactivate(pol_dict["My-Centralized-Policy"])
            deactivation_task.wait_for_completed()
        api.centralized.delete(pol_dict["My-Centralized-Policy"])
        api.definitions.delete(TrafficDataPolicy, pol_dict["My-Traffic-Data-Policy"])
        api.lists.delete(SiteList, pol_dict["My-Site-List"])
        api.lists.delete(VPNList, pol_dict["My-VPN-List"])
        api.localized.delete(pol_dict["My-Localized-Policy"])
        api.definitions.delete(RewritePolicy, pol_dict["My-Rewrite-Policy"])
        api.definitions.delete(QoSMapPolicy, pol_dict["My-QosMap-Policy"])
        api.lists.delete(ClassMapList, pol_dict["VOICE"])
        api.lists.delete(ClassMapList, pol_dict["CRITICAL_DATA"])
        api.lists.delete(ClassMapList, pol_dict["BULK"])
        api.lists.delete(ClassMapList, pol_dict["DEFAULT"])
        api.lists.delete(ClassMapList, pol_dict["INTERACTIVE_VIDEO"])
        api.lists.delete(ClassMapList, pol_dict["CONTROL_SIGNALING"])


def load_arguments() -> CmdArguments:
    url = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    device_template = sys.argv[5] if len(sys.argv) > 5 else None
    return CmdArguments(url, int(port), user, password, device_template)


if __name__ == "__main__":
    arguments = load_arguments()
    run_demo(arguments)
