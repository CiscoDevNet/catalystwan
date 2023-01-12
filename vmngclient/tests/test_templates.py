import unittest
from unittest.mock import MagicMock, Mock, patch

from ciscoconfparse import CiscoConfParse  # type: ignore

from vmngclient.api.task_status_api import TaskStatus
from vmngclient.api.templates import AttachedError, NameAlreadyExistError, NotFoundError, TemplateAPI
from vmngclient.dataclasses import Device, Template
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.personality import Personality
from vmngclient.utils.reachability import Reachability


class TestTemplateAPI(unittest.TestCase):
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
        self.templates = [create_dataclass(Template, template) for template in self.data_template]
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
        self.task = TaskStatus("Success", "success", [])

    @patch("vmngclient.session.vManageSession")
    def test_templates_success(self, mock_session):

        # Arrange
        mock_session.get_data.return_value = self.data_template

        # Act
        answer = TemplateAPI(mock_session).templates

        # Assert
        self.assertEqual(answer, self.templates)

    @patch("vmngclient.session.vManageSession")
    def test_templates_no_data(self, mock_session):

        # Arrange
        mock_session.get_data.return_value = []

        # Act
        answer = TemplateAPI(mock_session).templates

        # Assert
        self.assertEqual(answer, [])

    @patch.object(TemplateAPI, "templates")
    def test_get_success(self, mock_templates):

        # Arrage
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        answer = [test_object.get(template.name) for template in self.templates]

        # Assert
        self.assertEqual(answer, self.templates)

    @patch.object(TemplateAPI, "templates")
    def test_get_exception(self, mock_templates):

        # Arrage
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        def answer():
            return test_object.get("no_exist_name")

        # Assert
        self.assertRaises(NotFoundError, answer)

    @patch.object(TemplateAPI, "templates")
    def test_get_id_success(self, mock_templates):

        # Arrage
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        answer = [test_object.get_id(template.name) for template in self.templates]

        ids = [template.id for template in self.templates]
        # Assert
        self.assertEqual(answer, ids)

    @patch.object(TemplateAPI, "templates")
    def test_get_id_exception(self, mock_templates):

        # Arrage
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        def answer():
            return test_object.get_id("no_exist_name")

        # Assert
        self.assertRaises(NotFoundError, answer)

    @patch.object(TemplateAPI, "templates")
    @patch("vmngclient.api.templates.wait_for_completed")
    @patch("vmngclient.session.vManageSession")
    def test_attach_exist_template(self, mock_session, mock_wait_for_completed, mock_templates):

        # Arrage
        mock_session.post_json.return_value = {"id": "operation_id"}
        test_object = TemplateAPI(mock_session)

        # mock templates
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        test_object.templates = self.templates

        # mock wait complete
        mock_wait_for_completed.return_value = self.task

        # Act
        answer = test_object.attach("template_1", self.device_info)

        # Assert
        self.assertTrue(answer)

    @patch.object(TemplateAPI, "templates")
    @patch("vmngclient.api.templates.wait_for_completed")
    @patch("vmngclient.session.vManageSession")
    def test_attach_no_exist_template(self, mock_session, mock_wait_for_completed, mock_templates):

        # Arrage
        mock_session.post_json.return_value = {"id": "operation_id"}
        test_object = TemplateAPI(mock_session)

        # mock templates
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        test_object.templates = self.templates

        # mock wait complete
        mock_wait_for_completed.return_value = self.task

        # Act
        answer = test_object.attach("no_exist_template", self.device_info)

        # Assert
        self.assertFalse(answer)

    @patch("vmngclient.api.templates.wait_for_completed")
    @patch("vmngclient.session.vManageSession")
    def test_device_to_cli_true(self, mock_session, mock_wait_for_completed):

        # Arrage
        mock_session.post_json.return_value = {"id": "operation_id"}
        test_object = TemplateAPI(mock_session)

        # mock wait complete
        mock_wait_for_completed.return_value = self.task

        # Act
        answer = test_object.device_to_cli(self.device_info)

        # Assert
        self.assertTrue(answer)

    @patch.object(TemplateAPI, "templates")
    @patch("vmngclient.session.vManageSession")
    def test_delete_success(self, mock_session, mock_templates):

        # Arrage
        MockResponse = MagicMock()
        MockResponse.status_code = 200
        mock_session.delete.return_value = MockResponse
        test_object = TemplateAPI(mock_session)

        # mock templates
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        test_object.templates = self.templates

        # Act
        answer = test_object.delete("template_1")
        # Assert
        self.assertTrue(answer)

    @patch.object(TemplateAPI, "templates")
    @patch("vmngclient.session.vManageSession")
    def test_delete_wrong_status(self, mock_session, mock_templates):

        # Arrage
        MockResponse = MagicMock()
        MockResponse.ok = False
        mock_session.delete.return_value = MockResponse
        test_object = TemplateAPI(mock_session)

        # mock templates
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        test_object.templates = self.templates

        # Act
        answer = test_object.delete("template_1")

        # Assert
        self.assertFalse(answer)

    @patch.object(TemplateAPI, "templates")
    @patch("vmngclient.session.vManageSession")
    def test_delete_exception(self, mock_session, mock_templates):

        # Arrage
        MockResponse = MagicMock()
        MockResponse.status = 404
        mock_session.delete.return_value = MockResponse
        test_object = TemplateAPI(mock_session)

        # mock templates
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        test_object.templates = self.templates

        # Act
        def answer():
            return test_object.delete("template_2")

        # Assert
        self.assertRaises(AttachedError, answer)

    @patch.object(TemplateAPI, "templates")
    @patch("vmngclient.session.vManageSession")
    def test_create_exception(self, mock_session, mock_templates):

        # Arrage
        test_object = TemplateAPI(mock_session)

        # mock templates
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        test_object.templates = self.templates
        config = CiscoConfParse([])

        # Act
        def answer():
            return test_object.create(self.device_info, "template_1", "new_description", config)

        # Assert
        self.assertRaises(NameAlreadyExistError, answer)
