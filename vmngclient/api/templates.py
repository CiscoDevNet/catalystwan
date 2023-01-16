import json
import logging
from difflib import Differ
from enum import Enum
from typing import List

from ciscoconfparse import CiscoConfParse  # type: ignore
from requests.exceptions import HTTPError

from vmngclient.api.task_status_api import wait_for_completed
from vmngclient.dataclasses import Device, Template
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.device_model import DeviceModel
from vmngclient.utils.operation_status import OperationStatus

logger = logging.getLogger(__name__)


class TemplateType(Enum):
    CLI = "file"
    FEATURE = "template"


class NotFoundError(Exception):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class NameAlreadyExistError(Exception):
    """Used when a template item exists."""

    def __init__(self, name):
        self.message = f"Template with that name '{name}' exists."


class AttachedError(Exception):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateTypeError(Exception):
    """Used when wrong type template."""

    def __init__(self, name):
        self.message = f"Template: {name} - wrong template type."


class TemplateAPI:
    def __init__(self, session: vManageSession) -> None:
        self.session = session

    @property
    def templates(self) -> List[Template]:
        """

        Returns:
            List[Template]: List of existing templates.
        """
        endpoint = "/dataservice/template/device"
        data = self.session.get_data(endpoint)
        return [create_dataclass(Template, template) for template in data]

    def get(self, name: str) -> Template:
        """

        Args:
            name (str): Name of template.

        Raises:
            NotFoundError: If template does not exist.

        Returns:
            Template: Selected template.
        """
        for template in self.templates:
            if name == template.name:
                return template
        raise NotFoundError(name)

    def get_id(self, name: str) -> str:
        """

        Args:
            name (str): Name of template to get id.

        Returns:
            str: Template id.
        """
        return self.get(name).id

    def attach(self, name: str, device: Device) -> bool:
        """

        Args:
            name (str): Template name to attached.
            device (Device): Device to attach template.

        Returns:
            bool: True if attaching template is successful, otherwise - False.
        """
        try:
            template_id = self.get_id(name)
            self.template_validation(template_id, device=device)
        except NotFoundError:
            logger.error(f"Error, Template with name {name} not found on {device}.")
            return False
        except HTTPError as error:
            error_details = json.loads(error.response.text)
            logger.error(f"Error in config: {error_details['error']['details']}.")
            return False
        payload = {
            "deviceTemplateList": [
                {
                    "templateId": template_id,
                    "device": [
                        {
                            "csv-status": "complete",
                            "csv-deviceId": device.uuid,
                            "csv-deviceIP": device.id,
                            "csv-host-name": device.hostname,
                            "csv-templateId": template_id,
                        }
                    ],
                }
            ]
        }
        endpoint = "/dataservice/template/device/config/attachcli"
        logger.info(f"Attaching a template: {name} to the device: {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        task = wait_for_completed(session=self.session, action_id=response["id"])
        if task.status == OperationStatus.SUCCESS.value:
            return True
        logger.warning(f"Failed to attach tempate: {name} to the device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.activity}")
        return False

    def device_to_cli(self, device: Device) -> bool:
        """

        Args:
            device (Device): Device to change mode.

        Returns:
            bool: True if change mode to cli is successful, otherwise - False.
        """
        payload = {
            "deviceType": device.personality.value,
            "devices": [{"deviceId": device.uuid, "deviceIP": device.id}],
        }
        endpoint = "/dataservice/template/config/device/mode/cli"
        logger.info(f"Changing mode to cli mode for {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        task = wait_for_completed(session=self.session, action_id=response["id"])
        if task.status == OperationStatus.SUCCESS.value:
            return True
        logger.warning(f"Failed to change to cli mode for device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.activity}")
        return False

    def delete(self, name: str) -> bool:
        """

        Args:
            name (str): Name template to delete.

        Raises:
            AttachedError: If template is attached to device.

        Returns:
            bool: True if deletion is successful, otherwise - False.
        """
        template = self.get(name)
        endpoint = f"/dataservice/template/device/{template.id}"
        if template.devices_attached == 0:
            response = self.session.delete(url=endpoint)
            logger.info(f"Template with name: {name} - deleted.")
            return response.ok
        logger.warning(f"Template: {template} is attached to device - cannot be deleted.")
        raise AttachedError(template.name)

    def create(
        self,
        device_model: DeviceModel,
        name: str,
        description: str,
        config: CiscoConfParse,
    ) -> bool:
        """

        Args:
            device_model (DeviceModel): Device model to create template.
            name (str): Name template to create.
            description (str): Description template to create.
            config (CiscoConfParse): The config to device.

        Raises:
            NameAlreadyExistError: If such template name already exists.

        Returns:
            bool: True if create template is successful, otherwise - False.
        """
        try:
            self.get(name)
            logger.error(f"Error, Template with name: {name} exists.")
            raise NameAlreadyExistError(name)
        except NotFoundError:
            cli_template = CLITemplate(self.session, device_model, name, description)
            cli_template.config = config
            logger.info(f"Template with name: {name} - created.")
            return cli_template.send_to_device()

    def template_validation(self, id: str, device: Device) -> str:
        """Checking the template of the configuration on the machine.

        Args:
            id (str): template id to check.
            device (Device): The device on which the configuration is to be validate.

        Returns:
            str: Validated config.
        """
        payload = {
            "templateId": id,
            "device": {
                "csv-status": "complete",
                "csv-deviceId": device.uuid,
                "csv-deviceIP": device.id,
                "csv-host-name": device.hostname,
                "csv-templateId": id,
            },
            "isEdited": False,
            "isMasterEdited": False,
            "isRFSRequired": True,
        }
        endpoint = "/dataservice/template/device/config/config/"
        response = self.session.post(url=endpoint, json=payload)
        return response.text

    @staticmethod
    def compare_template(
        first: CiscoConfParse,
        second: CiscoConfParse,
        full: bool = False,
        debug: bool = False,
    ) -> str:
        """

        Args:
            first: First template for comparison.
            second: Second template for comparison.
            full: Return a full comparison if True, otherwise only the lines that differ.
            debug: Adding debug to the logger. Defaults to False.

        Returns:
            str: The compared templates.

        Code    Meaning
        '- '    line unique to sequence 1
        '+ '    line unique to sequence 2
        '  '    line common to both sequences
        '? '    line not present in either input sequence

        Example:
        >>> a = "!\n  tacacs\n  server 192.168.1.1\n   vpn 2\n   secret-key a\n   auth-port 151\n exit".splitlines()
        >>> b = "!\n  tacacs\n  server 192.168.1.1\n   vpn 3\n   secret-key a\n   auth-port 151\n exit".splitlines()
        >>> a_conf = CiscoConfParse(a)
        >>> b_conf = CiscoConfParse(b)
        >>> compare = TemplateAPI.compare_template(a_conf, b_conf full=True)
        >>> print(compare)
          !
            tacacs
            server 192.168.1.1
        -    vpn 2
        ?        ^
        +    vpn 3
        ?        ^
            secret-key a
            auth-port 151
        exit
        """
        first_n = list(map(lambda x: x + "\n", first.ioscfg))
        second_n = list(map(lambda x: x + "\n", second.ioscfg))
        compare = list(Differ().compare(first_n, second_n))
        if not full:
            compare = [x for x in compare if x[0] in ["?", "-", "+"]]
        if debug:
            logger.debug("".join(compare))
        return "".join(compare)

    def compare_with_running(
        self,
        template: CiscoConfParse,
        device: Device,
        full: bool = False,
        debug: bool = False,
    ) -> str:
        """The comparison of the config with the one running on the machine.

        Args:
            template: The template to compare.
            device: The device on which to compare config.
            full: Return a full comparison if True, otherwise only the lines that differ.
            debug: Adding debug to the logger. Defaults to False.

        Returns:
            str: The compared templates.

        Example:
        >>> a = "!\n  tacacs\n  server 192.168.1.1\n   vpn 512\n   secret-key a\n   auth-port 151\n exit".splitlines()
        >>> a_conf = CiscoConfParse(a)
        >>> device = DevicesAPI(API_SESSION).get(DeviceField.HOSTNAME, device_name)
        >>> compare = TemplateAPI.compare_template(a_conf, device, full=True)
        >>> print(compare)
        .
        .
        .
            zbfw-udp-idle-time    30
           !
          !
        + !
        +   tacacs
        +   server 192.168.1.1
        +    vpn vpn 512
        +    secret-key a
        +    auth-port 151
        +  exit
          omp
           no shutdown
           ecmp-limit       6
        .
        .
        .
        """
        running_config = CLITemplate(
            self.session, DeviceModel(device.model), "running_conf", "running_conf"
        ).load_running(device)
        return self.compare_template(running_config, template, debug)


class CLITemplate:
    def __init__(
        self,
        session: vManageSession,
        device_model: DeviceModel,
        name: str,
        description: str,
    ) -> None:
        self.session = session
        self.device_model = device_model
        self.name = name
        self.description = description
        self.config: CiscoConfParse = CiscoConfParse([])

    def load(self, id: str) -> CiscoConfParse:
        """Load CLI config from template.

        Args:
            id (str): The template id from which load config.

        Raises:
            TemplateTypeError: wrong template type - CLI required.

        Returns:
            CiscoConfParse: Loaded template.
        """
        endpoint = f"/dataservice/template/device/object/{id}"
        config = self.session.get_json(endpoint)
        if TemplateType(config["configType"]) == TemplateType.FEATURE:
            raise TemplateTypeError(config["templateName"])
        self.config = CiscoConfParse(config["templateConfiguration"].splitlines())
        return self.config

    def load_running(self, device: Device) -> CiscoConfParse:
        """Load running config from device.

        Args:
            device (Device): The device from which load config.

        Returns:
            CiscoConfParse: A working configuration on the machine.
        """
        endpoint = f"/dataservice/template/config/running/{device.uuid}"
        config = self.session.get_json(endpoint)
        self.config = CiscoConfParse(config["config"].splitlines())
        logger.debug(f"Template loaded from {device.hostname}.")
        return self.config

    def send_to_device(self) -> bool:
        """

        Returns:
            bool: True if send template to device is successful, otherwise - False.

        The payload differs depending on the type of machine - for physical machines it has two more attributes.
        """
        config_str = "\n".join(self.config.ioscfg)
        payload = {
            "templateName": self.name,
            "templateDescription": self.description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_str,
            "factoryDefault": False,
            "configType": "file",
        }
        if self.device_model not in [
            DeviceModel.VEDGE,
            DeviceModel.VSMART,
            DeviceModel.VMANAGE,
            DeviceModel.VBOND,
        ]:
            payload["cliType"] = "device"
            payload["draftMode"] = False

        endpoint = "/dataservice/template/device/cli/"
        try:
            self.session.post(url=endpoint, json=payload).json()
        except HTTPError as error:
            response = json.loads(error.response.text)["error"]
            logger.error(f'Response message: {response["message"]}')
            logger.error(f'Response details: {response["details"]}')
            return False
        logger.info(f"Template with name: {self.name} - sent to the device.")
        return True

    def update(self, id: str, config: CiscoConfParse) -> bool:
        """Update an existing cli template.

        Args:
            id (str): Template id to update.
            config (CiscoConfParse): Updated config.

        Returns:
            bool: True if update template is successful, otherwise - False.

        """
        self.config = config
        config_str = "\n".join(self.config.ioscfg)
        payload = {
            "templateId": id,
            "templateName": self.name,
            "templateDescription": self.description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_str,
            "factoryDefault": False,
            "configType": "file",
            "draftMode": False,
        }
        endpoint = f"/dataservice/template/device/{id}"
        try:
            self.session.put(url=endpoint, json=payload)
        except HTTPError as error:
            response = json.loads(error.response.text)["error"]
            logger.error(f'Response message: {response["message"]}')
            logger.error(f'Response details: {response["details"]}')
            return False
        logger.info(f"Template with name: {self.name} - updated.")
        return True

    def add_to_config(self, add_config: CiscoConfParse, add_before: str) -> None:
        """Add config to existing config before provided value.

        Args:
            add_config (CiscoConfParse): Config to added.
            add_before (str): The value before which to add config.
        """
        for comand in add_config.ioscfg:
            self.config.ConfigObjs.insert_before(add_before, comand, atomic=True)
