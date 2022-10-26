from vmngclient.dataclasses import DeviceInfo
from vmngclient.session import Session
from vmngclient.api.repository import Repository
from vmngclient.dataclasses import DeviceInfo
from typing import List

class PartitionManager:

    def __init__(self, session: Session, devices : List[DeviceInfo],
                 vmanage_image : str = '') -> None:
        
        self.vmanange_image = vmanage_image
        self.session = session
        self.devices = []
        self.all_software_versions = Repository(self.session).get_all_versions()
        
        for dev in devices:
            dev_dict = dict()
            dev_dict['deviceId'] = dev.uuid
            dev_dict['deviceIP'] = dev.id
            self.devices.append(dev_dict)

    def set_default_partition(self, version: str):

        for dev in self.devices:
            dev['version'] = self.all_software_versions[dev['deviceId']][version]
            
        print (self.devices)
        url = '/dataservice/device/action/defaultpartition'
        payload = {'action': 'defaultpartition',
                   'devices': self.devices,
                   'deviceType': 'vmanage'
                  }

        return self.session.post_json(url, payload)

    def remove_available_partition(self):
        
        for dev in self.devices:
            dev['version'] = self.all_software_versions["availableVersions"]

        url = '/dataservice/device/action/removepartition'
        payload = {'action': 'removepartition',
                   'devices': self.devices,
                   'deviceType': 'vmanage'
                   }
        return self.session.post_data(url, payload)
    

        
