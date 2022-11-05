import os
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.dataclasses import DeviceInfo
from vmngclient.dataclasses import DeviceSoftwareRepository
from typing import List

class Repository:

    def __init__(self, session: Session,devices : List[DeviceInfo],
                  vmanage_image : str = ''):
        
        self.session = session
        self.vmanage_image = vmanage_image
        self.devices = []
 
        for dev in devices:
            dev_dict = dict()
            dev_dict['deviceId'] = dev.uuid
            dev_dict['deviceIP'] = dev.id
            self.devices.append(dev_dict)

    
    def get_image_version(self) -> str:
        
        image_version = ''
        url = '/dataservice/device/action/software/images?imageType=software'
        image_name = os.path.basename(self.vmanage_image)
        software_images = self.session.get_data(url)
        for img in software_images:
            if image_name in img['availableFiles']:
                image_version = img['versionName']
                break
        return image_version
   
    def create_controllers_versions_repository(self)-> dict[DeviceSoftwareRepository] : 

        url = '/dataservice/system/device/controllers'
        controllers_versions_info = self.session.get_data(url)
        self.controllers_versions_repository = {}
        for controller in controllers_versions_info:
            controller_obj = create_dataclass(DeviceSoftwareRepository,controller)
            self.controllers_versions_repository[controller_obj.device_id] = controller_obj
        return self.controllers_versions_repository

    def complete_device_list(self,version_to_set_up)-> None:
        
        for dev in self.devices:
            dev_available_versions = self.create_controllers_versions_repository()[dev['deviceId']].available_versions
            for available_version in dev_available_versions:
                if version_to_set_up in available_version:
                    dev['version'] = available_version
                    print (dev['version'])
                    break