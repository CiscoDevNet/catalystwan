import unittest
from unittest.mock import Mock, patch
from vmngclient.api.task_status_api import wait_for_completed, TaskStatus
from tenacity import RetryError

class TestTaskStatusApi(unittest.TestCase):

    def setUp(self):
        self.task = TaskStatus('Success', "success", [])
        self.not_completed_task = TaskStatus("Other_status","other_status",[]) 

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_success(self,mock_session):

        #Prepare mock data
        mock_session.get_data.return_value = [{'status':'Success', "statusId": "success", "activity":[]}]

        #Assert
        answer = wait_for_completed(mock_session,
        'mock_action_id',3000,5)
        self.assertEqual(answer, self.task, 'job status incorrect')
 
    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_status_out_of_range(self, mock_session):

        #Prepare mock data
        mock_session.get_data.return_value = [{'status':'Other_status', "statusId": "other_status", "activity":[]}]
    
        #Assert
        # self.assertRaises(
        #     RetryError,
        #     wait_for_completed,
        # mock_session,
        # 'mock_action_id',1,1
        # 
        answer = wait_for_completed(mock_session,
        'mock_action_id',1,1)
        self.assertEqual(answer, self.not_completed_task, 'job status incorrect')