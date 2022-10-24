from vmngclient.api.basic_api import DevicesApi, DeviceStateApi
from vmngclient.dataclasses import DeviceInfo
from vmngclient.session import Session
from typing import List
from vmngclient.utils.creation_tools import get_logger_name
import os
import logging

logger = logging.getLogger(get_logger_name(__name__))

class VmanageUpgradeApi:
    # TODO: add rollback option if it's api endpoint
    # TODO: add logging

    def __init__(self,vmanage_image : str, session: Session, devices: List[DeviceInfo]):
        self.vmanage_image = vmanage_image
        # self.version_to_set = Repository(session).get_image_version()
        self.all_versions = get_all_versions(self)
        self.session = session
        self.devices = devices

    def upload_vmanage_image (self):

        "have to wait for request lib case resolve"
    
    def upgrade_vmanage (self):

        self.set_default_partition()
        self.remove_available_partition()


    def set_default_partition(self):
        
        #raw version of self.devs, have to write it prettier
        self.devs = []
        for dev in self.devices:
                dev_dict = dict()
                dev_dict['deviceIP'] = dev.local_system_ip
                dev_dict['version'] = self.all_versions["current"]
                dev_dict['deviceId'] = dev.uuid
                self.devs.append(dev_dict)

        url = '/device/action/defaultpartition'
        payload = {'action': 'defaultpartition',
                   'devices': self.devs ,
                   'deviceType': 'vmanage'
                   }
        return self.session.post_data(url, payload)
    
    def remove_available_partition(self):

        
        self.devs = []
        for dev in self.devices:
                dev_dict = dict()
                dev_dict['deviceIP'] = {dev.local_system_ip}
                dev_dict['version'] = self.all_versions["default"]
                dev_dict['deviceId'] = {dev.uuid}
                self.devs.append(dev_dict)

        url = '/device/action/removepartition'
        payload = {'action': 'removepartition',
                   'devices': self.devs,
                   'deviceType': 'vmanage'
                   }
        return self.session.post_data(url, payload)
    
    def get_all_versions(self):
        url = '/system/device/controllers'
        versions = {'deviceId' :{'availableVersions':['ver1','ver2'], 
                                  'defaultVersions':['ver1','ver2'],
                                  'toInstallVersion':[self.get_image_version()]} }
        
    
        """
        3. Install software (use endpoint from software_upgrade from vmanagehttp.py), 
           have to create dataclass InstallSpecification
        4. Activate (many actions here)
        """

# maybe remove Repository class and input get_image_version into VmanageupgradeApi?
class Repository:

    def __init__(self, session: Session, vmanage_image : str):
        self.session = session
        self.vmanage_image = vmanage_image
    
    def get_image_version(self) -> str:
        
        '''
        The image name in several cases doesn't contain whole image version.
        It's necessary to get the version from vManage which shows whole version.

        @param image: the image name
        '''
        version = ''
        url = '/device/action/software/images?imageType=software'
        image_head = os.path.basename(self.vmanage_image)
        software_images = self.session.get_data(url)

        for img in software_images:
            if image_head in img['availableFiles']:
                version = img['versionName']
                break
        return version