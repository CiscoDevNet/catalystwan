# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import json
import logging
from difflib import Differ
from typing import TYPE_CHECKING

from attr import define  # type: ignore
from ciscoconfparse import CiscoConfParse  # type: ignore
from requests.exceptions import HTTPError

from catalystwan.dataclasses import Device
from catalystwan.exceptions import TemplateTypeError
from catalystwan.utils.device_model import DeviceModel
from catalystwan.utils.template_type import TemplateType

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


@define
class CLITemplate:
    template_name: str
    template_description: str
    device_model: DeviceModel
    config: CiscoConfParse = CiscoConfParse([], factory=True)

    def load(self, session: ManagerSession, id: str) -> CiscoConfParse:
        """Load CLI config from template.
        Args:
            id (str): The template id from which load config.
        Raises:
            TemplateTypeError: wrong template type - CLI required.
        Returns:
            CiscoConfParse: Loaded template.
        """
        endpoint = f"/dataservice/template/device/object/{id}"
        config = session.get_json(endpoint)
        if TemplateType(config["configType"]) == TemplateType.FEATURE:
            raise TemplateTypeError(config["templateName"])
        self.config = CiscoConfParse(config["templateConfiguration"].splitlines())
        return self.config

    def load_running(self, session: ManagerSession, device: Device) -> CiscoConfParse:
        """Load running config from device.

        Args:
            session: logged in API client session
            device: The device from which load config.

        Returns:
            CiscoConfParse: A working configuration on the machine.
        """
        encoded_uuid = device.uuid.replace("/", "%2F")
        endpoint = f"/dataservice/template/config/running/{encoded_uuid}"
        config = session.get_json(endpoint)
        self.config = CiscoConfParse(config["config"].splitlines())
        logger.debug(f"Template loaded from {device.hostname}.")
        return self.config

    def generate_payload(self) -> dict:
        config_str = "\n".join(self.config.ioscfg)
        payload = {
            "templateName": self.template_name,
            "templateDescription": self.template_description,
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
        return payload

    def update(self, session: ManagerSession, id: str, config: CiscoConfParse) -> bool:
        """Update an existing cli template.

        Args:
            session: logged in API client session
            id: Template id to update.
            config: Updated config.

        Returns:
            bool: True if update template is successful, otherwise - False.

        """
        self.config = config
        config_str = "\n".join(self.config.ioscfg)
        payload = {
            "templateId": id,
            "templateName": self.template_name,
            "templateDescription": self.template_description,
            "deviceType": self.device_model.value,
            "templateConfiguration": config_str,
            "factoryDefault": False,
            "configType": "file",
            "draftMode": False,
        }
        endpoint = f"/dataservice/template/device/{id}"
        try:
            session.put(url=endpoint, json=payload)
        except HTTPError as error:
            if error.response:
                response = json.loads(error.response.text)["error"]
                logger.error(f'Response message: {response["message"]}')
                logger.error(f'Response details: {response["details"]}')
            else:
                logger.error("Response is None.")
            return False
        logger.info(f"Template with name: {self.template_name} - updated.")
        return True

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
        session,
        template: CiscoConfParse,
        device: Device,
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
        running_config = self.load_running(session, device)
        return self.compare_template(running_config, template, debug)
