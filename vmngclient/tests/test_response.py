import unittest
from typing import Any, Optional
from unittest.mock import patch

from attr import define, field  # type: ignore
from parameterized import parameterized  # type: ignore

from vmngclient.dataclasses import DataclassBase
from vmngclient.response import ErrorInfo, vManageResponse
from vmngclient.typed_list import DataSequence


@define
class ParsedDataType(DataclassBase):
    key1: str
    key2: int
    key3: Optional[float] = field(default=None)


class TestResponse(unittest.TestCase):
    @parameterized.expand(
        [
            (True, None, 0),
            (True, "string", 0),
            (True, {}, 0),
            (True, {"key1": "string", "key2": 12, "key3": 4.5}, 0),
            (True, 15, 0),
            (True, {"data": None}, 0),
            (True, {"data": {}}, 0),
            (False, {"data": []}, 0),
            (True, {"data": "something"}, 0),
            (False, {"data": {"key1": "string", "key2": 12, "key3": None}}, 1),
            (False, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}, 2),
            (True, {"headers": {"key1": 1, "key2": "two"}}, 0),
            (True, {"error": {"message": "Error happened!", "details": "error details", "code": "ABC123"}}, 0),
        ]
    )
    @patch("requests.Response")
    def test_dataseq(self, raises: bool, json: Any, expected_len: int, mock_response):
        mock_response.json.return_value = json
        vmng_response = vManageResponse(mock_response)
        if not raises:
            data_sequence = vmng_response.dataseq(ParsedDataType)
            assert isinstance(data_sequence, DataSequence)
            assert len(data_sequence) == expected_len
        else:
            with self.assertRaises(Exception):
                vmng_response.dataseq(ParsedDataType)

    @parameterized.expand(
        [
            (True, None),
            (True, "string"),
            (True, {}),
            (True, {"key1": "string", "key2": 12, "key3": 4.5}),
            (True, 15),
            (True, {"data": None}),
            (True, {"data": {}}),
            (True, {"data": []}),
            (True, {"data": "something"}),
            (True, {"data": {"key1": "string", "key2": 12, "key3": -0.7}}),
            (True, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}),
            (True, {"headers": {"key1": 1, "key2": "two"}}),
            (False, {"error": {"message": "Error happened!", "details": "error details", "code": "ABC123"}}),
        ]
    )
    @patch("requests.Response")
    def test_get_error(self, raises: bool, json: Any, mock_response):
        mock_response.json.return_value = json
        vmng_response = vManageResponse(mock_response)
        if not raises:
            assert isinstance(vmng_response.get_error_info(), ErrorInfo)
        else:
            with self.assertRaises(Exception):
                vmng_response.get_error_info()
