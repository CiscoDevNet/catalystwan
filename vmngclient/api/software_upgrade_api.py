from vmngclient.session import Session
from vmngclient.api.repository_api import Repository
from typing import List, Union
from vmngclient.utils.creation_tools import get_logger_name
import logging
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from attr import define
from enum import Enum
# from vmngclient.api.software_upgrade_api import InstallSpecification

logger = logging.getLogger(get_logger_name(__name__))

class Family(Enum):
    CEDGE = 'vedge'
    VBOND = 'vedge'
    VEDGE = 'vedge'
    VSMART = 'vedge'
    VMANAGE = 'vmanage'

class VersionType(Enum):
    VSMART = 'vmanage'
    VBOND = 'vmanage'
    VEDGE = 'vmanage'
    CEDGE = 'vmanage'
    VMANAGE = 'vmanage'

class DeviceType(Enum):
    VSMART = 'controller'
    VBOND = 'controller'
    VEDGE = 'vedge'
    CEDGE = 'vedge'
    VMANAGE = 'vmanage'

@define
class InstallSpecification:
    """Class to keep installation specification"""

    family: Family 
    version_type: VersionType
    device_type: DeviceType


class SoftwareUpgradeApi:

    def __init__(self, session: Session,
                 repository = Repository) -> None:
        self.session = session
        self.repository = repository

    def activate_software(self,version_to_activate: str) -> str:
        
        self.repository.complete_device_list(version_to_activate)
        url = '/dataservice/device/action/changepartition'
        payload = {'action': 'changepartition',
                   'devices': self.repository.devices,
                   'deviceType': 'vmanage',
                  }
        activate = self.session.post_json(url, payload)
        return activate['id']
    
    def upgrade_software(self, software_image: str, install_spec: InstallSpecification,
                         reboot : bool, sync: bool = True) -> str:
        self.install_spec = install_spec

        url = '/dataservice/device/action/install'
        payload = {"action":"install",
                   "input":{
                        "vEdgeVPN":0,
                        "vSmartVPN":0,
                        "family":self.install_spec.family,
                        "version":self.repository.get_image_version(software_image),
                        "versionType":self.install_spec.version_type,
                        "reboot":reboot,
                        "sync":sync},
                    "devices":self.repository.devices,
                    "deviceType":self.install_spec.device_type
                    }
        
        if self.install_spec.family in (Family.VMANAGE.value, Family.CEDGE.value):
            incorrect_devices = self.downgrade_check(payload['input']['version'],
                                self.repository.device_category)
            if incorrect_devices:
                raise ValueError(
                f'Current version of devices {incorrect_devices} is higher than upgrade version. Acion denied!')
        upgrade = self.session.post_json(url,payload)
        return upgrade['id']
    
    
    def downgrade_check(self, version_to_upgrade : str,
                 devices_category: InstallSpecification) -> Union[None,List]:

        for dev in self.repository.devices:
            incorrect_devices = []
            dev_current_version = self.repository.create_devices_versions_repository()[dev['deviceId']].current_version
            version_to_upgrade = version_to_upgrade.split('.')
            for priority, label in enumerate(dev_current_version.split('.')):
                if str(label) > str(version_to_upgrade[priority]):
                    if devices_category == 'vmanages' and label == 2:
                       continue
                    incorrect_devices.append(dev['deviceId'])
                    break
        if incorrect_devices == []:
            return None
        else:
            return incorrect_devices

                                                                             
    

    def wait_for_completed(self, 
        sleep_seconds: int,timeout_seconds: int,
        expected_status: str,
        action_id : str) -> None:
        
        def check_status(action_data):
            return not action_data in (expected_status,'Failure')

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_end_software_action():
            url = f'/dataservice/device/action/status/{action_id}'
            try:
                action_data = self.session.get_data(url)[0]['status']
                logger.debug(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ''

            return action_data

        wait_for_end_software_action()


