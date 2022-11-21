import unittest
from unittest.mock import Mock, patch

from vmngclient.api.repository_api import DeviceCategory, DeviceSoftwareRepository, RepositoryAPI
from vmngclient.dataclasses import DeviceInfo


class TestRepositoryAPI(unittest.TestCase):

    def setUp(self):
        self.device_info = DeviceInfo(
                personality='vedge',
                uuid='mock_uuid',
                id='mock_ip',
                hostname='mock_host',
                reachability='reachable',
                local_system_ip='mock_ip',
                vedgeCertificateState='NA',
                cpuState='normal',
                chasisNumber='NA',
                memState='normal',
                status='normal',
                memUsage=1.0,
                cpuLoad=1.0,
                serialNumber='NA',
                configStatusMessage='NA',
                connected_vManages=['192.168.0.1'],
                model='vedge-cloud',
                stateDescription='All daemons up',
                board_serial=None,
            )
        self.DeviceSoftwareRepository_obj = {'mock_uuid':DeviceSoftwareRepository(['ver1', 'ver2', 'curr_ver'],
        ['ver1', 'ver2'],'curr_ver', 'def_ver','mock_uuid')}
 

    @patch('vmngclient.session.Session')
    def test_get_image_version_if_image_available(self,mock_session):
        
        versions_response = [{'availableFiles': 'vmanage-20.9.1-x86_64.tar.gz', 'versionName': '20.9.1'}]
        mock_session.get_data.return_value = versions_response
        image_version = '20.9.1'
        answer = RepositoryAPI(mock_session,[self.device_info],DeviceCategory.CEDGE.value).get_image_version('vmanage-20.9.1-x86_64.tar.gz')

        self.assertEqual(answer,image_version,'not same version')
   
    @patch('vmngclient.session.Session')
    def test_get_image_version_if_image_unavailable(self,mock_session):
        
        api_mock_response = [{'availableFiles': 'vmanage-20.9.2-x86_64.tar.gz',
                             'versionName': '20.9.1'}]
        mock_session.get_data.return_value = api_mock_response
        image_version = None
        answer = RepositoryAPI(mock_session,[self.device_info],DeviceCategory.CEDGE.value).get_image_version('vmanage-20.9.1-x86_64.tar.gz')

        self.assertEqual(answer,image_version,'not same version')


    @patch('vmngclient.session.Session')
    def test_create_devices_versions_repository(self,mock_session):

        api_mock_response = [{'availableVersions': ['ver1', 'ver2'],
         'version' : 'curr_ver', 'defaultVersion' : 'def_ver',
          'uuid' : 'mock_uuid'}] 
        mock_session.get_data.return_value = api_mock_response
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],DeviceCategory.CEDGE.value)

        answer = mock_repository_object.create_devices_versions_repository()
        
        self.assertEqual(answer['mock_uuid'],self.DeviceSoftwareRepository_obj['mock_uuid'],
        'DeviceSoftwareRepository object created uncorrectly')
    

    @patch.object(RepositoryAPI,"create_devices_versions_repository")
    def test_complete_device_list(self,mock_create_devices_versions_repository):
        mock_create_devices_versions_repository.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],DeviceCategory.CEDGE.value)
        mock_repository_object.create_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_repository_object.complete_device_list('ver1','available_versions')
        expected_result = [{'deviceId' : 'mock_uuid', 'deviceIP' : 'mock_ip', 'version' : 'ver1'}]
        self.assertEqual(mock_repository_object.devices, expected_result,"self.devices filled incorrectly")
    
    
    @patch.object(RepositoryAPI,"create_devices_versions_repository")
    def test_complete_device_list_raise_error(self,mock_create_devices_versions_repository):
        mock_create_devices_versions_repository.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],DeviceCategory.CEDGE.value)
        mock_repository_object.create_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        self.assertRaises(ValueError, mock_repository_object.complete_device_list,'ver3','available_versions')

