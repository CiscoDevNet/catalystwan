from __future__ import annotations

import json
import logging
from difflib import Differ
from enum import Enum
from typing import TYPE_CHECKING, Optional, overload

from ciscoconfparse import CiscoConfParse  # type: ignore
from requests.exceptions import HTTPError

from vmngclient.api.task_status_api import wait_for_completed
from vmngclient.api.templates.device_template.device_template import DeviceSpecificValue, DeviceTemplate, GeneralTemplate
from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.dataclasses import Device, DeviceTemplateInfo, FeatureTemplateInfo, TemplateInfo
from vmngclient.exceptions import AlreadyExistsError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.device_model import DeviceModel
from vmngclient.utils.operation_status import OperationStatus

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class TemplateType(Enum):
    CLI = "file"
    FEATURE = "template"


class TemplateNotFoundError(Exception):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class AttachedError(Exception):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateTypeError(Exception):
    """Used when wrong type template."""

    def __init__(self, name):
        self.message = f"Template: {name} - wrong template type."


class DeviceTemplateFeature(Enum):
    LAWFUL_INTERCEPTION = "lawful-interception"
    CLOUD_DOCK = "cloud-dock"
    NETWORK_DESIGN = "network-design"
    VMANAGE_DEFAULT = "vmanage-default"
    ALL = "all"


class TemplatesAPI:
    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def _get_feature_templates(
        self, summary: bool = True, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> DataSequence[FeatureTemplateInfo]:
        """In a multitenant vManage system, this API is only available in the Provider view."""
        endpoint = "/dataservice/template/feature"
        params = {"summary": summary}

        fr_templates = self.session.get(url=endpoint, params=params)

        return fr_templates.dataseq(FeatureTemplateInfo)

    def _get_device_templates(
        self, feature: DeviceTemplateFeature = DeviceTemplateFeature.ALL
    ) -> DataSequence[DeviceTemplateInfo]:
        """In a multitenant vManage system, this API is only available in the Provider view."""
        endpoint = "/dataservice/template/device"
        params = {"feature": feature.value}

        templates = self.session.get(url=endpoint, params=params)
        return templates.dataseq(DeviceTemplateInfo)

    @overload
    def get(self, template: type) -> DataSequence[FeatureTemplate]:
        ...

    @overload
    def get(self, template: DeviceTemplate) -> DataSequence[DeviceTemplate]:
        ...

    def get(self, template):
        if template is FeatureTemplate:
            return self._get_feature_templates()

        if template is DeviceTemplate:
            return self._get_device_templates()

        return DataSequence(TemplateInfo)

    @overload
    def attach(self, template: CLITemplate, name: str, device: Device) -> bool:
        ...
    
    @overload    
    def attach(self, template: DeviceTemplate) -> bool:
        ...


    def attach(self, template, device, name=None, **kwargs):
        if isinstance(template, CLITemplate):
            return self._attach_cli(template, name, device)
        
        if isinstance(template, DeviceTemplate):
            return self.attach_feature(template.name, device, **kwargs)

        if template is DeviceTemplate and name:
            self.attach_feature(name, device, **kwargs)
        
        raise NotImplementedError()
    
    # TODO list of devices
    def attach_feature(self, name: str, device: Device, **kwargs):
        def get_device_specific_variables(name: str):
            endpoint = "/dataservice/template/device/config/exportcsv"
            template_id = self.get(DeviceTemplate).filter(name=name).single_or_default().id
            body = {
                "templateId": template_id,
                "isEdited": False,
                "isMasterEdited": False
            }

            values = self.session.post(endpoint, json=body).json()["header"]["columns"]
            return [DeviceSpecificValue(**value) for value in values]
        
        vars = get_device_specific_variables(name)
        template_id = self.get(DeviceTemplate).filter(name=name).single_or_default().id
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
        
        invalid = False
        for var in vars:
            if var.property not in payload["deviceTemplateList"][0]["device"][0]:
                pointer = payload["deviceTemplateList"][0]["device"][0]
                if var.property not in kwargs["device_specific_vars"]:
                    invalid = True
                    logger.error(f"{var.property} should be provided in attach method as device_specific_vars kwarg.")
                else:
                    pointer[var.property] = kwargs["device_specific_vars"][var.property]
                    
        if invalid:
            raise TypeError()

        endpoint = "/dataservice/template/device/config/attachfeature"
        logger.info(f"Attaching a template: {name} to the device: {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        task = wait_for_completed(session=self.session, action_id=response["id"])
        if task.status == OperationStatus.SUCCESS.value:
            return True
        logger.warning(f"Failed to attach tempate: {name} to the device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.activity}")
        return False
        
    
    def _attach_cli(self, name: str, device: Device) -> bool:
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
        except TemplateNotFoundError:
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
        raise NotImplementedError()
        template = self.get(name)
        endpoint = f"/dataservice/template/device/{template.id}"
        if template.devices_attached == 0:
            response = self.session.delete(url=endpoint)
            logger.info(f"Template with name: {name} - deleted.")
            return response.ok
        logger.warning(f"Template: {template} is attached to device - cannot be deleted.")
        raise AttachedError(template.name)

    def _create_cli_template(
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
            AlreadyExistsError: If such template name already exists.

        Returns:
            bool: True if create template is successful, otherwise - False.
        """
        try:
            self.get(CLITemplate)
            raise AlreadyExistsError(f"Error, Template with name: {name} exists.")
        except TemplateNotFoundError:
            cli_template = CLITemplate(self.session, device_model, name, description)
            cli_template.config = config
            logger.info(f"Template with name: {name} - created.")
            return cli_template.send_to_device()

    def _create_feature_template(self, template: FeatureTemplate) -> str:
        payload = template.generate_payload(self.session)
        response = self.session.post("/dataservice/template/feature", json=json.loads(payload))
        template_id = response.json()["templateId"]

        return template_id

    def _create_device_template(self, device_template: DeviceTemplate) -> str:
        def get_general_template_info(
            name: str, fr_templates: DataSequence[FeatureTemplateInfo]
        ) -> FeatureTemplateInfo:
            _template = fr_templates.filter(name=name).single_or_default()
            if not _template:
                raise TypeError(f"{name} does not exists. Device Template is invalid.")

            return _template

        def parse_general_template(
            general_template: GeneralTemplate, fr_templates: DataSequence[FeatureTemplateInfo]
        ) -> GeneralTemplate:
            if general_template.subTemplates:
                general_template.subTemplates = [
                    parse_general_template(_t, fr_templates) for _t in general_template.subTemplates
                ]

            info = get_general_template_info(general_template.name, fr_templates)
            return GeneralTemplate(
                name=general_template.name,
                subTemplates=general_template.subTemplates,
                templateId=info.id,
                templateType=info.template_type,
            )

        fr_templates = self.get(FeatureTemplate)
        device_template.general_templates = list(
            map(lambda x: parse_general_template(x, fr_templates), device_template.general_templates)  # type: ignore
        )

        endpoint = "/dataservice/template/device/feature/"
        payload = json.loads(device_template.generate_payload())
        response = self.session.post(endpoint, json=payload)

        return response.text

    @overload
    def create(self, template: FeatureTemplate) -> str:
        ...

    @overload
    def create(self, template: DeviceTemplate) -> str:
        ...

    @overload
    def create(self, template: CLITemplate) -> str:
        ...

    def create(self, template):
        if isinstance(template, list):
            return [self.create(t) for t in template]

        template_id: Optional[str] = None
        template_type = None

        exists = self.get(type(template)).filter(name=template.name)
        if exists:
            raise AlreadyExistsError(f"Template [{template.name}] already exists.")

        if isinstance(template, FeatureTemplate):
            template_id = self._create_feature_template(template)
            template_type = FeatureTemplate.__name__

        if isinstance(template, DeviceTemplate):
            template_id = self._create_device_template(template)
            template_type = DeviceTemplate.__name__

        if isinstance(template, CLITemplate):
            raise NotImplementedError("CLITemplate is not supported.")

        if not template_id:
            raise NotImplementedError()

        logger.info(f"Template {template.name} ({template_type}) was created successfully ({template_id}).")
        return template_id

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
        device: Optional[Device] = None,
    ):
        self.session = session
        self.device = device
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
