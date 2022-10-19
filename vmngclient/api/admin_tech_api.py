"""
Module for handling admintech logs for a device
"""
import json
import shutil
import time
from http.client import HTTPResponse
from pathlib import Path
from typing import List, Optional, cast
from urllib.error import HTTPError

from vmngclient.dataclasses import AdminTech
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass


class GenerateAdminTechLogError(Exception):
    pass


class RequestTokenIdNotFound(Exception):
    pass


class AdminTechApi:
    """Class for handling admintech logs for a device.

    Attributes:
        session: logged in API client session
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def get(self, device_id: str) -> AdminTech:
        """Gets admintech log information for a device.

        Args:
            device_id: device ID (usually system-ip)
        Returns:
            AdminTech object for given device
        """
        body = {'deviceIP': device_id}
        response = self.session.post_data('/dataservice/device/tools/admintechlist', data=body)
        return create_dataclass(AdminTech, response[0])

    def get_all(self) -> List[AdminTech]:
        """Gets admintech log information for all devices.

        Returns:
            AdminTech objects list for all devices
        """
        response = self.session.get_data('/dataservice/device/tools/admintechs')
        return [create_dataclass(AdminTech, dev_data) for dev_data in response]

    def generate(
        self, device_id: str, request_timeout: int = 3600, polling_timeout: int = 1200, polling_interval: int = 30
    ) -> str:
        """Generates admintech log for a device.

        Args:
            device_id: device ID (usually system-ip)
            request_timeout: wait time in seconds to generate admin tech after request
            polling_timeout: retry period in seconds for successfull request
            polling_interval: polling interval in seconds between request attempts
        Returns:
            filename of generated admintech log
        """
        create_admin_tech_error_msgs = 'Admin tech creation already in progress'
        body = {'deviceIP': device_id, 'exclude-cores': True, 'exclude-tech': False, 'exclude-logs': True}
        _session_timeout = self.session.timeout
        polling_timer = polling_timeout
        while polling_timer > 0:
            try:
                self.session.timeout = request_timeout
                response = self.session.post_json('/dataservice/device/tools/admintech', body)
                return cast(dict, response)['fileName']
            except HTTPError as error:
                error_details = error.read().decode()
                if error.code != 400 and create_admin_tech_error_msgs not in json.loads(error_details).get('error').get(
                    'details'
                ):
                    raise GenerateAdminTechLogError(f'It is not possible to generate admintech log for {device_id}')
                time.sleep(polling_interval)
                polling_timer -= polling_interval
            finally:
                self.session.timeout = _session_timeout
        raise GenerateAdminTechLogError(f'It is not possible to generate admintech log for {device_id}')

    def _get_token_id(self, device_id) -> str:
        admin_tech_filename = self.generate(device_id)
        admin_techs = self.get_all()
        for admin_tech in admin_techs:
            if admin_tech_filename == admin_tech.filename:
                return admin_tech.token_id
        raise RequestTokenIdNotFound(f'Request Id of admin tech generation request not found for device: {device_id}')

    def delete(self, device_id: str) -> HTTPResponse:
        """Deletes admin tech logs for a device.

        Args:
            device_id: device ID (usually system-ip)
        Returns:
            response: http response for delete operation
        """

        token_id = self._get_token_id(device_id)
        response = self.session.delete(f'/dataservice/device/tools/admintech/{token_id}')
        return response

    def download(self, admin_tech_name: str, download_dir: Optional[Path] = None) -> Path:
        """Downloads admintech log for a device.

        Args:
            admin_tech_name: name of admin_tech file
            download_dir: download directory (defaults to current working directory)
        Returns:
            path to downloaded admin_tech file
        """
        if not download_dir:
            download_dir = Path.cwd()
        download_path = download_dir / admin_tech_name
        with self.session.get(f'/dataservice/device/tools/admintech/download/{admin_tech_name}') as payload:
            with open(download_path, 'wb') as file:
                shutil.copyfileobj(payload, file)
        return download_path
