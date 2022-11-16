"""
Module for handling admintech logs for a device
"""
import json
import time
from pathlib import Path
from typing import List, Optional, cast
from urllib.error import HTTPError

from requests import Response

from vmngclient.dataclasses import AdminTech
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass


class GenerateAdminTechLogError(Exception):
    pass


class DownloadAdminTechLogError(Exception):
    pass


class RequestTokenIdNotFound(Exception):
    pass


class AdminTechAPI:
    """Class for handling admintech logs for a device.

    Attributes:
        session: logged in API client session
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def get(self, device_id: str) -> List[AdminTech]:
        """Gets admintech log information for a device.

        Args:
            device_id: device ID (usually system-ip)
        Returns:
            AdminTech object list for given device
        """
        body = {"deviceIP": device_id}
        response = self.session.post(url="/dataservice/device/tools/admintechlist", data=body).json()
        return [create_dataclass(AdminTech, data) for data in response]

    def get_all(self) -> List[AdminTech]:
        """Gets admintech log information for all devices.

        Returns:
            AdminTech objects list for all devices
        """
        response = self.session.get_data("/dataservice/device/tools/admintechs")
        return [create_dataclass(AdminTech, data) for data in response]

    def generate(
        self,
        device_id: str,
        exclude_cores: bool = True,
        exclude_tech: bool = False,
        exclude_logs: bool = True,
        request_timeout: int = 3600,
        polling_timeout: int = 1200,
        polling_interval: int = 30,
    ) -> str:
        """Generates admintech log for a device.

        Args:
            device_id: device ID (usually system-ip)
            exclude_cores: exclude core in generated admintech log file
            exclude_tech: exclude core in generated admintech log file
            exclude_logs: exclude core in generated admintech log file
            request_timeout: wait time in seconds to generate admintech after request
            polling_timeout: retry period in seconds for successfull request
            polling_interval: polling interval in seconds between request attempts
        Returns:
            filename of generated admintech log
        """
        create_admin_tech_error_msgs = "Admin tech creation already in progress"
        body = {
            "deviceIP": device_id,
            "exclude-cores": exclude_cores,
            "exclude-tech": exclude_tech,
            "exclude-logs": exclude_logs,
        }
        polling_timer = polling_timeout
        while polling_timer > 0:
            try:
                self.session.timeout = request_timeout
                response = self.session.post_json('/dataservice/device/tools/admintech', body)
                return cast(dict, response)['fileName']
            except HTTPError as error:
                error_details = error.read().decode()
                if error.code != 400 and create_admin_tech_error_msgs not in json.loads(error_details).get("error").get(
                    "details"
                ):
                    raise GenerateAdminTechLogError(f"It is not possible to generate admintech log for {device_id}")
                time.sleep(polling_interval)
                polling_timer -= polling_interval
            finally:
                self.session.timeout = _session_timeout
        raise GenerateAdminTechLogError(f'It is not possible to generate admintech log for {device_id}')

    def _get_token_id(self, filename: str) -> str:
        admin_techs = self.get_all()
        for admin_tech in admin_techs:
            if filename == admin_tech.filename:
                return admin_tech.token_id
        raise RequestTokenIdNotFound(
            f"requestTokenId of admin tech generation request not found for file name: {filename}"
        )

    def delete(self, filename: str) -> Response:
        """Deletes admin tech logs for a device.

        Args:
            filename: name of admin_tech file
        Returns:
            response: http response for delete operation
        """

        token_id = self._get_token_id(filename)
        response = self.session.delete(f"/dataservice/device/tools/admintech/{token_id}")
        return response

    def download(self, filename: str, download_dir: Optional[Path] = None) -> Path:
        """Downloads admintech log for a device.

        Args:
            filename: name of admin_tech file
            download_dir: download directory (defaults to current working directory)
        Returns:
            path to downloaded admin_tech file
        """
        if not download_dir:
            download_dir = Path.cwd()
        download_path = download_dir / filename
        url = f"/dataservice/device/tools/admintech/download/{filename}"
        if self.session.get_file(url=url, filename=download_path).status_code != 200:
            raise GenerateAdminTechLogError(f"Cannot download admin tech file: {filename} from remote")
        return download_path
