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
        #just upgrade here

        self.set_default_partition()
        self.remove_available_partition()
