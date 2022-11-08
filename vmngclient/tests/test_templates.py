import unittest
from unittest.mock import MagicMock, Mock, patch

from vmngclient.api.templates import TemplateAPI, TemplateNotFoundError
from vmngclient.dataclasses import Template
from vmngclient.utils.creation_tools import create_dataclass


class TestTemplateAPI(unittest.TestCase):
    def setUp(self):
        self.data = [
            {
                'deviceType': 'vedge-C8000V',
                'lastUpdatedBy': 'user',
                'resourceGroup': 'global',
                'templateClass': 'cedge',
                'configType': 'file',
                'templateId': 'dummy_id_1',
                'factoryDefault': False,
                'templateName': 'template_1',
                'devicesAttached': 1,
                'templateDescription': 'dummy template 1',
                'draftMode': 'Disabled',
                'lastUpdatedOn': 0,
                'templateAttached': 0,
            },
            {
                'deviceType': 'vedge-cloud',
                'lastUpdatedBy': 'admin',
                'resourceGroup': 'global',
                'templateClass': 'vedge',
                'configType': 'file',
                'templateId': 'dummy_id_2',
                'factoryDefault': False,
                'templateName': 'template_2',
                'devicesAttached': 1,
                'templateDescription': 'dummy template 2',
                'draftMode': 'Disabled',
                'lastUpdatedOn': 0,
                'templateAttached': 0,
            },
        ]
        self.templates = [create_dataclass(Template, template) for template in self.data]

    @patch('vmngclient.session.Session')
    def test_templates_success(self, mock_session):

        # Arrange
        mock_session.get_data.return_value = self.data

        # Act
        answer = TemplateAPI(mock_session).templates

        # Assert
        self.assertEqual(answer, self.templates)

    @patch('vmngclient.session.Session')
    def test_templates_no_data(self, mock_session):

        # Arrange
        mock_session.get_data.return_value = []

        # Act
        answer = TemplateAPI(mock_session).templates

        # Assert
        self.assertEqual(answer, [])

    @patch.object(TemplateAPI, 'templates')
    def test_get_success(self, mock_templates):

        # Arrage
        MockTemplates = MagicMock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        answer = [test_object.get(template.name) for template in self.templates]

        # Assert
        self.assertEqual(answer, self.templates)

    @patch.object(TemplateAPI, 'templates')
    def test_get_exception(self, mock_templates):

        # Arrage
        MockTemplates = MagicMock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        def answer():
            return test_object.get('no_exist_name')

        # Assert
        self.assertRaises(TemplateNotFoundError, answer)

    @patch.object(TemplateAPI, 'templates')
    def test_get_id_success(self, mock_templates):

        # Arrage
        MockTemplates = MagicMock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        answer = [test_object.get_id(template.name) for template in self.templates]

        ids = [template.id for template in self.templates]
        # Assert
        self.assertEqual(answer, ids)

    @patch.object(TemplateAPI, 'templates')
    def test_get_id_exception(self, mock_templates):

        # Arrage
        MockTemplates = MagicMock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        def answer():
            return test_object.get_id('no_exist_name')

        # Assert
        self.assertRaises(TemplateNotFoundError, answer)

    def test_wait_complete_true(self):
        pass

    def test_wait_complete_false(self):
        pass

    def test_attach_true(self):
        pass

    def test_attach_false(self):
        pass

    def test_device_to_cli_true(self):
        pass

    def test_device_to_cli_false(self):
        pass

    def test_get_operatrion_status_success(self):
        pass

    def test_get_operatrion_status_no_data(self):
        pass

    def test_delete(self):
        pass

    def test_delete_exception(self):
        pass

    def test_create(self):
        pass

    def test_create_exceptrion(self):
        pass
