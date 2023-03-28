from __future__ import annotations

import json
import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Type, overload

from requests.exceptions import HTTPError

from vmngclient.api.task_status_api import wait_for_completed
from vmngclient.api.templates.cli_template import CLITemplate
from vmngclient.api.templates.device_template.device_template import (
    DeviceSpecificValue,
    DeviceTemplate,
    GeneralTemplate,
)
from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.api.templates.feature_template_field import FeatureTemplateField, get_path_dict
from vmngclient.api.templates.feature_template_payload import FeatureTemplatePayload
from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel
from vmngclient.dataclasses import Device, DeviceTemplateInfo, FeatureTemplateInfo, TemplateInfo
from vmngclient.exceptions import AlreadyExistsError, AttachedError, TemplateNotFoundError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.operation_status import OperationStatus
from vmngclient.utils.template_type import TemplateType

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class DeviceTemplateFeature(Enum):
    LAWFUL_INTERCEPTION = "lawful-interception"
    CLOUD_DOCK = "cloud-dock"
    NETWORK_DESIGN = "network-design"
    VMANAGE_DEFAULT = "vmanage-default"
    ALL = "all"


class TemplatesAPI:
    def __init__(self, session: vManageSession) -> None:
        self.session = session

    @overload
    def get(self, template: Type[DeviceTemplate]) -> DataSequence[DeviceTemplateInfo]:  # type: ignore
        ...

    @overload
    def get(self, template: Type[FeatureTemplate]) -> DataSequence[FeatureTemplateInfo]:  # type: ignore
        ...

    @overload
    def get(self, template: Type[CLITemplate]) -> DataSequence[TemplateInfo]:  # type: ignore
        ...

    def get(self, template):
        if template is FeatureTemplate:
            return self._get_feature_templates()

        if template in [DeviceTemplate, CLITemplate]:
            return self._get_device_templates()

        raise NotImplementedError()

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

    def attach(self, name: str, device: Device, **kwargs):
        template_type = self.get(DeviceTemplate).filter(name=name).single_or_default().config_type
        if template_type == TemplateType.CLI:
            return self._attach_cli(name, device)

        if template_type == TemplateType.FEATURE:
            return self._attach_feature(name, device, **kwargs)

        raise NotImplementedError()

    def _attach_feature(self, name: str, device: Device, **kwargs):
        """Attach Device Template created with Feature Templates.

        Args:
            name: Name of the Device Template to be attached.
            device: Device object under which the template should be attached.
            **device_specific_vars: For parameters in a feature template that you configure as device-specific,
                when you attach a device template to a device, Cisco vManage prompts you for the values to use
                for these parameters. Entering device-specific values in this manner is useful in test or POC networks,
                or if you are deploying a small network. This method generally does not scale well for larger networks.
        """

        def get_device_specific_variables(name: str):
            endpoint = "/dataservice/template/device/config/exportcsv"
            template_id = self.get(DeviceTemplate).filter(name=name).single_or_default().id
            body = {"templateId": template_id, "isEdited": False, "isMasterEdited": False}

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
                    pointer[var.property] = kwargs["device_specific_vars"][var.property]  # type: ignore

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

    def _attach_cli(self, name: str, device: Device, is_edited: bool = False) -> bool:
        """

        Args:
            name (str): Template name to attached.
            device (Device): Device to attach template.
            is_edited (bool): Flag to indicate whether template is being attached as part of edit

        Returns:
            bool: True if attaching template is successful, otherwise - False.
        """
        try:
            template_id = self.get(CLITemplate).filter(name=name).single_or_default().id
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
        if is_edited:
            payload["deviceTemplateList"][0]["isEdited"] = True  # type: ignore
        endpoint = "/dataservice/template/device/config/attachcli"
        logger.info(f"Attaching a template: {name} to the device: {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        task = wait_for_completed(session=self.session, action_id=response["id"])
        if task.status == OperationStatus.SUCCESS.value:
            return True
        logger.warning(f"Failed to attach tempate: {name} to the device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.activity}")
        return False

    def deatach(self, device: Device) -> bool:
        """
        Deatach it`s the same to change device mode to CLI mode.

        Args:
            device (Device): Device to deatach template (change mode).

        Returns:
            bool: True if change deatach template (mode to CLI) is successful, otherwise - False.
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

    @overload
    def delete(self, template: Type[DeviceTemplate], name: str) -> bool:  # type: ignore
        ...

    @overload
    def delete(self, template: Type[FeatureTemplate], name: str) -> bool:  # type: ignore
        ...

    @overload
    def delete(self, template: Type[CLITemplate], name: str) -> bool:  # type: ignore
        ...

    def delete(self, template, name):
        status = False

        if template is FeatureTemplate:
            status = self._delete_feature_template(name)

        if template is DeviceTemplate and name:
            status = self._delete_device_template(name)

        if isinstance(template, CLITemplate):
            status = self._delete_cli_template(name)

        if template is CLITemplate and name:
            status = self._delete_cli_template(name)

        if status:
            logger.info(f"Template {name} was successfuly deleted.")
            return status

        raise NotImplementedError(f"Not implemented for {template}")

    def _delete_feature_template(self, name: str) -> bool:
        template = self.get(FeatureTemplate).filter(name=name).single_or_default()  # type: ignore
        if template:
            endpoint = f"/dataservice/template/feature/{template.id}"
            self.session.delete(url=endpoint)
        return True

    def _delete_device_template(self, name: str) -> bool:
        """

        Args:
            name (str): Name template to delete.

        Raises:
            AttachedError: If template is attached to device.

        Returns:
            bool: True if deletion is successful, otherwise - False.
        """
        template = self.get(DeviceTemplate).filter(name=name).single_or_default()  # type: ignore
        if template:
            endpoint = f"/dataservice/template/device/{template.id}"
            if template.devices_attached == 0:
                response = self.session.delete(url=endpoint)
                logger.info(f"Template with name: {name} - deleted.")
                return response.ok
            logger.warning(f"Template: {template} is attached to device - cannot be deleted.")
            raise AttachedError(template.name)
        return True

    def _delete_cli_template(self, name: str) -> bool:
        """

        Args:
            name (str): Name template to delete.

        Raises:
            AttachedError: If template is attached to device.

        Returns:
            bool: True if deletion is successful, otherwise - False.
        """
        template = self.get(CLITemplate).filter(name=name).single_or_default()  # type: ignore
        if template:
            endpoint = f"/dataservice/template/device/{template.id}"
            if template.devices_attached == 0:
                response = self.session.delete(url=endpoint)
                logger.info(f"Template with name: {name} - deleted.")
                return response.ok
            logger.warning(f"Template: {template} is attached to device - cannot be deleted.")
            raise AttachedError(template.name)
        return True

    @overload
    def create(self, template: FeatureTemplate) -> str:
        ...

    @overload
    def create(self, template: DeviceTemplate) -> str:
        ...

    @overload
    def create(self, template: CLITemplate) -> str:
        ...

    def create(self, template, debug: bool = False):
        if isinstance(template, list):
            return [self.create(t) for t in template]

        template_id: Optional[str] = None  # type: ignore
        template_type = None

        exists = self.get(type(template)).filter(name=template.name)
        if exists:
            raise AlreadyExistsError(f"Template with name [{template.name}] already exists.")

        if isinstance(template, FeatureTemplate):
            if self.is_created_by_generator(template):
                template_id = self.create_by_generator(template, debug)
            else:
                template_id = self._create_feature_template(template)
            template_type = FeatureTemplate.__name__

        if isinstance(template, DeviceTemplate):
            template_id = self._create_device_template(template)
            template_type = DeviceTemplate.__name__

        if isinstance(template, CLITemplate):
            template_id = self._create_cli_template(template)
            template_type = CLITemplate.__name__

        if not template_id:
            raise NotImplementedError()

        logger.info(f"Template {template.name} ({template_type}) was created successfully ({template_id}).")
        return template_id

    def _create_feature_template(self, template: FeatureTemplate) -> str:
        payload = template.generate_payload(self.session)
        response = self.session.post("/dataservice/template/feature", json=json.loads(payload))
        template_id = response.json()["templateId"]

        return template_id

    def _create_cli_template(self, template: CLITemplate) -> str:

        payload = template.generate_payload()
        response = self.session.post("/dataservice/template/device/cli/", json=payload)
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

        fr_templates = self.get(FeatureTemplate)  # type: ignore
        device_template.general_templates = list(
            map(lambda x: parse_general_template(x, fr_templates), device_template.general_templates)  # type: ignore
        )

        endpoint = "/dataservice/template/device/feature/"
        payload = json.loads(device_template.generate_payload())
        response = self.session.post(endpoint, json=payload)

        return response.text

    def is_created_by_generator(self, template: FeatureTemplate) -> bool:
        """Checks if template is created by generator

        Method will be deleted if every template's payload will be generated dynamically.
        """
        ported_templates = (CiscoAAAModel,)

        return isinstance(template, ported_templates)

    def get_feature_template_schema(self, template: FeatureTemplate, debug: bool = False) -> Any:
        endpoint = f"/dataservice/template/feature/types/definition/{template.type}/15.0.0"
        schema = self.session.get(url=endpoint).json()

        if debug:
            with open(f"response_{template.type}.json", "w") as f:
                f.write(json.dumps(schema, indent=4))

        return schema

    def create_by_generator(self, template: FeatureTemplate, debug: bool) -> str:
        schema = self.get_feature_template_schema(template, debug)
        payload = self.generate_feature_template_payload(template, schema, debug)

        endpoint = "/dataservice/template/feature"
        response = self.session.post(endpoint, json=payload.dict(by_alias=True))

        return response.json()["templateId"]

    def generate_feature_template_payload(
        self, template: FeatureTemplate, schema: Any, debug: bool = False
    ) -> FeatureTemplatePayload:
        payload = FeatureTemplatePayload(
            name=template.name,
            description=template.description,
            template_type=template.type,
            device_types=["vedge-C8000V"],  # TODO
            definition={},
        )

        fr_template_fields = [FeatureTemplateField(**field) for field in schema["fields"]]  # TODO
        payload.definition.update(get_path_dict([field.dataPath for field in fr_template_fields]))

        for field in fr_template_fields:
            payload.definition.update(field.data_path(output={}))

        for i, field in enumerate(fr_template_fields):
            pointer = payload.definition

            value = template.dict(by_alias=True).get(field.key, None)
            if isinstance(value, bool):
                value = str(value).lower()

            for path in field.dataPath:
                pointer = pointer[path]
            pointer.update(field.payload_scheme(value, payload.definition))

        if debug:
            with open(f"payload_{template.type}.json", "w") as f:
                f.write(json.dumps(payload.dict(by_alias=True), indent=4))

        return payload

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

    def edit_before_push(self, name: str, device: Device) -> bool:
        """
        Edits device / CLI template before pushing modified config to device(s)

        Args:
            name (str): Template name to edit.
            device (Device): Device to attach template.

        Returns:
            bool: True if edit template is successful, otherwise - False.
        """
        try:
            template_id = self.get(CLITemplate).filter(name=name).single_or_default().id
            self.template_validation(template_id, device=device)
        except TemplateNotFoundError:
            logger.error(f"Error, Template with name {name} not found on {device}.")
            return False
        except HTTPError as error:
            error_details = json.loads(error.response.text)
            logger.error(f"Error in config: {error_details['error']['details']}.")
            return False
        payload = {"templateId": template_id, "deviceIds": [device.uuid], "isEdited": True, "isMasterEdited": True}
        endpoint = "/dataservice/template/device/config/input/"
        logger.info(f"Editing template: {name} of device: {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        if (response.get("data") is not None) and (response["data"][0].get("csv-status") == "complete"):
            return True
        logger.warning(f"Failed to edit tempate: {name} of device: {device.hostname}.")
        return False
