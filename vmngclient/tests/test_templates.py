import unittest
from unittest.mock import Mock, patch

from vmngclient.api.templates import TemplateAPI, TemplateNotFoundError
from vmngclient.dataclasses import DeviceInfo, Template
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.operation_status import OperationStatus
from vmngclient.utils.reachability import Reachability


class TestTemplateAPI(unittest.TestCase):
    def setUp(self):
        self.data_template = [
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
        self.templates = [create_dataclass(Template, template) for template in self.data_template]
        self.device_info = DeviceInfo(
            personality='vedge',
            uuid='dummy_uuid',
            id='162.168.0.1',
            hostname='dummy_host',
            reachability=Reachability.reachable,
            local_system_ip='192.168.0.1',
            vedgeCertificateState='NA',
            cpuState='normal',
            chasisNumber='NA',
            memState='normal',
            status='normal',
            memUsage=1.0,
            cpuLoad=1.0,
            serialNumber='NA',
            configOperationMode='NA',
            configStatusMessage='NA',
            connected_vManages=['192.168.0.1'],
            model='vedge-cloud',
            stateDescription='All daemons up',
            board_serial=None,
        )

    @patch('vmngclient.session.Session')
    def test_templates_success(self, mock_session):

        # Arrange
        mock_session.get_data.return_value = self.data_template

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
        MockTemplates = Mock()
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
        MockTemplates = Mock()
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

    @patch.object(TemplateAPI, 'templates')
    def test_get_id_exception(self, mock_templates):

        # Arrage
        MockTemplates = Mock()
        mock_templates.return_value = MockTemplates
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.templates = self.templates

        # Act
        def answer():
            return test_object.get_id('no_exist_name')

        # Assert
        self.assertRaises(TemplateNotFoundError, answer)

    @patch.object(TemplateAPI, "get_operation_status")
    def test_wait_complete_true(self, mock_operation):

        # Arrage
        MockOperatrion = Mock()
        mock_operation.return_value = MockOperatrion
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.get_operation_status.return_value = [OperationStatus.SUCCESS, OperationStatus.SUCCESS]
        operation_id = 'operation_id'

        # Act
        answer = test_object.wait_complete(operation_id)

        # Assert
        self.assertTrue(answer)

    @patch.object(TemplateAPI, "get_operation_status")
    def test_wait_complete_false(self, mock_operation):

        # Arrage
        MockOperatrion = Mock()
        mock_operation.return_value = MockOperatrion
        session = Mock()
        test_object = TemplateAPI(session)
        test_object.get_operation_status.return_value = [OperationStatus.IN_PROGRESS, OperationStatus.SUCCESS]
        operation_id = 'operation_id'

        # Act
        answer = test_object.wait_complete(operation_id, timeout_seconds=2, sleep_seconds=1)

        # Assert
        self.assertFalse(answer)

    @patch('vmngclient.session.Session')
    @patch.object(TemplateAPI, "get_id")
    @patch.object(TemplateAPI, "wait_complete")
    def test_attach_true(self, mock_session, mock_wait_complete, mock_get_id):

        # Arrage
        mock_session.post_json.return_value = {"id": "operation_id"}
        test_object = TemplateAPI(mock_session)

        # mock get id
        MockTemplateId = Mock()
        mock_get_id.return_value = MockTemplateId
        test_object.get_id.return_value = 'dummy_id'

        # mock wait complete
        MockWaitComplete = Mock()
        mock_wait_complete.return_value = MockWaitComplete
        test_object.wait_complete.return_value = True

        # Act
        answer = test_object.attach('dummy_name', self.device_info)

        # Assert
        self.assertTrue(answer)

    def test_device_to_cli_true(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_device_to_cli_false(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_get_operatrion_status_success(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_get_operatrion_status_no_data(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_delete(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_delete_exception(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_create(self):
        pass

        # Arrage

        # Act

        # Assert

    def test_create_exceptrion(self):
        pass

        # Arrage

        # Act

        # Assert
