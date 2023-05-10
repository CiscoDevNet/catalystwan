import unittest
from unittest.mock import patch

from vmngclient.api.task_status_api import RunningTaskData, SubTaskData, Task, TaskResult, TasksAPI, TasksData


class TestTaskStatusApi(unittest.TestCase):
    def setUp(self):
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
        self.task_result = TaskResult(result=True, sub_tasks_data=[sub_tasks_data])
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
        self.running_task_data = RunningTaskData.parse_obj(
            {
                "detailsURL": "http://example.com",
                "userSessionUserName": "John",
                "@rid": 123,
                "tenantName": "",
                "processId": "processId_1",
                "name": "Some process",
                "tenantId": "456",
                "userSessionIP": "127.0.0.1",
                "action": "run",
                "startTime": 1649145600,
                "endTime": 1649174400,
                "status": "completed",
            }
        )
        self.running_task_data_json = {
            "runningTasks": [
                {
                    "detailsURL": "http://example.com",
                    "userSessionUserName": "John",
                    "@rid": 123,
                    "tenantName": "",
                    "processId": "processId_1",
                    "name": "Some process",
                    "tenantId": "456",
                    "userSessionIP": "127.0.0.1",
                    "action": "run",
                    "startTime": 1649145600,
                    "endTime": 1649174400,
                    "status": "completed",
                }
            ]
        }

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_success(self, mock_session):
        # Prepare mock data
        mock_session.get_data.return_value = self.action_data

        # Assert
        answer = Task(mock_session, "mock_action_id").wait_for_completed(3000, 5)
        self.assertEqual(answer, self.task_result)

    @patch("vmngclient.session.vManageSession")
    def test_wait_for_completed_status_out_of_range(self, mock_session):
        # Prepare mock data
        mock_session.get_data.return_value = self.action_data_time_out

        # Assert
        answer = Task(mock_session, "mock_action_id").wait_for_completed(1, 1).result
        self.assertEqual(answer, False)

    @patch("vmngclient.session.vManageSession")
    def test_get_all_tasks(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = self.running_task_data_json

        # Act
        answer = TasksAPI(mock_session, "").get_all_tasks()
        # Assert
        self.assertEqual(answer, TasksData.parse_obj(self.running_task_data_json))
