# Copyright 2022 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import json
import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Type, overload

from ciscoconfparse import CiscoConfParse  # type: ignore

from catalystwan.api.task_status_api import Task
from catalystwan.api.templates.cli_template import CLITemplate
from catalystwan.api.templates.device_template.device_template import (
    DeviceSpecificValue,
    DeviceTemplate,
    GeneralTemplate,
)
from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.api.templates.feature_template_field import FeatureTemplateField
from catalystwan.api.templates.feature_template_payload import FeatureTemplatePayload
from catalystwan.api.templates.models.cisco_aaa_model import CiscoAAAModel
from catalystwan.api.templates.models.cisco_banner_model import CiscoBannerModel
from catalystwan.api.templates.models.cisco_bfd_model import CiscoBFDModel
from catalystwan.api.templates.models.cisco_bgp_model import CiscoBGPModel
from catalystwan.api.templates.models.cisco_logging_model import CiscoLoggingModel
from catalystwan.api.templates.models.cisco_ntp_model import CiscoNTPModel
from catalystwan.api.templates.models.cisco_omp_model import CiscoOMPModel
from catalystwan.api.templates.models.cisco_ospf import CiscoOSPFModel
from catalystwan.api.templates.models.cisco_ospfv3 import CiscoOspfv3Model
from catalystwan.api.templates.models.cisco_secure_internet_gateway import CiscoSecureInternetGatewayModel
from catalystwan.api.templates.models.cisco_snmp_model import CiscoSNMPModel
from catalystwan.api.templates.models.cisco_system import CiscoSystemModel
from catalystwan.api.templates.models.cisco_vpn_interface_model import CiscoVpnInterfaceModel
from catalystwan.api.templates.models.cisco_vpn_model import CiscoVPNModel
from catalystwan.api.templates.models.cli_template import CliTemplateModel
from catalystwan.api.templates.models.omp_vsmart_model import OMPvSmart
from catalystwan.api.templates.models.security_vsmart_model import SecurityvSmart
from catalystwan.api.templates.models.system_vsmart_model import SystemVsmart
from catalystwan.dataclasses import Device, DeviceTemplateInfo, FeatureTemplateInfo, FeatureTemplatesTypes, TemplateInfo
from catalystwan.endpoints.configuration_device_template import FeatureToCLIPayload
from catalystwan.exceptions import AttachedError, TemplateNotFoundError
from catalystwan.models.templates import DeviceTemplateInformation, FeatureTemplateInformation
from catalystwan.response import ManagerResponse
from catalystwan.typed_list import DataSequence
from catalystwan.utils.device_model import DeviceModel
from catalystwan.utils.dict import merge
from catalystwan.utils.pydantic_field import get_extra_field
from catalystwan.utils.template_type import TemplateType

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class DeviceModelError(Exception):
    """Used when unsupported device model used in template."""

    def __init__(self, template, device_models):
        self.message = f"Provided template type '{template.type}' not available for device models: {device_models}"
        super().__init__(self.message)


class DeviceTemplateFeature(Enum):
    LAWFUL_INTERCEPTION = "lawful-interception"
    CLOUD_DOCK = "cloud-dock"
    NETWORK_DESIGN = "network-design"
    VMANAGE_DEFAULT = "vmanage-default"
    ALL = "all"


class TemplatesAPI:
    def __init__(self, session: ManagerSession) -> None:
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
        if isinstance(template, FeatureTemplate):
            return self._get_feature_templates()
        if template is FeatureTemplate:
            return self._get_feature_templates()
        if isinstance(template, (DeviceTemplate, CLITemplate)):
            return self._get_device_templates()
        if template in [DeviceTemplate, CLITemplate]:
            return self._get_device_templates()

        raise NotImplementedError()

    def _get_feature_templates(
        self,
        summary: bool = True,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
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

    def attach(self, name: str, device: Device, timeout_seconds: int = 300, **kwargs):
        template_type = self.get(DeviceTemplate).filter(name=name).single_or_default().config_type
        if template_type == TemplateType.CLI:
            return self._attach_cli(name, device, timeout_seconds=timeout_seconds, **kwargs)

        if template_type == TemplateType.FEATURE:
            return self._attach_feature(name, device, timeout_seconds=timeout_seconds, **kwargs)

        raise NotImplementedError()

    def _attach_feature(self, name: str, device: Device, timeout_seconds: int = 300, **kwargs):
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
            body = {
                "templateId": template_id,
                "isEdited": False,
                "isMasterEdited": False,
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
                    pointer[var.property] = kwargs["device_specific_vars"][var.property]  # type: ignore

        if invalid:
            raise TypeError()

        endpoint = "/dataservice/template/device/config/attachfeature"
        logger.info(f"Attaching a template: {name} to the device: {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        task = Task(session=self.session, task_id=response["id"]).wait_for_completed(timeout_seconds=timeout_seconds)
        if task.result:
            return True
        logger.warning(f"Failed to attach tempate: {name} to the device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.sub_tasks_data[0].activity}")
        return False

    def _attach_cli(self, name: str, device: Device, is_edited: bool = False, timeout_seconds: int = 300) -> bool:
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
        task = Task(session=self.session, task_id=response["id"]).wait_for_completed(timeout_seconds=timeout_seconds)
        if task.result:
            return True
        logger.warning(f"Failed to attach tempate: {name} to the device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.sub_tasks_data[0].activity}")
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
        task = Task(session=self.session, task_id=response["id"]).wait_for_completed()
        if task.result:
            return True
        logger.warning(f"Failed to change to cli mode for device: {device.hostname}.")
        logger.warning(f"Task activity information: {task.sub_tasks_data[0].activity}")
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
    def edit(self, template: FeatureTemplate) -> Any:
        ...

    @overload
    def edit(self, template: CLITemplate) -> Any:
        ...

    @overload
    def edit(self, template: DeviceTemplate) -> Any:
        ...

    def edit(self, template):
        template_info = self.get(template).filter(name=template.template_name).single_or_default()
        if not template_info:
            raise TemplateNotFoundError(f"Template with name [{template.template_name}] does not exists.")

        if isinstance(template, FeatureTemplate):
            return self._edit_feature_template(template, template_info)

        if isinstance(template, DeviceTemplate):
            return self._edit_device_template(template)

        raise NotImplementedError()

    def _edit_device_template(self, template: DeviceTemplate):
        self._create_device_template(template, True)

    def _edit_feature_template(self, template: FeatureTemplate, data: FeatureTemplateInfo) -> ManagerResponse:
        if self.is_created_by_generator(template):
            debug = False
            schema = self.get_feature_template_schema(template, debug)
            payload = self.generate_feature_template_payload(template, schema, debug).model_dump(
                by_alias=True, mode="json"
            )
        else:
            payload = json.loads(template.generate_payload(self.session))

        response = self.session.put(f"/dataservice/template/feature/{data.id}", json=payload)
        return response

    @overload
    def create(self, template: FeatureTemplate, debug=False) -> str:
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

        # exists = self.get(template).filter(name=template.name)
        # if exists:
        #     raise AlreadyExistsError(f"Template with name [{template.name}] already exists.")

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

        logger.info(f"Template {template.template_name} ({template_type}) was created successfully ({template_id}).")
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

    def _create_device_template(self, device_template: DeviceTemplate, edit: bool = False) -> str:
        def get_general_template_info(
            name: str, fr_templates: DataSequence[FeatureTemplateInfo]
        ) -> FeatureTemplateInfo:
            _template = fr_templates.filter(name=name).single_or_default()

            if not _template:
                raise TypeError(f"{name} does not exists. Device Template is invalid.")

            return _template

        def parse_general_template(
            general_template: GeneralTemplate,
            fr_templates: DataSequence[FeatureTemplateInfo],
        ) -> GeneralTemplate:
            if general_template.subTemplates:
                general_template.subTemplates = [
                    parse_general_template(_t, fr_templates) for _t in general_template.subTemplates
                ]
            if general_template.name:
                info = get_general_template_info(general_template.name, fr_templates)
                return GeneralTemplate(
                    name=general_template.name,
                    subTemplates=general_template.subTemplates,
                    templateId=info.id,
                    templateType=info.template_type,
                )
            else:
                return general_template

        fr_templates = self.get(FeatureTemplate)  # type: ignore
        device_template.general_templates = list(
            map(lambda x: parse_general_template(x, fr_templates), device_template.general_templates)  # type: ignore
        )

        if edit:
            template_id = (
                self.session.api.templates.get(DeviceTemplate)
                .filter(name=device_template.template_name)
                .single_or_default()
                .id
            )
            payload = json.loads(device_template.generate_payload())
            response = self.session.put(f"/dataservice/template/device/{template_id}", json=payload)
        else:
            endpoint = "/dataservice/template/device/feature/"
            payload = json.loads(device_template.generate_payload())
            response = self.session.post(endpoint, json=payload)

        return response.text

    def is_created_by_generator(self, template: FeatureTemplate) -> bool:
        """Checks if template is created by generator

        Method will be deleted if every template's payload will be generated dynamically.
        """
        ported_templates = (
            CiscoAAAModel,
            CiscoBFDModel,
            CiscoBannerModel,
            CiscoNTPModel,
            CiscoLoggingModel,
            CiscoOMPModel,
            OMPvSmart,
            SecurityvSmart,
            SystemVsmart,
            CiscoVpnInterfaceModel,
            CiscoSystemModel,
            CiscoSNMPModel,
            CiscoVPNModel,
            CiscoBGPModel,
            CiscoOSPFModel,
            CliTemplateModel,
            CiscoSecureInternetGatewayModel,
            CiscoOspfv3Model,
        )

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
        response = self.session.post(endpoint, json=payload.model_dump(by_alias=True, exclude_none=True, mode="json"))

        return response.json()["templateId"]

    def generate_feature_template_payload(
        self, template: FeatureTemplate, schema: Any, debug: bool = False
    ) -> FeatureTemplatePayload:
        payload = FeatureTemplatePayload(
            name=template.template_name,
            description=template.template_description,
            template_type=template.type,
            device_types=[device_model.value for device_model in template.device_models],
            definition={},
        )  # type: ignore

        fr_template_fields = [FeatureTemplateField(**field) for field in schema["fields"]]  # TODO
        json_dumped_template = template.model_dump(mode="json")
        # "name"
        for field in fr_template_fields:
            value = None
            priority_order = None
            # TODO How to discover Device specific variable
            if field.key in template.device_specific_variables:
                value = template.device_specific_variables[field.key]
            else:
                for field_name, field_value in template.model_fields.items():
                    data_path = get_extra_field(field_value, "data_path", default=[])
                    vmanage_key = get_extra_field(field_value, "vmanage_key")
                    if field.dataPath == data_path and (  # type: ignore
                        (field.key == field_value.alias or field.key == field_name)
                        or field.key == vmanage_key  # type: ignore
                    ):
                        priority_order = get_extra_field(field_value, "priority_order")  # type: ignore
                        value = getattr(template, field_name)
                        json_dumped_value = json_dumped_template.get(field_name)
                        break
                if value is None:
                    continue

            payload.definition = merge(
                payload.definition,
                field.payload_scheme(value, json_dumped_value=json_dumped_value, priority_order=priority_order),
            )

        if debug:
            with open(f"payload_{template.type}.json", "w") as f:
                f.write(json.dumps(payload.model_dump(by_alias=True, mode="json"), indent=4))

        return payload

    def validate_device_model(self, template: FeatureTemplate) -> bool:
        """Verify if selected template can be used with provided device model"""

        template_type = self._get_feature_template_types().filter(name=template.type).single_or_default()

        available_devices_for_template = [device["name"] for device in template_type.device_models]

        provided_device_models = [
            dev_mod.value if type(dev_mod) is DeviceModel else dev_mod for dev_mod in template.device_models
        ]

        if not all(dev in available_devices_for_template for dev in provided_device_models):
            logger.debug(f"Available devices for template '{template.type}': {available_devices_for_template}")
            raise DeviceModelError(template, provided_device_models)
        return True

    def _get_feature_template_types(self, type: str = "all") -> DataSequence[FeatureTemplatesTypes]:
        """Gets list off all templates and devices associated with these templates"""

        endpoint = "/dataservice/template/feature/types"
        params = {"type": type}
        response = self.session.get(endpoint, params=params)

        return response.dataseq(FeatureTemplatesTypes)

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
        payload = {
            "templateId": template_id,
            "deviceIds": [device.uuid],
            "isEdited": True,
            "isMasterEdited": True,
        }
        endpoint = "/dataservice/template/device/config/input/"
        logger.info(f"Editing template: {name} of device: {device.hostname}.")
        response = self.session.post(url=endpoint, json=payload).json()
        if (response.get("data") is not None) and (response["data"][0].get("csv-status") == "complete"):
            return True
        logger.warning(f"Failed to edit tempate: {name} of device: {device.hostname}.")
        return False

    def get_device_configuration_preview(self, payload: FeatureToCLIPayload) -> CiscoConfParse:
        text_config = self.session.endpoints.configuration_device_template.get_device_configuration_preview(payload)

        return CiscoConfParse(text_config.splitlines())

    def load_running(self, device: Device) -> CiscoConfParse:
        """Load running config from device.

        Args:
            device: The device from which load config.

        Returns:
            CiscoConfParse: A working configuration on the machine.
        """
        encoded_uuid = device.uuid.replace("/", "%2F")
        endpoint = f"/dataservice/template/config/running/{encoded_uuid}"
        response = self.session.get_json(endpoint)
        config = CiscoConfParse(response["config"].splitlines())
        logger.debug(f"Template loaded from {device.hostname}.")
        return config

    def get_feature_templates(self) -> DataSequence[FeatureTemplateInformation]:
        endpoint = "/dataservice/template/feature"
        fr_templates = self.session.get(endpoint)
        return fr_templates.dataseq(FeatureTemplateInformation)

    def get_device_templates(self) -> DataSequence[DeviceTemplateInformation]:
        endpoint = "/dataservice/template/device"
        params = {"feature": "all"}
        templates = self.session.get(url=endpoint, params=params)
        return templates.dataseq(DeviceTemplateInformation)

    def get_device_template(self, template_id: str) -> DeviceTemplate:
        endpoint = f"/dataservice/template/device/object/{template_id}"
        response = self.session.get(endpoint)
        return DeviceTemplate(**response.json())
