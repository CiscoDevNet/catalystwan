from vmngclient.dataclasses import DeviceInfo, InstallSpec
from vmngclient.api.device_action_api import DeviceActionApi
from vmngclient.api.basic_api import DeviceStateApi
from vmngclient.session import Session
from vmngclient.api.repository import Repository
from typing import List
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.api.partition_manager_api import PartitionManager
import logging
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

logger = logging.getLogger(get_logger_name(__name__))


class VmanageUpgradeApi:
    # TODO 1: add rollback option if it's api endpoint
    # TODO 2: add logging
    # TODO 3: Ask about timeouts

    def __init__(self, session: Session,
                 partition_manager : PartitionManager,
                 install_spec: InstallSpec):

        self.session = session
        self.partition_manager = partition_manager
        self.install_spec = install_spec

    def upgrade_vmanage (self):
        
        url = '/dataservice/device/action/install'
        payload = {
            'action': 'install',
            'input': {
                'vEdgeVPN': 0,
                'vSmartVPN': 0,
                'family': self.install_spec.family,
                'version': Repository(self.session, self.partition_manager.vmanange_image).get_image_version(),
                'versionType': self.install_spec.version_type,
                'reboot': self.install_spec.reboot,
                'sync': self.install_spec.sync,
            },
            'devices': self.partition_manager.devices,
            'deviceType': self.install_spec.device_type,
        }


        upgrade_id = self.session.post_json(url,payload)
        return upgrade_id['id']

    def activate_vmanage(self):

        self.completed_devices_list = self.partition_manager.complete_device_list('available_versions')
        url = '/dataservice/device/action/changepartition'
        payload = {'action': 'changepartition',
                   'devices': self.completed_devices_list,
                   'deviceType': 'vmanage'
                   }


        activate_id = self.session.post_json(url, payload)
        return activate_id['id'] 

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
            status_api = f'/dataservice/device/action/status/{action_id}'
            
            try:
                action_data = self.session.get_data(f'{status_api}')[0]['status']
                logger.debug(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ''

            return action_data

        wait_for_end_software_action()