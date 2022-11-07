
from vmngclient.dataclasses import InstallSpec
from vmngclient.session import Session
from vmngclient.api.repository import Repository
from typing import List
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.api.partition_manager_api import PartitionManager
import logging
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

logger = logging.getLogger(get_logger_name(__name__))
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s')



class SoftwareUpgradeApi:

    def __init__(self, session: Session,
                 install_spec: InstallSpec = None,
                 repository = Repository):

        self.session = session
        self.install_spec = install_spec
        self.repository = repository


    def activate_software(self,version_to_activate: str, devices_category: str) -> str:
        
        self.repository.devices_category = devices_category
        self.repository.complete_device_list(version_to_activate)
        url = '/dataservice/device/action/changepartition'
        payload = {'action': 'changepartition',
                   'devices': self.repository.devices,
                   'deviceType': 'vmanage'
                   }
        activate_id = self.session.post_json(url, payload)
        return activate_id['id']
    
    def upgrade_software(self, software_image: str):
        url = '/dataservice/device/action/install'
        payload = {"action":"install",
                   "input":{
                        "vEdgeVPN":0,
                        "vSmartVPN":0,
                        "family":self.install_spec.family,
                        "version":self.repository.get_image_version(software_image),
                        "versionType":self.install_spec.version_type,
                        "reboot":self.install_spec.reboot,
                        "sync":self.install_spec.sync},
                    "devices":self.repository.devices,
                    "deviceType":self.install_spec.device_type}
        upgrade_id = self.session.post_json(url,payload)
        return upgrade_id['id']
    

    def wait_for_completed(self, 
        sleep_seconds: int,timeout_seconds: int,
        expected_status: str,
        action_id : str):
        
        def check_status(action_data):
            return not action_data == expected_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_end_software_action():
            url = f'/dataservice/device/action/status/{action_id}'
            try:
                action_data = self.session.get_data(f'{url}')[0]['status']
                logger.debug(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ''

            return action_data

        wait_for_end_software_action()