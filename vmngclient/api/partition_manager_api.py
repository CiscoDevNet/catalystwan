from vmngclient.dataclasses import DeviceInfo
from vmngclient.session import Session
from vmngclient.api.repository import Repository
from vmngclient.dataclasses import DeviceInfo
from typing import List
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
import logging
from vmngclient.utils.creation_tools import get_logger_name

logger = logging.getLogger(get_logger_name(__name__))

class PartitionManager:

    def __init__(self, session: Session, devices : List[DeviceInfo],
                 vmanage_image : str = '') -> None:
        
        self.vmanange_image = vmanage_image
        self.session = session
        self.devices = []
        self.devices_software_versions = Repository(self.session, self.vmanange_image).get_devices_software_versions()
        
        for dev in devices:
            dev_dict = dict()
            dev_dict['deviceId'] = dev.uuid
            dev_dict['deviceIP'] = dev.id
            self.devices.append(dev_dict)

    def set_default_partition(self, version: str):
        
        self.complete_device_list(version)
        url = '/dataservice/device/action/defaultpartition'
        payload = {'action': 'defaultpartition',
                   'devices': self.devices,
                   'deviceType': 'vmanage'
                  }
        
        return self.session.post_json(url, payload)

    def remove_partition(self, version: str):
        
        self.complete_device_list(version)
        url = '/dataservice/device/action/removepartition'
        payload = {'action': 'removepartition',
                   'devices': self.devices,
                   'deviceType': 'vmanage'
                   }

        return self.session.post_json(url, payload)
    
    def complete_device_list(self, version : str):
        
        for dev in self.devices:
            for device in self.devices_software_versions:
                if device.device_id == dev['deviceId']:
                    dev['version'] = getattr(device,version)
                    if isinstance(dev['version'],list):
                        dev['version'] = dev['version'][0]
                    break
        return self.devices
    
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
        def wait_for_end_partition_action():
            status_api = f'/dataservice/device/action/status/{action_id}'
            
            try:
                action_data = self.session.get_data(f'{status_api}')[0]['status']
                logger.debug(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ''

            return action_data

        wait_for_end_partition_action()




        
