from vmngclient.session import Session
from vmngclient.utils.creation_tools import get_logger_name
import logging


logger = logging.getLogger(get_logger_name(__name__))

class SettingsApi:
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get_organization_name(self) -> str:
        response = self.session.get_data("/dataservice/settings/configuration/organization")
        organization_name = ""
        try:
            organization_name = response[0]["org"]
        except KeyError:
            logger.info("Organization name is not set.")
        return organization_name
    
    def set_organization_name(self, name: str) -> bool:
        response = self.session.put("/dataservice/settings/configuration/organization")
        