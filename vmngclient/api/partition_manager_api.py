class PartitionManager:

    def set_default_partition(self):

        #move to __init__
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
        
        # u is for unicode
        self.devs = []
        for dev in self.devices:
                dev_dict = dict()
                dev_dict['deviceIP'] = dev.local_system_ip
                dev_dict['version'] = self.all_versions["default"]
                dev_dict['deviceId'] = dev.uuid
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