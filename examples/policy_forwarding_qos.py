# mypy: ignore-errors
"""
[Draft] 'pip install vmngclient==0.17.3.dev4'
This example demonstrates usage of PolicyAPI in vmngclient
Code below executes equivalent of WEB-UI steps presented in
'Forwarding and QoS Configuration Guide for vEdge Routers, Cisco SD-WAN Release 20'
https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/qos/vEdge-20-x/qos-book/forwarding-qos.html#Cisco_Concept.dita_bce41c9c-323f-4a04-af08-38604e5de0ee
I.   Map Each Forwarding Class to an Output Queue
II.  Configure Localized Policy
    A. Enable Cloud QoS
    B. Configure QoS Scheduler
    C. Create Re-write Policy
III. Apply Localized Policy to the Device Template
IV.  Apply QoS and Re-write Policy to WAN Interface Feature Template
V.   Define Centralized Traffic Data QoS Policy to Classify Traffic into Proper Queue
VI.  Apply Centralized Policy
"""
from vmngclient.session import create_vManageSession

# Provide ip/port to reachable vmanage instance together with valid credentials, recommended target: SDWAN >= 20.12
SESSION_PARAMS = {"url": "127.0.0.1", "port": 443, "username": "admin", "password": "***"}

with create_vManageSession(**SESSION_PARAMS) as session:
    api = session.api.policy

    """ I. Map Each Forwarding Class to an Output Queue:
        1. From the Cisco vManage menu, choose Configuration > Policies.
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
            | CONTROL SIGNALING |     5 |
            +-------------------+-------+
    """

    from vmngclient.model.policy.lists import ClassMapList

    pol_dict = {}  # this variable will hold a dictionary of created policy references by names used in examples
    for i, name in enumerate(["VOICE", "CRITICAL_DATA", "BULK", "DEFAULT", "INTERACTIVE_VIDEO", "CONTROL_SIGNALING"]):
        class_map = ClassMapList(name=name)
        class_map.add_queue(i)
        pol_dict[name] = api.lists.create(class_map)

    """ II.A. Configure Localized Policy: Enable Cloud QoS
        1. From the Cisco vManage menu, choose Configuration > Policies.
        2. Click Localized Policy.
        3. Create a customized localized policy following the steps below:
        4. Click Add Policy.
        5. In the Add Policy page, continue to click Next till you navigate to Policy Overview page.
        6. In the Policy Overview page, enter Policy Name and Description for your localized policy.
        7. In the Policy Overview page, select the Cloud QoS checkbox to enable QoS on the transport side
        and select the Cloud QoS Service side checkbox to enable QoS on the service side.
    """

    from vmngclient.model.policy.localized import LocalizedPolicy

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

    from vmngclient.model.policy.definitions.qos_map import QoSMap

    qos_map = QoSMap(name="My-QosMap-Policy")
    qos_map.add_scheduler(queue=1, class_map_ref=pol_dict["CRITICAL_DATA"], bandwidth=30, buffer=30)  # red is default
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
    from vmngclient.model.policy.definitions.rewrite import RewritePolicy

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

    input("Check in browser that policies are created. Press Enter to remove created items ...")

    api.definitions.delete(RewritePolicy, pol_dict["My-Rewrite-Policy"])
    api.definitions.delete(QoSMap, pol_dict["My-QosMap-Policy"])
    api.lists.delete(ClassMapList, pol_dict["VOICE"])
    api.lists.delete(ClassMapList, pol_dict["CRITICAL_DATA"])
    api.lists.delete(ClassMapList, pol_dict["BULK"])
    api.lists.delete(ClassMapList, pol_dict["DEFAULT"])
    api.lists.delete(ClassMapList, pol_dict["INTERACTIVE_VIDEO"])
    api.lists.delete(ClassMapList, pol_dict["CONTROL_SIGNALING"])
