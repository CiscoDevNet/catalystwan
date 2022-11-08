import logging
from typing import List, cast

from ciscoconfparse import CiscoConfParse  # type: ignore
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from vmngclient.dataclasses import DeviceInfo, Template
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass, get_logger_name
from vmngclient.utils.device_model import DeviceModel
from vmngclient.utils.operation_status import OperationStatus

logger = logging.getLogger(get_logger_name(__name__))


class TemplateNotFoundError(Exception):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class TemplateExist(Exception):
    """Used when a template item is exist."""

    def __init__(self, name):
        self.message = f"Template with that name '{name}' exists."


class TemplateAttached(Exception):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateAPI:
    """TemplateAPI."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @property
    def templates(self) -> List[Template]:
        """Templates.

        Returns:
            List[Template]: List of existing templates.
        """
        endpoint = "/dataservice/template/device"
        data = self.session.get_data(endpoint)
        return [create_dataclass(Template, template) for template in data]

    def get(self, name: str) -> Template:
        """Get template.

        Args:
            name (str): Name of template.

        Raises:
            TemplateNotFoundError: If template does not exist.

        Returns:
            Template: Selected template.
        """
        for template in self.templates:
            if name == template.name:
                return template
        raise TemplateNotFoundError(name)

    def get_id(self, name: str) -> str:
        """Get id template.

        Args:
            name (str): Name of template to get id.

        Returns:
            str: Template id.
        """
        return self.get(name).id

    def wait_complete(self, operation_id: str, timeout_seconds: int = 300, sleep_seconds: int = 5) -> bool:
        """Wait to complete action.

        Args:
            operation_id (str): Id of the action waiting for completion.
            timeout_seconds (int, optional): Time for completion. Defaults to 300.
            sleep_seconds (int, optional): Sleep time between repetitions. Defaults to 5.

        Returns:
            bool: True if acction status is successful, otherwise - False.
        """

        def check_status(action_data):
            if action_data:
                list_action = [action == OperationStatus.SUCCESS for action in action_data]
                return not all(list_action)
            else:
                return True

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_status():
            return self.__get_operation_status(operation_id)

        return True if wait_for_status() else False

    def attach(self, name: str, device: DeviceInfo) -> bool:
        """Attach template to device.

        Args:
            name (str): Template name to attached.
            device (DeviceInfo): Device to attach template.

        Returns:
            bool: True if attaching template is successful, otherwise - False.
        """
        templateId = self.get_id(name)
        payload = {
            "deviceTemplateList": [
                {
                    "templateId": templateId,
                    "device": [
                        {
                            "csv-status": "complete",
                            "csv-deviceId": device.uuid,
                            "csv-deviceIP": device.id,
                            "csv-host-name": device.hostname,
                            "csv-templateId": templateId,
                        }
                    ],
                }
            ]
        }
        endpoint = "/dataservice/template/device/config/attachcli"
        response = cast(dict, self.session.post_json(url=endpoint, data=payload))
        return self.wait_complete(response['id'])

    def device_to_cli(self, device: DeviceInfo) -> bool:
        """Device mode to Cli.

        Args:
            device (DeviceInfo): Device to chcange mode.

        Returns:
            bool: True if change mode to cli is successful, otherwise - False.
        """
        payload = {"deviceType": device.personality, "devices": [{"deviceId": device.uuid, "deviceIP": device.id}]}
        endpoint = "/dataservice/template/config/device/mode/cli"
        response = cast(dict, self.session.post_json(url=endpoint, data=payload))
        return self.wait_complete(response['id'])

    def __get_operation_status(self, operation_id: str) -> List[OperationStatus]:
        """Get operatrion status.

        Args:
            operation_id (str): Operatrion id.

        Returns:
            List[OperationStatus]: List of operations.
        """
        endpoint = f"/dataservice/device/action/status/{operation_id}"
        response = cast(list, self.session.get_data(endpoint))
        return [OperationStatus(status['status']) for status in response]

    def delete(self, name: str) -> bool:
        """Delete template.

        Args:
            name (str): Name template to delete.

        Raises:
            TemplateAttached: If template is attached to device.

        Returns:
            bool: True if deletion is successful, otherwise - False.
        """
        template = self.get(name)
        endpoint = f"/dataservice/template/device/{template.id}"
        if template.devices_attached == 0:
            response = self.session.delete(url=endpoint)
            return response.status == 200
        raise TemplateAttached(template.name)

    def create(self, device_model: DeviceModel, name: str, description: str, config: CiscoConfParse) -> str:
        """Create template.

        Args:
            device_model (DeviceModel): Device model to create template.
            name (str): Name template to create.
            description (str): Description template to create.
            config (CiscoConfParse): The config to device.

        Returns:
            str: Id of the created template.
        """
        try:
            self.get(name)
            raise TemplateExist(name)
        except TemplateNotFoundError:
            cli_template = CliTemplate(self.session, device_model, name, description)
            cli_template.config = config
            return cli_template.send_to_device()


class CliTemplate:
    """Cli Template."""

    def __init__(self, session: Session, device_model: DeviceModel, name: str, description: str) -> None:
        self.session = session
        self.device_model = device_model
        self.name = name
        self.description = description
        self.config: CiscoConfParse = CiscoConfParse([])

    def load(self, id: str) -> None:
        """Load config from template.

        Args:
            id (str): The template id from which load config.
        """
        endpoint = f"/dataservice/template/device/object/{id}"
        config = cast(dict, self.session.get_json(endpoint))
        self.config = CiscoConfParse(config['templateConfiguration'].splitlines())

    def load_running(self, device: DeviceInfo) -> None:
        """Load running config from device.

        Args:
            device (DeviceInfo): The device from which load config.
        """
        endpoint = f"/dataservice/template/config/running/{device.uuid}"
        config = cast(dict, self.session.get_json(endpoint))
        self.config = CiscoConfParse(config['config'].splitlines())

    def send_to_device(self) -> str:
        """Send CLI template to device.

        Returns:
            str: Template id.
        """
        config_p = "\n".join(self.config.ioscfg)
        payload = {
            "templateName": self.name,
            "templateDescription": self.description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_p,
            "factoryDefault": False,
            "configType": "file",
        }
        endpoint = "/dataservice/template/device/cli/"
        response = cast(dict, self.session.post_json(url=endpoint, data=payload))
        return response['templateId']

    def update(self, id: str) -> None:
        """Update CLI template.

        Args:
            id (str): Template id to update.

        Returns:
            str: Process id.
        """
        config_p = "\n".join(self.config.ioscfg)
        payload = {
            "templateId": id,
            "templateName": self.name,
            "templateDescription": self.description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_p,
            "factoryDefault": False,
            "configType": "file",
            "draftMode": False,
        }
        endpoint = f"/dataservice/template/device/{id}"
        cast(dict, self.session.put_json(url=endpoint, data=payload))

    def add_to_config(self, add_config: CiscoConfParse, add_before: str) -> None:
        """Adding config to exist config before existing value.

        Args:
            add_config (CiscoConfParse): Config to added.
            add_before (str): The value before which to add config.
        """
        for comand in add_config.ioscfg:
            self.config.ConfigObjs.insert_before(add_before, comand, atomic=True)
