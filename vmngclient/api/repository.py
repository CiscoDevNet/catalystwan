import os
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.dataclasses import DeviceSoftwareVersions
from typing import List

class Repository:

    def __init__(self, session: Session, vmanage_image : str = ''):
        self.session = session
        self.vmanage_image = vmanage_image
    
    def get_image_version(self) -> str:
        
        version = ''
        url = '/dataservice/device/action/software/images?imageType=software'
        image_name = os.path.basename(self.vmanage_image)
        software_images = self.session.get_data(url)
        for img in software_images:
            if image_name in img['availableFiles']:
                version = img['versionName']
                break
        return version
   
    def get_devices_software_versions(self)-> List[DeviceSoftwareVersions] : 

        url = '/dataservice/system/device/controllers'
        devices = self.session.get_data(url)
        self.software_versions = []
        image_version = self.get_image_version()
        for device in devices:
            software_versions_object = create_dataclass(DeviceSoftwareVersions,device)
            software_versions_object.image_version = image_version
            self.software_versions.append(software_versions_object)
        return self.software_versions

