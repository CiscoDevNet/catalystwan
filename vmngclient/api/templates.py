import json
import logging
import time
from enum import Enum
from typing import Dict, List, Union

from attrs import frozen

from vmngclient.dataclasses import DeviceInfo, TemplateData
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass, get_logger_name

logger = logging.getLogger(get_logger_name(__name__))


class TemplateNotFoundError(Exception):
    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class OperationStatus(Enum):
    IN_PROGRESS = 'In progress'
    FAILURE = 'Failure'
    SUCCESS = 'Success'


@frozen
class OperationInformation:
    activity: List[str]
    status: OperationStatus


class TemplateAPI:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_template_list(self) -> List[TemplateData]:
        data = self.session.get_data("/dataservice/template/device")
        return [create_dataclass(TemplateData, template) for template in data]

    def get_template_id(self, template_name: str) -> str:
        templates = self.get_template_list()
        for template in templates:
            if template_name == template.name:
                return template.template_id
        raise TemplateNotFoundError(template_name)

    def wait_until_operation_complete(self, operation_id: str, timeout: int = 300) -> bool:
        operation_status = self.get_operation_status(operation_id)
        # logger.debug(json.dumps(self.get_request_status(operation_id), indent=4))
        logger.debug(operation_status)
        while any(filter(lambda x: x == OperationStatus.IN_PROGRESS, operation_status)):
            logger.debug("Operation(s) in progress.")
            time.sleep(30)
            operation_status = self.get_operation_status(operation_id)
            logger.debug(operation_status)
        # if operation_status == OperationStatus.SUCCESS:
        #     return True
        # elif operation_status == OperationStatus.FAILURE:
        

        logger.debug(json.dumps(self.get_request_status(operation_id)['data'], indent=4))
        return False

    def tt(self):
        payload = {
            "templateId": "dfb831c4-f0a3-4f28-b24a-0912f8c849e8",
            "device": {
                "csv-status": "complete",
                "csv-deviceId": "C8K-eb40c692-e2fd-4c91-9d0e-f577a5af5117",
                "csv-deviceIP": "172.16.254.5",
                "csv-host-name": "vm6",
                "csv-templateId": "dfb831c4-f0a3-4f28-b24a-0912f8c849e8",
            },
        }

        r = self.session.post(url="/dataservice/template/device/config/config", data=payload)
        return r

    def generate_device_input(self, template_id: str, device_id: str):
        payload = {
            "templateId": template_id,
            "deviceIds": [device_id],
        }
        return self.session.post_data("/dataservice/template/device/config/input", data=payload)[0]

    def attach_cli_template(self, template_ids, devices: Union[List[DeviceInfo], DeviceInfo]) -> str:
        if isinstance(devices, DeviceInfo):
            devices = list(devices)
        devices_input = [
            self.generate_device_input(template_id, device.uuid) for template_id, device in zip(template_ids, devices)
        ]
        device_template_list = [
            {"templateId": template_id, "device": [device_input]}
            for template_id, device_input in zip(template_ids, devices_input)
        ]

        endpoint = "/dataservice/template/device/config/attachcli"
        logger.debug(json.dumps(device_template_list, indent=4))
        payload = {"deviceTemplateList": device_template_list}
        request_id = self.session.post_json(endpoint, payload)
        logger.debug(f"Request id: {request_id}")
        return request_id['id']

    def get_operation_information(self, id: str) -> List[Dict[str, str]]:
        endpoint = f"/dataservice/device/action/status/{id}"
        return self.session.get_json(endpoint)

    def get_operation_status(self, operation_id: str) -> List[OperationStatus]:
        return [OperationStatus(status['status']) for status in self.get_operation_information(operation_id)['data']]

    def get(self, template_name: str) -> TemplateData:
        templates = self.get_template_list()
        for template in templates:
            if template_name == template.name:
                return template
        raise TemplateNotFoundError(template_name)
