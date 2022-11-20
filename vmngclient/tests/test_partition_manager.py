import unittest
from unittest.mock import MagicMock, Mock, patch

from vmngclient.api.repository_api import (DeviceCategory,
                                           DeviceSoftwareRepository,
                                           RepositoryAPI)
from vmngclient.api.partition_manager_api import (PartitionManagerAPI)
from vmngclient.dataclasses import DeviceInfo
from tenacity import RetryError


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
        ['ver1', 'ver2'],'curr_ver', 'def_ver','mock_uuid'),}

        self.mock_devices = [{"deviceId" : "mock_uuid", "deviceIP" : 'mock_ip', 'version' : 'ver1'}]

    @patch.object(PartitionManagerAPI,'_check_remove_partition_possibility')
    @patch.object(RepositoryAPI,'complete_device_list')
    def test_remove_partition_raise_error_force_false (self, mock_complete_device_list, 
        mock_check_remove):

        #Prepare mock data
        mock_complete_device_list.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],
        DeviceCategory.CEDGE.value)
        mock_repository_object.complete_device_list (
            'ver1', "available_versions").return_value = self.mock_devices  
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)
        mock_check_remove.return_value = ['mock_uuid']
        mock_repository_object.devices = self.mock_devices

        #Assert
        self.assertRaises(ValueError, mock_partition_manager_obj.remove_partition, 'ver1', False) 
    


    @patch.object(RepositoryAPI,'complete_device_list')
    def test_remove_partition_if_force_true (self, mock_complete_device_list):

        #Prepare mock data
        mock_complete_device_list.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],DeviceCategory.CEDGE.value)
        mock_devices = Mock()
        mock_devices.return_value = self.mock_devices
        mock_repository_object.complete_device_list (
            'ver1', "available_versions").return_value = self.mock_devices  
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)
        mock_repository_object.devices = self.mock_devices
        mock_repository_object.session.post_json.return_value = {'id' : 'mock_action_id'}
        
        #Assert
        answer = mock_partition_manager_obj.remove_partition('ver1',True)
        self.assertEqual(answer, 'mock_action_id', 'action ids not equal')
    
    @patch.object(PartitionManagerAPI,'_check_remove_partition_possibility')
    @patch.object(RepositoryAPI,'complete_device_list')
    def test_remove_partition_not_raise_error_force_false (self, mock_complete_device_list, 
        mock_check_remove):

        #Prepare mock data
        mock_complete_device_list.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],
        DeviceCategory.CEDGE.value)
        mock_repository_object.complete_device_list (
            'ver1', "available_versions").return_value = self.mock_devices  
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)
        mock_check_remove.return_value = None
        mock_repository_object.devices = self.mock_devices
        mock_repository_object.session.post_json.return_value = {'id' : 'mock_action_id'}

        #Assert
        answer = mock_partition_manager_obj.remove_partition('ver1',True)
        self.assertEqual(answer, 'mock_action_id', 'action ids not equal') 
    
    def test_check_remove_partition_possibility_if_version_incorrect(self):
        
        #Prepare mock data
        mock_devices = [{"deviceId" : "mock_uuid", "deviceIP" : 'mock_ip', 'version' : 'curr_ver'}]
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],
        DeviceCategory.CEDGE.value)
        mock_repository_object.devices = mock_devices
        mock_repository_object.devices_versions_repository = self.DeviceSoftwareRepository_obj
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)
        mock_devices = [{"deviceId" : "mock_uuid", "deviceIP" : 'mock_ip', 'version' : 'curr_ver'}]

        #Assert
        answer = mock_partition_manager_obj._check_remove_partition_possibility()

        self.assertEqual(answer, ['mock_uuid'], 'lists are not equal')
    
    def test_check_remove_partition_possibility_if_version_correct(self):
        
        #Prepare mock data
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],
        DeviceCategory.CEDGE.value)
        mock_repository_object.devices = self.mock_devices
        mock_repository_object.devices_versions_repository = self.DeviceSoftwareRepository_obj
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)

        #Assert
        answer = mock_partition_manager_obj._check_remove_partition_possibility()
        self.assertEqual(answer, None, 'value is diffrent than None')
    

    def test_wait_for_completed_success(self):

        #Prepare mock data
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],
        DeviceCategory.CEDGE.value)
        mock_repository_object.session.get_data.return_value = [{'status':'Success'}]
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)

        #Assert
        answer = mock_partition_manager_obj.wait_for_completed(5,500,['Success', 'Failure'],
        'mock_action_id')
        self.assertEqual(answer, 'Success', 'job status incorrect')
    
    def test_wait_for_completed_status_out_of_range(self):

        #Prepare mock data
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session,[self.device_info],
        DeviceCategory.CEDGE.value)
        mock_repository_object.session.get_data.return_value = [{'status':'other_status'}]
        mock_partition_manager_obj = PartitionManagerAPI(mock_repository_object)

        #assert
        self.assertRaises(RetryError, mock_partition_manager_obj.wait_for_completed,1,1,['Success', 'Failure'],
        'mock_action_id')
    



