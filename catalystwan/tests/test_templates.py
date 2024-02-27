# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import patch

from parameterized import parameterized  # type: ignore

from catalystwan.api.task_status_api import SubTaskData, TaskResult
from catalystwan.api.template_api import TemplatesAPI
from catalystwan.api.templates.cli_template import CLITemplate
from catalystwan.api.templates.device_template.device_template import DeviceTemplate
from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.api.templates.models.cisco_aaa_model import CiscoAAAModel
from catalystwan.api.templates.payloads.aaa.aaa_model import AAAModel, AuthenticationOrder
from catalystwan.dataclasses import Device, FeatureTemplateInfo, TemplateInfo
from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import create_dataclass
from catalystwan.utils.device_model import DeviceModel
from catalystwan.utils.personality import Personality
from catalystwan.utils.reachability import Reachability


class TestTemplatesAPI(unittest.TestCase):
    def setUp(self):
        self.data_template = [
            {
                "deviceType": "vedge-C8000V",
                "lastUpdatedBy": "user",
                "resourceGroup": "global",
                "templateClass": "cedge",
                "configType": "file",
                "templateId": "dummy_id_1",
                "factoryDefault": False,
                "templateName": "template_1",
                "devicesAttached": 0,
                "templateDescription": "dummy template 1",
                "draftMode": "Disabled",
                "lastUpdatedOn": 0,
                "templateAttached": 0,
            },
            {
                "deviceType": "vedge-cloud",
                "lastUpdatedBy": "admin",
                "resourceGroup": "global",
                "templateClass": "vedge",
                "configType": "file",
                "templateId": "dummy_id_2",
                "factoryDefault": False,
                "templateName": "template_2",
                "devicesAttached": 1,
                "templateDescription": "dummy template 2",
                "draftMode": "Disabled",
                "lastUpdatedOn": 0,
                "templateAttached": 0,
            },
        ]
        self.templates = DataSequence(
            TemplateInfo,
            [create_dataclass(TemplateInfo, template) for template in self.data_template],
        )
        self.device_info = Device(
            personality=Personality.EDGE,
            uuid="dummy_uuid",
            id="162.168.0.1",
            hostname="dummy_host",
            reachability=Reachability.REACHABLE,
            local_system_ip="192.168.0.1",
            memUsage=1.0,
            connected_vManages=["192.168.0.1"],
            model="vedge-cloud",
            status="normal",
        )
        sub_tasks_data = SubTaskData.parse_obj(
            {
                "status": "Success",
                "statusId": "success",
                "action": "",
                "activity": [],
                "currentActivity": "",
                "actionConfig": "",
                "order": 1,
                "uuid": "",
                "host-name": "",
                "site-id": "",
            }
        )
        self.task = TaskResult(result=True, sub_tasks_data=[sub_tasks_data])

    @patch("catalystwan.response.ManagerResponse")
    @patch("catalystwan.session.ManagerSession")
    def test_templates_success(self, mock_session, mocked_response):
        # Arrange
        mock_session.get.return_value = mocked_response
        mocked_response.dataseq.return_value = self.templates

        # Act
        answer = TemplatesAPI(mock_session).get(FeatureTemplate)

        # Assert
        self.assertEqual(answer, self.templates)

    @patch("catalystwan.response.ManagerResponse")
    @patch("catalystwan.session.ManagerSession")
    def test_templates_get(self, mock_session, mocked_response):
        # Arrange
        mock_session.get_data.return_value = mocked_response
        mocked_response.dataseq.return_value = DataSequence(FeatureTemplateInfo, [])

        # Act
        TemplatesAPI(mock_session).get(FeatureTemplate)

        # Assert
        mock_session.get.assert_called_once_with(url="/dataservice/template/feature", params={"summary": True})

    @parameterized.expand(
        [
            (
                AAAModel(
                    template_name="test_template",
                    template_description="test_description",
                    auth_order=[AuthenticationOrder.LOCAL],
                    auth_fallback=False,
                    auth_disable_audit_logs=True,
                    auth_admin_order=True,
                    auth_disable_netconf_logs=False,
                ),
                "aaa_id",
            ),
            (
                DeviceTemplate(  # type: ignore
                    template_name="test_device_template",
                    template_description="test_device_template_description",
                    device_type=DeviceModel.VEDGE_2000,
                    general_templates=[],
                ),
                "device_template_id",
            ),
            (
                CLITemplate(  # type: ignore
                    template_name="test", template_description="test", device_model=DeviceModel.VEDGE
                ),
                "cli_id",
            ),
            (
                CiscoAAAModel(  # type: ignore
                    template_name="test_aaa_model",
                    template_description="test_aaa_description",
                ),
                "generator_id",
            ),
        ]
    )
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.api.template_api.TemplatesAPI.create_by_generator")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_feature_template")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_device_template")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_cli_template")
    def test_templates_create_success(
        self,
        template,
        template_id,
        mock_create_cli_template,
        mock_create_device_template,
        mock_create_feature_template,
        mock_create_by_generator,
        mock_session,
    ):
        # Arrange
        mock_create_by_generator.return_value = "generator_id"
        mock_create_feature_template.return_value = "aaa_id"
        mock_create_device_template.return_value = "device_template_id"
        mock_create_cli_template.return_value = "cli_id"

        # Act
        templates_api = TemplatesAPI(mock_session)

        # Assert
        self.assertEqual(templates_api.create(template), template_id)

    @parameterized.expand(
        [
            (
                [
                    AAAModel(
                        template_name="test_template",
                        template_description="test_description",
                        auth_order=[AuthenticationOrder.LOCAL],
                        auth_fallback=False,
                        auth_disable_audit_logs=True,
                        auth_admin_order=True,
                        auth_disable_netconf_logs=False,
                    ),
                    DeviceTemplate(  # type: ignore
                        template_name="test_device_template",
                        template_description="test_device_template_description",
                        device_type=DeviceModel.VEDGE_2000,
                        general_templates=[],
                    ),
                    CLITemplate(  # type: ignore
                        template_name="test_cli_template",
                        template_description="test_cli_description",
                        device_model=DeviceModel.VBOND,
                    ),
                    CiscoAAAModel(  # type: ignore
                        template_name="test_aaa_model",
                        template_description="test_aaa_description",
                    ),
                ],
                ["aaa_id", "device_template_id", "cli_id", "generator_id"],
            ),
        ]
    )
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.api.template_api.TemplatesAPI.create_by_generator")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_feature_template")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_device_template")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_cli_template")
    def test_templates_create_list_success(
        self,
        templates,
        template_ids,
        mock_create_cli_template,
        mock_create_device_template,
        mock_create_feature_template,
        mock_create_by_generator,
        mock_session,
    ):
        # Arrange
        mock_create_by_generator.return_value = "generator_id"
        mock_create_feature_template.return_value = "aaa_id"
        mock_create_device_template.return_value = "device_template_id"
        mock_create_cli_template.return_value = "cli_id"

        # Act
        templates_api = TemplatesAPI(mock_session)

        # Assert
        self.assertEqual(templates_api.create(templates), template_ids)

    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.api.template_api.TemplatesAPI.create_by_generator")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_feature_template")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_device_template")
    @patch("catalystwan.api.template_api.TemplatesAPI._create_cli_template")
    def test_templates_create_failure(
        self,
        mock_create_cli_template,
        mock_create_device_template,
        mock_create_feature_template,
        mock_create_by_generator,
        mock_session,
    ):
        # Act
        templates_api = TemplatesAPI(mock_session)

        # Assert
        with self.assertRaises(NotImplementedError):
            templates_api.create(None)
        assert not mock_create_cli_template.called
        assert not mock_create_device_template.called
        assert not mock_create_feature_template.called
        assert not mock_create_by_generator.called

    # @patch.object(TemplatesAPI, "templates")
    # @patch("catalystwan.api.template_api.wait_for_completed")
    # @patch("catalystwan.session.ManagerSession")
    # def test_attach_exist_template(self, mock_session, mock_wait_for_completed, mock_templates):

    #     # Arrage
    #     mock_session.post_json.return_value = {"id": "operation_id"}
    #     test_object = TemplatesAPI(mock_session)

    #     # mock templates
    #     MockTemplates = Mock()
    #     mock_templates.return_value = MockTemplates
    #     test_object.templates = self.templates

    #     # mock wait complete
    #     mock_wait_for_completed.return_value = self.task

    #     # Act
    #     answer = test_object.attach("template_1", self.device_info)

    #     # Assert
    #     self.assertTrue(answer)

    # @patch.object(TemplatesAPI, "templates")
    # @patch("catalystwan.api.template_api.wait_for_completed")
    # @patch("catalystwan.session.ManagerSession")
    # def test_attach_no_exist_template(self, mock_session, mock_wait_for_completed, mock_templates):

    #     # Arrage
    #     mock_session.post_json.return_value = {"id": "operation_id"}
    #     test_object = TemplatesAPI(mock_session)

    #     # mock templates
    #     MockTemplates = Mock()
    #     mock_templates.return_value = MockTemplates
    #     test_object.templates = self.templates

    #     # mock wait complete
    #     mock_wait_for_completed.return_value = self.task

    #     # Act
    #     answer = test_object.attach("no_exist_template", self.device_info)

    #     # Assert
    #     self.assertFalse(answer)

    # @patch("catalystwan.api.template_api.wait_for_completed")
    # @patch("catalystwan.session.ManagerSession")
    # def test_device_to_cli_true(self, mock_session, mock_wait_for_completed):

    #     # Arrage
    #     mock_session.post_json.return_value = {"id": "operation_id"}
    #     test_object = TemplatesAPI(mock_session)

    #     # mock wait complete
    #     mock_wait_for_completed.return_value = self.task

    #     # Act
    #     answer = test_object.device_to_cli(self.device_info)

    #     # Assert
    #     self.assertTrue(answer)

    # @patch.object(TemplatesAPI, "templates")
    # @patch("catalystwan.session.ManagerSession")
    # def test_delete_success(self, mock_session, mock_templates):

    #     # Arrage
    #     MockResponse = MagicMock()
    #     MockResponse.status_code = 200
    #     mock_session.delete.return_value = MockResponse
    #     test_object = TemplatesAPI(mock_session)

    #     # mock templates
    #     MockTemplates = Mock()
    #     mock_templates.return_value = MockTemplates
    #     test_object.templates = self.templates

    #     # Act
    #     answer = test_object.delete("template_1")
    #     # Assert
    #     self.assertTrue(answer)

    # @patch.object(TemplatesAPI, "templates")
    # @patch("catalystwan.session.ManagerSession")
    # def test_delete_wrong_status(self, mock_session, mock_templates):

    #     # Arrage
    #     MockResponse = MagicMock()
    #     MockResponse.ok = False
    #     mock_session.delete.return_value = MockResponse
    #     test_object = TemplatesAPI(mock_session)

    #     # mock templates
    #     MockTemplates = Mock()
    #     mock_templates.return_value = MockTemplates
    #     test_object.templates = self.templates

    #     # Act
    #     answer = test_object.delete("template_1")

    #     # Assert
    #     self.assertFalse(answer)

    # @patch.object(TemplatesAPI, "templates")
    # @patch("catalystwan.session.ManagerSession")
    # def test_delete_exception(self, mock_session, mock_templates):

    #     # Arrage
    #     MockResponse = MagicMock()
    #     MockResponse.status = 404
    #     mock_session.delete.return_value = MockResponse
    #     test_object = TemplatesAPI(mock_session)

    #     # mock templates
    #     MockTemplates = Mock()
    #     mock_templates.return_value = MockTemplates
    #     test_object.templates = self.templates

    #     # Act
    #     def answer():
    #         return test_object.delete("template_2")

    #     # Assert
    #     self.assertRaises(AttachedError, answer)

    # @patch.object(TemplatesAPI, "templates")
    # @patch("catalystwan.session.ManagerSession")
    # def test_create_exception(self, mock_session, mock_templates):

    #     # Arrage
    #     test_object = TemplatesAPI(mock_session)

    #     # mock templates
    #     MockTemplates = Mock()
    #     mock_templates.return_value = MockTemplates
    #     test_object.templates = self.templates
    #     config = CiscoConfParse([])

    #     # Act
    #     def answer():
    #         return test_object.create(self.device_info, "template_1", "new_description", config)

    #     # Assert
    #     self.assertRaises(AlreadyExistsError, answer)
