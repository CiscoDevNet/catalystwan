import unittest
from typing import Any, Optional
from unittest.mock import patch

from attr import define, field  # type: ignore
from parameterized import parameterized  # type: ignore

from vmngclient.dataclasses import DataclassBase
from vmngclient.response import vManageResponse, vManageResponseErrorData, vManageResponseException
from vmngclient.typed_list import DataSequence


@define
class ParsedDataType(DataclassBase):
    key1: str
    key2: int
    key3: Optional[float] = field(default=None)


class TestResponse(unittest.TestCase):
    @parameterized.expand(
        [
            (True, None),
            (True, "string"),
            (True, {}),
            (True, {"key1": "string", "key2": 12, "key3": 4.5}),
            (True, 15),
            (True, {"data": None}),
            (True, {"data": {}}),
            (False, {"data": []}),
            (True, {"data": "something"}),
            (True, {"data": {"key1": "string", "key2": 12, "key3": None}}),
            (False, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}),
            (True, {"headers": {"key1": 1, "key2": "two"}}),
            (True, {"error": {"message": "Error happened!", "details": "error details", "code": "ABC123"}}),
        ]
    )
    @patch("requests.Response")
    def test_parse_list(self, raises: bool, json: Any, mock_response):
        mock_response.json.return_value = json
        vmng_response = vManageResponse(mock_response)
        if not raises:
            assert isinstance(vmng_response.parse_list(ParsedDataType), DataSequence)
        else:
            with self.assertRaises(vManageResponseException):
                vmng_response.parse_list(ParsedDataType)

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
            (False, {"data": {"key1": "string", "key2": 12, "key3": -0.7}}),
            (True, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}),
            (True, {"headers": {"key1": 1, "key2": "two"}}),
            (True, {"error": {"message": "Error happened!", "details": "error details", "code": "ABC123"}}),
        ]
    )
    @patch("requests.Response")
    def test_parse(self, raises: bool, json: Any, mock_response):
        mock_response.json.return_value = json
        vmng_response = vManageResponse(mock_response)
        if not raises:
            assert isinstance(vmng_response.parse(ParsedDataType), DataclassBase)
        else:
            with self.assertRaises(vManageResponseException):
                vmng_response.parse(ParsedDataType)

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
            assert isinstance(vmng_response.get_error(), vManageResponseErrorData)
        else:
            with self.assertRaises(vManageResponseException):
                vmng_response.get_error()
