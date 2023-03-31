import unittest
from unittest.mock import patch

from vmngclient.api.task_status_api import SubTaskData, TaskAPI, TaskResult
from vmngclient.exceptions import EmptyTaskResponseError, TaskNotRegisteredError
from vmngclient.typed_list import DataSequence


class TestTaskStatusApi(unittest.TestCase):
    def setUp(self):
        self.task_result = TaskResult(
            True, DataSequence(SubTaskData, [SubTaskData("Success", "success", "", [], "", "", 1, "", "", "")])
        )
        self.action_data = [
            {
                "status": "Success",
                "statusId": "success",
                "activity": [],
                "action": "",
                "currentActivity": "",
                "actionConfig": "",
                "order": 1,
                "uuid": "",
                "host-name": "",
                "site-id": "",
            }
        ]
        self.action_data_time_out = [
            {
                "status": "Other_status",
                "statusId": "other_status",
                "activity": [],
                "action": "",
                "currentActivity": "",
                "actionConfig": "",
                "order": 1,
                "uuid": "",
                "host-name": "",
                "site-id": "",
            }
        ]

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_success(self, mock_session):
        # Prepare mock data
        mock_session.get_data.return_value = self.action_data

        # Assert
        answer = TaskAPI(mock_session, "mock_action_id").wait_for_completed(3000, 5)
        self.assertEqual(answer, self.task_result)

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_status_out_of_range(self, mock_session):
        # Prepare mock data
        mock_session.get_data.return_value = self.action_data_time_out

        # Assert
        answer = TaskAPI(mock_session, "mock_action_id").wait_for_completed(1, 1).result
        self.assertEqual(answer, False)

    @patch("vmngclient.api.task_status_api.sleep")
    @patch.object(TaskAPI, "_TaskAPI__get_all_tasks")
    @patch("vmngclient.session.vManageSession")
    def test_raise_index_error_actionid_in_tasks_ids_data_exists(self, mock_session, mock_get_tasks, mock_sleep):
        # Arrange
        mock_session.get_data.side_effect = [[], self.action_data]
        mock_get_tasks.return_value = ["action_id"]
        # Act
        answer = TaskAPI(mock_session, "action_id").wait_for_completed(1, 1)
        # Assert
        self.assertEqual(answer, self.task_result)

    @patch("vmngclient.api.task_status_api.sleep")
    @patch.object(TaskAPI, "_TaskAPI__get_all_tasks")
    @patch("vmngclient.session.vManageSession")
    def test_raise_error_actionid_in_tasks_ids_data_dosnt_exists(self, mock_session, mock_get_tasks, mock_sleep):
        # Arrange
        mock_session.get_data.return_value = []
        mock_get_tasks.return_value = ["action_id"]
        # Act&Assert
        self.assertRaises(
            EmptyTaskResponseError, TaskAPI(mock_session, "action_id").wait_for_completed, mock_session, 1, 1
        )

    @patch("vmngclient.api.task_status_api.sleep")
    @patch.object(TaskAPI, "_TaskAPI__get_all_tasks")
    @patch("vmngclient.session.vManageSession")
    def test_raise_index_error_actionid_not_in_tasks(self, mock_session, mock_get_tasks, mock_sleep):
        # Arrange
        mock_session.get_data.return_value = []
        mock_get_tasks.return_value = ["no_id"]
        # Act&Assert
        self.assertRaises(
            TaskNotRegisteredError, TaskAPI(mock_session, "action_id").wait_for_completed, mock_session, 1, 1
        )

    @patch("vmngclient.session.vManageSession")
    def test_get_all_tasks(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = {
            "runningTasks": [{"processId": "processId_1"}, {"processId": "processId_2"}]
        }
        # Act
        answer = TaskAPI(mock_session, "")._TaskAPI__get_all_tasks()
        # Assert
        self.assertEqual(answer, ["processId_1", "processId_2"])
