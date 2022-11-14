from vmngclient.session import Session
from vmngclient.api.repository_api import Repository
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
import logging
from vmngclient.utils.creation_tools import get_logger_name

logger = logging.getLogger(get_logger_name(__name__))

class PartitionManager:

    def __init__(self, session: Session, repository : Repository,
                 ) -> None:        
        self.session = session
        self.repository = repository

    def set_default_partition(self, version_to_default: str)-> str:
        
        self.repository.complete_device_list(version_to_default, 'installed_versions')
        url = '/dataservice/device/action/defaultpartition'
        payload = {'action': 'defaultpartition',
                   'devices': self.repository.devices,
                   'deviceType': 'vmanage'
                  }
        set_default = dict(self.session.post_json(url, payload))
        return set_default['id']

    def remove_partition(self, version_to_remove: str)-> str:
        
        self.repository.complete_device_list(version_to_remove, 'available_versions')
        url = '/dataservice/device/action/removepartition'
        payload = {'action': 'removepartition',
                   'devices': self.repository.devices,
                   'deviceType': 'vmanage'
                   }

        remove_action = dict(self.session.post_json(url, payload))
        return remove_action['id']
    
    def wait_for_completed(self, 
        sleep_seconds: int,timeout_seconds: int,
        exit_statuses: str,
        action_id : str) -> None:
        
        def check_status(action_data):
            return not action_data in (exit_statuses)

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_end_software_action():
            url = f'/dataservice/device/action/status/{action_id}'
            try:
                action_data = self.session.get_data(url)[0]['status']
                logger.debug(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ''

            return action_data

        wait_for_end_software_action()





        
