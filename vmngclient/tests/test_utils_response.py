import unittest
from typing import Any
from unittest.mock import patch

from parameterized import parameterized  # type: ignore

from vmngclient.utils.response import (
    VManageResponseException,
    get_json_data,
    get_json_data_as_dict,
    get_json_data_as_list,
)


class TestResponse(unittest.TestCase):
    @parameterized.expand(
        [
            (True, None),
            (True, "string"),
            (True, {}),
            (True, {"key1": "string", "key2": 12, "key3": {"nested": None}}),
            (True, 15),
            (False, {"data": None}),
            (False, {"data": {}}),
            (False, {"data": []}),
            (False, {"data": "something"}),
            (False, {"data": [1, 2, 3]}),
            (False, {"data": {"key1": "string", "key2": 12, "key3": None}}),
            (False, {"data": [{"key1": "string"}, {"key2": {}, "key3": None}, "data"]}),
        ]
    )
    @patch("requests.Response")
    def test_get_json_data(self, raises: bool, json: Any, mock_response):
        mock_response.json.return_value = json
        if not raises:
            self.assertEqual(get_json_data(mock_response), json["data"])
        else:
            with self.assertRaises(VManageResponseException):
                get_json_data(mock_response)

    @parameterized.expand(
        [
            (True, None),
            (True, "string"),
            (True, {}),
            (True, {"key1": "string", "key2": 12, "key3": {"nested": None}}),
            (True, 15),
            (True, {"data": None}),
            (True, {"data": {}}),
            (False, {"data": []}),
            (True, {"data": "something"}),
            (False, {"data": [1, 2, 3]}),
            (True, {"data": {"key1": "string", "key2": 12, "key3": None}}),
            (False, {"data": [{"key1": "string"}, {"key2": {}, "key3": None}, "data"]}),
        ]
    )
    @patch("requests.Response")
    def test_get_json_data_as_list(self, raises: bool, json: Any, mock_response):
        mock_response.json.return_value = json
        if not raises:
            self.assertEqual(get_json_data_as_list(mock_response), json["data"])
        else:
            with self.assertRaises(VManageResponseException):
                get_json_data_as_list(mock_response)

    @parameterized.expand(
        [
            (True, None),
            (True, "string"),
            (True, {}),
            (True, {"key1": "string", "key2": 12, "key3": {"nested": None}}),
            (True, 15),
            (True, {"data": None}),
            (False, {"data": {}}),
            (True, {"data": []}),
            (True, {"data": "something"}),
            (True, {"data": [1, 2, 3]}),
            (False, {"data": {"key1": "string", "key2": 12, "key3": None}}),
            (True, {"data": [{"key1": "string"}, {"key2": {}, "key3": None}, "data"]}),
        ]
    )
    @patch("requests.Response")
    def test_get_json_data_as_dict(self, raises: bool, json: Any, mock_response):
        mock_response.json.return_value = json
        if not raises:
            self.assertEqual(get_json_data_as_dict(mock_response), json["data"])
        else:
            with self.assertRaises(VManageResponseException):
                get_json_data_as_dict(mock_response)
