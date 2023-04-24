from __future__ import annotations

import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class PolicyList:
    '''
    This class represents various (GET / DELETE / POST) operations that can be
    done with Centralized / Localized policy lists.
    '''
    # Data prefix list mount points
    MP_DATA_PREFIX_LIST = "/dataservice/template/policy/list/dataprefix"
    MP_DATA_PREFIX_ALL = "/dataservice/template/policy/list/dataprefixall"
    MP_DATA_PREFIX_ID = \
        "/dataservice/template/policy/list/dataprefix/{list_id}"

    # Site list mount points
    MP_SITE_LIST = "/dataservice/template/policy/list/site"
    MP_SITE_ALL = "/dataservice/template/policy/list/site"
    MP_SITE_ID = "/dataservice/template/policy/list/site/{list_id}"

    # VPN list mount points
    MP_VPN_LIST = "/dataservice/template/policy/list/vpn"
    MP_VPN_ALL = "/dataservice/template/policy/list/vpn"
    MP_VPN_ID = "/dataservice/template/policy/list/vpn/{list_id}"

    # Data / traiffic policy mount points
    MP_DATA_POLICY = "/dataservice/template/policy/definition/data"
    MP_DATA_POLICY_ID = "/dataservice/template/policy/definition/data/{definition_id}"

    # vSmart policy mount points
    MP_VSMART_POLICY = "/dataservice/template/policy/vsmart/"
    MP_VSMART_POLICY_ID = "/dataservice/template/policy/vsmart/{policy_id}"
    MP_VSMART_POLICY_ACTIVATE = "/dataservice/template/policy/vsmart/activate/{policy_id}?confirm=true"
    MP_VSMART_POLICY_DEACTIVATE = "/dataservice/template/policy/vsmart/deactivate/{policy_id}?confirm=true"
    MP_VSMART_CONFIG_ID = "/dataservice/device/action/status/{task_id}"

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def create_data_prefix_list(self, name: str, ip_prefixes: list):
        '''
        Creates data prefix list
        '''
        payload = {
            "name": name,
            "description": "Desc not required",
            "type": "dataprefix",
            "listId": None,
            "entries": [{"ipPrefix": item.strip()} for item in ip_prefixes.split(",")],
        }

        response = self.session.post(self.MP_DATA_PREFIX_LIST, json=payload)
        try:
            list_id = response.json()["listId"]
        except Exception:
            list_id = None

        return list_id

    def get_data_prefix_lists(self):
        '''
        Gets all existing data prefix lists
        '''
        response = self.session.get(self.MP_DATA_PREFIX_ALL)

        if not response.ok:
            logger.error("Failed to get data prefix lists. Details: "
                         f"{response.text}")
            return None

        try:
            data = response.json()['data']
        except Exception as ex:
            logger.error("Caught exception while extracting data for data "
                         f"prefix list. Details: {ex}")
            data = None

        return data

    def get_data_prefix_list(self, name):
        '''
        Gets details of given data prefix list
        '''
        data_prefix_lists = self.get_data_prefix_lists()

        if data_prefix_lists is None:
            logger.error("Failed to get data prefix lists")
            return None
        
        data_prefix_list = None
        for item in data_prefix_lists:
            if item['name'] == name:
                data_prefix_list = item
                break
        
        return data_prefix_list

    def delete_data_prefix_list(self, list_id):
        '''
        Deletes data prefix list with given list ID
        '''
        mount_point = self.MP_DATA_PREFIX_ID.format(list_id=list_id)
        response = self.session.delete(mount_point)

        if not response.ok:
            logger.error(f"Failed to delete data prefix list: {list_id}"
                         f"Details: {response.text}")
            return False

        return True

    def create_site_list(self, name: str, sites: list):
        '''
        Creates site list
        '''
        payload = {
            "name": name,
            "description": "Desc not required",
            "type": "site",
            "listId": None,
            "entries": [{"siteId": item.strip()} for item in sites.split(",")],
        }

        response = self.session.post(self.MP_SITE_LIST, json=payload)
        try:
            list_id = response.json()["listId"]
        except Exception:
            list_id = None

        return list_id

    def get_site_lists(self):
        '''
        Gets all existing site lists
        '''
        response = self.session.get(self.MP_SITE_ALL)

        if not response.ok:
            logger.error(f"Failed to get site lists. Details: {response.text}")
            return None

        try:
            data = response.json()['data']
        except Exception as ex:
            logger.error("Caught exception while extracting data for site "
                         f"list. Details: {ex}")
            data = None

        return data
    
    def get_site_list(self, name):
        '''
        Gets details of given site list
        '''
        site_lists = self.get_site_lists()

        if site_lists is None:
            logger.error("Failed to get site lists")
            return None
        
        site_list = None
        for item in site_lists:
            if item['name'] == name:
                site_list = item
                break
        
        return site_list

    def delete_site_list(self, list_id):
        '''
        Deletes site list with given list ID
        '''
        mount_point = self.MP_SITE_ID.format(list_id=list_id)
        response = self.session.delete(mount_point)

        if not response.ok:
            logger.error(f"Failed to delete site list: {list_id}"
                         f"Details: {response.text}")
            return False

        return True

    def create_vpn_list(self, name: str, vpns: list):
        '''
        Creates VPN list
        '''
        payload = {
            "name": name,
            "description": "Desc not required",
            "type": "vpn",
            "listId": None,
            "entries": [{"vpn": item.strip()} for item in vpns.split(",")]
        }

        response = self.session.post(self.MP_VPN_LIST, json=payload)
        try:
            list_id = response.json()["listId"]
        except Exception:
            list_id = None

        return list_id

    def get_vpn_lists(self):
        '''
        Gets all existing VPN lists
        '''
        response = self.session.get(self.MP_VPN_ALL)

        if not response.ok:
            logger.error(f"Failed to get VPN lists. Details: {response.text}")
            return None

        try:
            data = response.json()['data']
        except Exception as ex:
            logger.error("Caught exception while extracting data for VPN "
                         f"list. Details: {ex}")
            data = None

        return data

    def get_vpn_list(self, name):
        '''
        Gets details of given VPN list
        '''
        vpn_lists = self.get_vpn_lists()

        if vpn_lists is None:
            logger.error("Failed to get VPN lists")
            return None
        
        vpn_list = None
        for item in vpn_lists:
            if item['name'] == name:
                vpn_list = item
                break
        
        return vpn_list

    def delete_vpn_list(self, list_id):
        '''
        Deletes VPN list with given list ID
        '''
        mount_point = self.MP_VPN_ID.format(list_id=list_id)
        response = self.session.delete(mount_point)

        if not response.ok:
            logger.error(f"Failed to delete VPN list: {list_id}"
                         f"Details: {response.text}")
            return False

        return True

    def create_data_policy(self, name, description, default_action, sequences):
        '''
        Creates data / traffic policy
        '''
        if name is None:
            logger.error(f"Invalid name: {name}")
            return None
        
        if description is None:
            logger.error(f"Invalid description: {description}")
            return None

        if default_action.lower() not in ['accept', 'drop']:
            logger.error(f"Invalid default_action: {default_action}")
            return None

        payload = {'name': name,
                   'type': 'data',
                   'description': description,
                   'defaultAction': {'type': default_action.lower()},
                   'sequences': sequences
                   }
        
        response = self.session.post(self.MP_DATA_POLICY, json=payload)

        try:
            definition_id = response.json()["definitionId"]
        except Exception:
            definition_id = None

        return definition_id

    def delete_data_policy(self, definition_id):
        '''
        Deletes data / traffic policy
        '''
        mount_point = self.MP_DATA_POLICY_ID.format(definition_id=definition_id)
        response = self.session.delete(mount_point)

        if not response.ok:
            logger.error(f"Failed to delete data policy: {definition_id}"
                         f"Details: {response.text}")
            return False

        return True
    
    def get_data_policies(self):
        '''
        Gets all existing data / traffic policies
        '''
        response = self.session.get(self.MP_DATA_POLICY)

        if not response.ok:
            logger.error(f"Failed to get data policies. Details: {response.text}")
            return None

        try:
            data = response.json()['data']
        except Exception as ex:
            logger.error("Caught exception while extracting data for data "
                         f"policies. Details: {ex}")
            data = None

        return data
    
    def get_data_policy(self, name):
        '''
        Gets details of given data / traffic policy
        '''
        data_policies = self.get_data_policies()

        if data_policies is None:
            logger.error("Failed to get data policies")
            return None
        
        data_policy = None
        for item in data_policies:
            if item['name'] == name:
                data_policy = item
                break
        
        return data_policy

    def create_vsmart_policy(self, name, description, definition):
        '''
        Creates vSmart policy
        '''
        payload = {
            "policyDescription": description,
            "policyType": "feature",
            "policyName": name,
            "policyDefinition": definition,
            "isPolicyActivated": False
        }

        response = self.session.post(self.MP_VSMART_POLICY, json=payload)
        try:
            policy_id = response.json()["policyId"]
        except Exception:
            policy_id = None

        return policy_id

    def create_vsmart_cli_policy(self, name, description, definition):
        '''
        Creates vSmart CLI policy
        '''
        payload = {
            "policyDescription": description,
            "policyName": name,
            "policyDefinition": definition,
        }

        response = self.session.post(self.MP_VSMART_POLICY, json=payload)
        try:
            policy_id = response.json()["policyId"]
        except Exception:
            policy_id = None

        return policy_id


    def delete_vsmart_policy(self, policy_id):
        '''
        Deletes vSmart policy with given list ID
        '''
        mount_point = self.MP_VSMART_POLICY_ID.format(policy_id=policy_id)
        response = self.session.delete(mount_point)

        if not response.ok:
            logger.error(f"Failed to delete vSmart policy: {policy_id}"
                         f"Details: {response.text}")
            return False

        return True

    def get_vsmart_policies(self):
        '''
        Gets all existing vSmart policies
        '''
        response = self.session.get(self.MP_VSMART_POLICY)

        if not response.ok:
            logger.error(f"Failed to get vSmart policies. Details: {response.text}")
            return None

        try:
            data = response.json()['data']
        except Exception as ex:
            logger.error("Caught exception while extracting data for vSmart "
                         f"policies. Details: {ex}")
            data = None

        return data
    
    def get_vsmart_policy(self, name):
        '''
        Gets details of given vSmart policy
        '''
        vsmart_policies = self.get_vsmart_policies()

        if vsmart_policies is None:
            logger.error("Failed to get vSmart policies")
            return None
        
        vsmart_policy = None
        for item in vsmart_policies:
            if item['policyName'] == name:
                vsmart_policy = item
                break
        
        return vsmart_policy

    def activate_vsmart_policy(self, name):
        '''
        Activates given vSmart policy
        '''
        vsmart_policy = self.get_vsmart_policy(name)

        if vsmart_policy is None:
            logger.error(f"Failed to get policy details for vSmart policy: {name}")
            return None

        policy_id = vsmart_policy.get('policyId')

        if policy_id is None:
            logger.error(f"Policy ID is None for policy {name}")
            return None

        mount_point = self.MP_VSMART_POLICY_ACTIVATE.format(policy_id=policy_id)

        response = self.session.post(mount_point, json={})

        if not response.ok:
            logger.error(f"Failed to activate vSmart policy. Details: {response.text}")
            return None

        task_id = None

        try:
            task_id = response.json()['id']
            logger.info(f"vSmart policy {name} activation started. "
                        f"Task ID: {task_id}")
        except Exception as ex:
            logger.error("Caught exception while extracting vSmart policy "
                         f"activation task ID. Details: {ex}")
            task_id = None

        return task_id

    def deactivate_vsmart_policy(self, name):
        '''
        Deactivates given vSmart policy
        '''
        vsmart_policy = self.get_vsmart_policy(name)

        if vsmart_policy is None:
            logger.error(f"Failed to get policy details for vSmart policy: {name}")
            return None

        policy_id = vsmart_policy.get('policyId')

        if policy_id is None:
            logger.error(f"Policy ID is None for policy {name}")
            return None

        mount_point = self.MP_VSMART_POLICY_DEACTIVATE.format(policy_id=policy_id)

        response = self.session.post(mount_point, json={})

        if not response.ok:
            logger.error(f"Failed to deactivate vSmart policy. Details: {response.text}")
            return None

        task_id = None

        try:
            task_id = response.json()['id']
            logger.info(f"vSmart policy {name} deactivation started. "
                        f"Task ID: {task_id}")
        except Exception as ex:
            logger.error("Caught exception while extracting vSmart policy "
                         f"deactivation task ID. Details: {ex}")
            task_id = None

        return task_id

    def get_vsmart_config_task_status(self, task_id):
        '''
        Gets vSmart config (activate / deactivate) task status
        '''
        mount_point = self.MP_VSMART_CONFIG_ID.format(task_id=task_id)
        response = self.session.get(mount_point)

        if not response.ok:
            logger.error("Failed to get vSmart config task status. "
                         f"Details: {response.text}")
            return None
        
        try:
            data = response.json()['data']
        except Exception as ex:
            logger.error("Caught exception while extracting data for vSmart "
                         f"config task status. Details: {ex}")
            data = None

        return data
