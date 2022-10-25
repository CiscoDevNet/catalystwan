from vmngclient.dataclasses import DeviceInfo, InstallSpec
from vmngclient.session import Session
from vmngclient.api.repository import Repository
from typing import List
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.api.partition_manager_api import PartitionManager
import logging

logger = logging.getLogger(get_logger_name(__name__))

class VmanageUpgradeApi:
    # TODO 1: add rollback option if it's api endpoint
    # TODO 2: add logging
    # TODO 3: Ask about timeouts

    def __init__(self,vmanage_image : str, session: Session,
                 partition_manager : PartitionManager,
                 install_spec: InstallSpec):

        self.vmanage_image = vmanage_image
        self.session = session
        self.devices = partition_manager.devices
        self.install_spec = install_spec

    def upgrade_vmanage (self):
        
        api = '/device/action/install'
        payload = {
            'action': 'install',
            'input': {
                'vEdgeVPN': 0,
                'vSmartVPN': 0,
                'data': [
                    {
                        'family': self.install_spec.family,
                        'version': Repository(self.session, self.vmanage_image).get_image_version(),
                    }
                ],
                'versionType': self.install_spec.version_type,
                'reboot': self.install_spec.reboot,
                'sync': self.install_spec.sync,
            },
            'devices': self.devices,
            'deviceType': self.install_spec.device_type,
        }

        self.session.get_data(api,payload)

    def activate_vmanage(self):

        api = '/device/action/changepartition'
        payload = {'action': 'changepartition',
                   'devices': self.devices,
                   'deviceType': 'vmanage'
                   }
        self.session.post_data(api, payload)
