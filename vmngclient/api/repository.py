import os
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.dataclasses import SoftwareVersions

class Repository:

    def __init__(self, session: Session, vmanage_image : str = ''):
        self.session = session
        self.vmanage_image = vmanage_image
    
    def get_image_version(self) -> str:
        
        '''
        The image name in several cases doesn't contain whole image version.
        It's necessary to get the version from vManage which shows whole version.

        @param image: the image name
        '''
        version = ''
        url = '/dataservice/device/action/software/images?imageType=software'
        image_name = os.path.basename(self.vmanage_image)
        software_images = self.session.get_data(url)
        for img in software_images:
            if image_name in img['availableFiles']:
                version = img['versionName']
                break
        return version
   
    def get_all_software_versions(self):
        #Maybe create dataclass for that?
        # url = '/dataservice/system/device/controllers'
        
        # devices_versions = dict()
        # devices = self.session.get_data(url)
        # for dev in devices:
        #     versions_dict = dict()
        #     versions_dict['availableVersions'] = [version for version in
        #                                           dev['availableVersions']]
        #     versions_dict['currentVersion'] = dev['version']
        #     versions_dict['defaultVersion'] = dev['defaultVersion']
        #     versions_dict['UpgradeVersion'] = self.get_image_version()
        #     devices_versions[dev['uuid']] = versions_dict
        
        # return devices_versions

        url = '/dataservice/system/device/controllers'
        devices = self.session.get_data(url)
        self.software_versions = []
        upgrade_version = self.get_image_version()
        for device in devices:
            software_versions_object = create_dataclass(SoftwareVersions,device)
            software_versions_object.upgrade_version = upgrade_version
            self.software_versions.append(software_versions_object)
        return self.software_versions

