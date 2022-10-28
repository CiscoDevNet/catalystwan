from vmngclient.dataclasses import DeviceInfo
from vmngclient.session import Session
from vmngclient.api.repository import Repository
from vmngclient.dataclasses import DeviceInfo
from typing import List
from vmngclient.dataclasses import DeviceSoftwareVersions

class PartitionManager:
    #TODO add clearing version method

    def __init__(self, session: Session, devices : List[DeviceInfo],
                 vmanage_image : str = '') -> None:
        
        self.vmanange_image = vmanage_image
        self.session = session
        self.devices = []
        self.devices_software_versions = Repository(self.session).get_devices_software_versions()
        
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
                    break
        return self.devices




        
