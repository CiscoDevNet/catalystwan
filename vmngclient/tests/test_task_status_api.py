import unittest
from unittest.mock import patch

from vmngclient.api.task_status_api import TaskStatus, get_all_tasks, wait_for_completed


class TestTaskStatusApi(unittest.TestCase):
    def setUp(self):
        self.task = TaskStatus("Success", "success", [])
        self.action_data = [{"status": "Success", "statusId": "success", "activity": []}]

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_success(self, mock_session):
        # Prepare mock data
        mock_session.get_data.return_value = self.action_data

        # Assert
        answer = wait_for_completed(mock_session, "mock_action_id", 3000, 5)
        self.assertEqual(answer, self.task, "job status incorrect")

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_status_out_of_range(self, mock_session):
        # Prepare mock data
        mock_session.get_data.return_value = [{"status": "Other_status", "statusId": "other_status", "activity": []}]

        # Assert
        answer = wait_for_completed(mock_session, "mock_action_id", 1, 1)
        self.assertEqual(answer, None, "job status incorrect")

    @patch("vmngclient.api.task_status_api.sleep")
    @patch("vmngclient.api.task_status_api.get_all_tasks")
    @patch("vmngclient.session.vManageSession")
    def test_raise_index_error_actionid_in_tasks_ids_data_exists(self, mock_session, mock_get_tasks, mock_sleep):
        # Arrange
        mock_session.get_data.side_effect = [IndexError(), self.action_data]
        mock_get_tasks.return_value = ["action_id"]
        # Act
        answer = wait_for_completed(mock_session, "action_id", 1, 1)
        # Assert
        self.assertEqual(answer, self.task)

    @patch("vmngclient.api.task_status_api.sleep")
    @patch("vmngclient.api.task_status_api.get_all_tasks")
    @patch("vmngclient.session.vManageSession")
    def test_raise_index_error_actionid_in_tasks_ids_data_dosnt_exists(self, mock_session, mock_get_tasks, mock_sleep):
        # Arrange
        mock_session.get_data.side_effect = [IndexError(), []]
        mock_get_tasks.return_value = ["action_id"]
        # Act&Assert
        self.assertRaises(IndexError, wait_for_completed, mock_session, "action_id", 1, 1)

    @patch("vmngclient.api.task_status_api.sleep")
    @patch("vmngclient.api.task_status_api.get_all_tasks")
    @patch("vmngclient.session.vManageSession")
    def test_raise_index_error_actionid_not_in_tasks(self, mock_session, mock_get_tasks, mock_sleep):
        # Arrange
        mock_session.get_data.side_effect = IndexError()
        mock_get_tasks.return_value = ["no_id"]
        # Act&Assert
        self.assertRaises(ValueError, wait_for_completed, mock_session, "action_id", 1, 1)

    @patch("vmngclient.session.vManageSession")
    def test_get_all_tasks(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = {
            "runningTasks": [{"processId": "processId_1"}, {"processId": "processId_2"}]
        }
        # Act
        answer = get_all_tasks(mock_session)
        # Assert
        self.assertEqual(answer, ["processId_1", "processId_2"])
