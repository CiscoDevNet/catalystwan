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
        for dev in devices:
                dev_dict = dict()
                dev_dict['deviceIP'] = dev.local_system_ip
                dev_dict['deviceId'] = dev.uuid
                self.devices.append(dev_dict)

    def set_default_partition(self):

        for dev in self.devices:
            dev['version'] = self.get_all_versions["current"]
        url = '/device/action/defaultpartition'
        payload = {'action': 'defaultpartition',
                   'devices': self.devices ,
                   'deviceType': 'vmanage'
                   }
        return self.session.post_data(url, payload)
    
    def remove_available_partition(self):
        
        # u is for unicode, have to checkout if it's unneccessary
        for dev in self.devices:
            dev['version'] = self.get_all_versions["current"]

        url = '/device/action/removepartition'
        payload = {'action': 'removepartition',
                   'devices': self.devices,
                   'deviceType': 'vmanage'
                   }
        return self.session.post_data(url, payload)
    

        
