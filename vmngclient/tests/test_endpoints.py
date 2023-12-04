# mypy: disable-error-code="annotation-unchecked"
import json
import tempfile
import unittest
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union
from unittest.mock import MagicMock

import pytest  # type: ignore
from packaging.version import Version  # type: ignore
from parameterized import parameterized  # type: ignore
from pydantic import BaseModel as BaseModelV2
from pydantic import Field as FieldV2
from pydantic.v1 import BaseModel as BaseModelV1
from typing_extensions import Annotated

from vmngclient.endpoints import (
    BASE_PATH,
    JSON,
    APIEndpoints,
    CustomPayloadType,
    PreparedPayload,
    TypeSpecifier,
    delete,
    get,
)
from vmngclient.endpoints import logger as endpoints_logger
from vmngclient.endpoints import post, put, request, versions, view
from vmngclient.exceptions import APIEndpointError, APIRequestPayloadTypeError, APIVersionError, APIViewError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.session_type import ProviderAsTenantView, ProviderView, TenantView


class BaseModelV1Example(BaseModelV1):
    id: str
    size: int
    capacity: float
    active: bool


class ParamsModelV1Example(BaseModelV1):
    name: str
    color: str


class BaseModelV2Example(BaseModelV2):
    id: str
    size: int
    capacity: float
    active: bool


class BaseModelV2Example2(BaseModelV2):
    other_id: str
    active: bool


class ParamsModelV2Example(BaseModelV2):
    name: str
    color: str


class CustomTypeExample(CustomPayloadType):
    def __init__(self, filename: Path):
        self.filename = filename

    def prepared(self) -> PreparedPayload:
        data = open(self.filename, "rb")
        return PreparedPayload(files={"file": (Path(data.name).name, data)})


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.base_path = BASE_PATH
        self.session_mock = MagicMock()
        self.session_mock.request = MagicMock(return_value=MagicMock())
        self.session_mock.api_version = None
        self.session_mock.session_type = None
        self.endpoints = APIEndpoints(self.session_mock)
        self.dict_payload = {
            "id": "XYZ-189",
            "size": 100,
            "capacity": 1.7,
            "active": True,
        }
        self.json_payload = json.dumps(self.dict_payload)
        self.basemodel_v1_payload = BaseModelV1Example.parse_obj(self.dict_payload)
        self.basemodel_v2_payload = BaseModelV2Example.model_validate(self.dict_payload)
        self.list_dict_payload = [self.dict_payload] * 2
        self.dict_params = {
            "name": "purple",
            "color": "haze",
        }
        self.basemodel_v1_params = ParamsModelV1Example.parse_obj(self.dict_params)
        self.basemodel_v2_params = ParamsModelV2Example.model_validate(self.dict_params)
        self.basemodel_v1_sequence_payload = [self.basemodel_v1_payload] * 2
        self.basemodel_v2_sequence_payload = [self.basemodel_v2_payload] * 2

    @parameterized.expand(
        [
            ("<2.0", "1.9.9"),
            (">=1.9, !=3.0", "3.1"),
            (">0.9, <=1.3", "1.3"),
        ]
    )
    def test_versions_decorator_passes(self, supported_versions, current_version):
        class ExampleAPI(APIEndpoints):
            @versions(supported_versions=supported_versions, raises=True)
            def versions_decorated_method(self):
                pass

        self.session_mock.api_version = Version(current_version)
        api = ExampleAPI(self.session_mock)
        api.versions_decorated_method()

    @parameterized.expand(
        [
            ("<2.0", "2.0"),
            ("<=1.9, !=3.0", "3.0"),
            (">0.9, <1.3", "1.3"),
        ]
    )
    def test_versions_decorator_raises(self, supported_versions, current_version):
        class ExampleAPI(APIEndpoints):
            @versions(supported_versions=supported_versions, raises=True)
            def versions_decorated_method(self):
                pass

        self.session_mock.api_version = Version(current_version)
        api = ExampleAPI(self.session_mock)
        with self.assertRaises(APIVersionError):
            api.versions_decorated_method()

    def test_version_decorator_logs_warning(self):
        supported_versions = "<1.6"
        current_version = "1.7"

        class ExampleAPI(APIEndpoints):
            @versions(supported_versions=supported_versions, raises=False)
            def versions_decorated_method(self):
                pass

        self.session_mock.api_version = Version(current_version)
        api = ExampleAPI(self.session_mock)
        with self.assertLogs(endpoints_logger, level="WARNING") as log:
            api.versions_decorated_method()
            assert supported_versions in log.output[0]
            assert current_version in log.output[0]

    @parameterized.expand(
        [
            ({ProviderView}, ProviderView),
            ({TenantView, ProviderAsTenantView}, TenantView),
            ({ProviderAsTenantView}, ProviderAsTenantView),
        ]
    )
    def test_view_decorator_passes(self, allowed_sessions, current_session):
        class ExampleAPI(APIEndpoints):
            @view(allowed_session_types=allowed_sessions, raises=True)
            def versions_decorated_method(self):
                pass

        self.session_mock.session_type = current_session
        api = ExampleAPI(self.session_mock)
        api.versions_decorated_method()

    @parameterized.expand(
        [
            ({ProviderView}, ProviderAsTenantView),
            ({TenantView, ProviderAsTenantView}, ProviderView),
            ({ProviderAsTenantView}, TenantView),
        ]
    )
    def test_view_decorator_raises(self, allowed_sessions, current_session):
        class ExampleAPI(APIEndpoints):
            @view(allowed_session_types=allowed_sessions, raises=True)
            def versions_decorated_method(self):
                pass

        self.session_mock.session_type = current_session
        api = ExampleAPI(self.session_mock)
        with self.assertRaises(APIViewError):
            api.versions_decorated_method()

    def test_view_decorator_logs_warinig(self):
        allowed_sessions = {ProviderAsTenantView, TenantView}
        current_session = ProviderView

        class ExampleAPI(APIEndpoints):
            @view(allowed_session_types=allowed_sessions)
            def versions_decorated_method(self):
                pass

        self.session_mock.session_type = current_session
        api = ExampleAPI(self.session_mock)
        with self.assertLogs(endpoints_logger, level="WARNING") as log:
            api.versions_decorated_method()
            for allowed in allowed_sessions:
                assert str(allowed) in log.output[0]
            assert str(current_session) in log.output[0]

    def test_basemodel_v1_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.basemodel_v1_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.dict_payload

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_basemodel_v2_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.basemodel_v2_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.dict_payload

    def test_basemodel_v1_sequence_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.basemodel_v1_sequence_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.list_dict_payload

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_basemodel_v2_sequence_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.basemodel_v2_sequence_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.list_dict_payload

    def test_custom_payload(self):
        expected_data = b"\xFFsomething\x00"
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)
            payload_file = tempdir_path / "payload.bin"
            with open(payload_file, "wb") as tmpfile:
                tmpfile.write(expected_data)
            custom_payload = CustomTypeExample(payload_file)
            self.endpoints._request("POST", f"/{__name__}", payload=custom_payload)
            _, kwargs = self.session_mock.request.call_args
            prepared = custom_payload.prepared()
            assert kwargs.get("data") == prepared.data
            assert kwargs.get("headers") == prepared.headers
            assert kwargs.get("files")["file"][0] == prepared.files["file"][0]

    def test_dict_payload(self):
        self.endpoints._request("POST", f"/{__name__}", payload=self.dict_payload)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("data") == self.json_payload

    @parameterized.expand(
        [
            ("JStr", str),
            (1, int),
            (3.33, float),
            (True, bool),
            ({"a": {"b": [1.6]}}, dict),
            ([1, 2, {"a": {"b": [1.6]}}], list),
        ]
    )
    def test_forced_json_payload(self, payload, _):
        self.endpoints._request("POST", f"/{__name__}", payload=payload, force_json_payload=True)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("data") == json.dumps(payload)

    def test_str_payload(self):
        str_payload = "This is string payload!"
        self.endpoints._request("POST", f"/{__name__}", payload=str_payload)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("data") == str_payload

    def test_bytes_payload(self):
        bytes_payload = b"\xEFtest\x00"
        self.endpoints._request("POST", f"/{__name__}", payload=bytes_payload)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("data") == bytes_payload

    def test_unexpected_payload(self):
        with self.assertRaises(APIRequestPayloadTypeError):
            self.endpoints._request("GET", f"/{__name__}", payload={1, 2, 3})

    def test_dict_params(self):
        self.endpoints._request("POST", f"/{__name__}", params=self.dict_params)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("params") == self.dict_params

    def test_basemodel_v1_params(self):
        self.endpoints._request("POST", f"/{__name__}", params=self.basemodel_v1_params)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("params") == self.dict_params

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_basemodel_v2_params(self):
        self.endpoints._request("POST", f"/{__name__}", params=self.basemodel_v2_params)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("params") == self.dict_params

    def test_request_decorator_forbidden_url_field_name(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("GET", "/v1/data/{payload}")
                def get_data(self, payload: str) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_return_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("GET", "/v1/data/")
                def get_data(self) -> DataSequence:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_datasequence_return_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("GET", "/v1/data/")
                def get_data(self) -> DataSequence[str]:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_composite_return_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("GET", "/v1/data")
                def get_data(self) -> List[BaseModelV1Example]:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_payload_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, payload: DataSequence) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_payload_sequence_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, payload: List[str]) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_payload_composite_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, payload: Dict[str, BaseModelV1Example]) -> None:  # type: ignore [empty-body]
                    ...

    @parameterized.expand(
        [
            (BaseModelV1Example, False, TypeSpecifier(True, None, BaseModelV1Example, None, False, False)),
            (List[BaseModelV1Example], False, TypeSpecifier(True, list, BaseModelV1Example, None, False, False)),
            (Optional[BaseModelV1Example], False, TypeSpecifier(True, None, BaseModelV1Example, None, False, True)),
            (
                Optional[List[BaseModelV1Example]],
                False,
                TypeSpecifier(True, list, BaseModelV1Example, None, False, True),
            ),
            (List[Optional[BaseModelV1Example]], True, None),
            (List[BaseModelV2Example], False, TypeSpecifier(True, list, BaseModelV2Example, None, False, False)),
            (Optional[BaseModelV2Example], False, TypeSpecifier(True, None, BaseModelV2Example, None, False, True)),
            (
                Optional[List[BaseModelV2Example]],
                False,
                TypeSpecifier(True, list, BaseModelV2Example, None, False, True),
            ),
            (List[Optional[BaseModelV2Example]], True, None),
            (JSON, False, TypeSpecifier(True, None, None, None, True, False)),
            (str, False, TypeSpecifier(True, None, str, None, False, False)),
            (bytes, False, TypeSpecifier(True, None, bytes, None, False, False)),
            (
                Union[BaseModelV2Example, BaseModelV2Example2],
                False,
                TypeSpecifier(True, None, None, [BaseModelV2Example, BaseModelV2Example2], False, False),
            ),
            (
                Annotated[Union[BaseModelV2Example, BaseModelV2Example2], None],
                False,
                TypeSpecifier(True, None, None, [BaseModelV2Example, BaseModelV2Example2], False, False),
            ),
            (None, True, None),
        ]
    )
    def test_request_decorator_payload_spec(self, payload_type, raises, expected_payload_spec):
        # Arrange
        class TestAPI(APIEndpoints):
            def get_data(self, payload: payload_type) -> None:  # type: ignore [empty-body]
                ...

        decorator = request("POST", "/v1/data")
        # Act / Assert
        if raises:
            with self.assertRaises(APIEndpointError):
                decorator(TestAPI.get_data)
        else:
            decorator(TestAPI.get_data)
            assert decorator.payload_spec == expected_payload_spec

    def test_request_decorator_not_annotated_params(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, params) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_not_supprted_param_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, params: List[str]) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_not_annotated_url_field_arguments(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data/{id}")
                def get_data(self, id) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_bogus_params(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data/{id}")  # type: ignore [empty-body]
                def get_data(self, id: str, payload: BaseModelV1Example, bogus: str) -> None:
                    ...

    def test_request_decorator_accepts_optional_payload(self):
        # Arrange
        class TestAPIOptional(APIEndpoints):
            @request("GET", "/v1/data")
            def get_data1(self, payload: Optional[BaseModelV1Example]) -> None:  # type: ignore [empty-body]
                ...

        class TestAPIUnion(APIEndpoints):
            @request("GET", "/v2/data")
            def get_data2(self, payload: Union[None, BaseModelV1Example]) -> None:  # type: ignore [empty-body]
                ...

        class TestAPIOptionalModelSequence(APIEndpoints):
            @request("GET", "/v3/data")
            def get_data3(self, payload: Optional[List[BaseModelV1Example]]) -> None:  # type: ignore [empty-body]
                ...

    def test_request_decorator_call_from_unsuitable_base_class(self):
        class TestAPI:
            @request("GET", "/v1/data")
            def get_data(self) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI()
        with self.assertRaises(APIEndpointError):
            api.get_data()

    def test_request_decorator_call_with_positional_arguments(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/data/{id}")
            def get_data(self, id: str, payload: BaseModelV2Example) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data("ID123", self.basemodel_v1_payload)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v1/data/ID123",
            data=self.json_payload,
            headers={"content-type": "application/json"},
        )

    def test_request_decorator_call_with_mixed_positional_arguments(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self, payload: BaseModelV2Example, category: str, params: ParamsModelV1Example
            ) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data(self.basemodel_v1_payload, "clothes", self.basemodel_v1_params)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v2/clothes/items",
            data=self.json_payload,
            headers={"content-type": "application/json"},
            params=self.basemodel_v1_params,
        )

    def test_request_decorator_call_with_keyword_arguments(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self, payload: BaseModelV2Example, category: str, params: ParamsModelV1Example
            ) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data(category="clothes", params=self.basemodel_v1_params, payload=self.basemodel_v1_payload)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v2/clothes/items",
            data=self.json_payload,
            headers={"content-type": "application/json"},
            params=self.basemodel_v1_params,
        )

    def test_request_decorator_call_with_json_payload(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/aaa/bbb/ccc")
            def get_data(self, payload: JSON) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        json_payload = {"a": {"b": [1.6]}}
        # Act
        api.get_data(payload=json_payload)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/aaa/bbb/ccc",
            data=json.dumps(json_payload),
            headers={"content-type": "application/json"},
        )

    def test_request_decorator_call_optional_model_payload(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("PUT", "/v1/data/{id}")
            def put_data(self, id: str, payload: Optional[BaseModelV1Example]) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.put_data("ID123", None)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "PUT",
            self.base_path + "/v1/data/ID123",
        )

    def test_request_decorator_call_and_return_model(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> BaseModelV1Example:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.dataobj = MagicMock(return_value=self.basemodel_v1_payload)
        api = TestAPI(self.session_mock)
        # Act
        retval = api.get_data()
        # Assert
        self.session_mock.request.return_value.dataobj.assert_called_once()
        assert retval == self.basemodel_v1_payload

    def test_request_decorator_call_and_return_model_datasequece(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> DataSequence[BaseModelV1Example]:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.dataseq = MagicMock(return_value=self.basemodel_v1_sequence_payload)
        api = TestAPI(self.session_mock)
        # Act
        retval = api.get_data()
        # Assert
        self.session_mock.request.return_value.dataseq.assert_called_once()
        assert retval == self.basemodel_v1_sequence_payload

    def test_request_decorator_call_and_return_str(self):
        # Arrange
        expected = "This is String!"

        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> str:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.text = expected
        api = TestAPI(self.session_mock)
        # Act
        observed = api.get_data()
        # Assert
        assert observed == expected

    def test_request_decorator_call_and_return_bytes(self):
        # Arrange
        expected = b"\xFFThis is String!"

        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> bytes:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.content = expected
        api = TestAPI(self.session_mock)
        # Act
        observed = api.get_data()
        # Assert
        assert observed == expected

    def test_request_decorator_call_and_return_dict(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> dict:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.json = MagicMock(return_value=self.dict_payload)
        api = TestAPI(self.session_mock)
        # Act
        retval = api.get_data()
        # Assert
        self.session_mock.request.return_value.json.assert_called_once()
        assert retval == self.dict_payload

    @parameterized.expand(
        [
            ("JStr", str),
            (1, int),
            (3.33, float),
            (True, bool),
            ({"a": {"b": [1.6]}}, dict),
            ([1, 2, {"a": {"b": [1.6]}}], list),
        ]
    )
    def test_request_decorator_call_and_return_json(self, json, jtype):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> JSON:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.json = MagicMock(return_value=json)
        api = TestAPI(self.session_mock)
        # Act
        retval = api.get_data()
        # Assert
        self.session_mock.request.return_value.json.assert_called_once()
        assert retval == json
        assert isinstance(retval, jtype)

    def test_request_decorator_call_raises_when_payload_has_no_resp_json_key(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items", "data")
            def get_data(self) -> JSON:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.json = MagicMock(return_value=[1, 2, 3])
        api = TestAPI(self.session_mock)
        # Act / Assert
        with self.assertRaises(TypeError):
            api.get_data()

    def test_get_decorator(self):
        # Arrange
        class TestAPI(APIEndpoints):
            def method(self) -> None:  # type: ignore [empty-body]
                ...

        decorator = get("/url/data")
        # Act / Assert
        decorator(TestAPI.method)
        decorator.http_method = "GET"

    def test_put_decorator(self):
        # Arrange
        class TestAPI(APIEndpoints):
            def method(self) -> None:  # type: ignore [empty-body]
                ...

        decorator = put("/url/data")
        # Act / Assert
        decorator(TestAPI.method)
        decorator.http_method = "PUT"

    def test_post_decorator(self):
        # Arrange
        class TestAPI(APIEndpoints):
            def method(self) -> None:  # type: ignore [empty-body]
                ...

        decorator = post("/url/data")
        # Act / Assert
        decorator(TestAPI.method)
        decorator.http_method = "POST"

    def test_delete_decorator(self):
        # Arrange
        class TestAPI(APIEndpoints):
            def method(self) -> None:  # type: ignore [empty-body]
                ...

        decorator = delete("/url/data")
        # Act / Assert
        decorator(TestAPI.method)
        decorator.http_method = "DELETE"

    def test_no_mutable_state_when_calling_endpoint(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self, payload: BaseModelV1Example, category: str, params: ParamsModelV1Example
            ) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        for category in ["clothes", "food"]:
            for dict_payload in [
                {"id": "id1", "size": 100, "capacity": 1.7, "active": True},
                {"id": "id2", "size": 120, "capacity": 1.9, "active": False},
            ]:
                for params in [
                    ParamsModelV1Example(name="submarine", color="yellow"),
                    ParamsModelV1Example(name="oyster", color="blue"),
                ]:
                    # Act
                    payload = BaseModelV1Example.parse_obj(dict_payload)
                    api.get_data(category=category, params=params, payload=payload)
                    # Assert
                    self.session_mock.request.assert_called_once_with(
                        "GET",
                        self.base_path + f"/v2/{category}/items",
                        data=json.dumps(dict_payload),
                        headers={"content-type": "application/json"},
                        params=params,
                    )
                    self.session_mock.reset_mock()

    def test_request_decorator_call_with_defaults_arguments(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self,
                payload: BaseModelV1Example = self.basemodel_v1_payload,
                category: str = "default-category",
                params: ParamsModelV1Example = self.basemodel_v1_params,
            ) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data()
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v2/default-category/items",
            data=self.json_payload,
            headers={"content-type": "application/json"},
            params=self.basemodel_v1_params,
        )

    def test_request_decorator_call_with_defaults_arguments_override(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self,
                payload: BaseModelV1Example = self.basemodel_v1_payload,
                category: str = "default",
                params: ParamsModelV1Example = self.basemodel_v1_params,
            ) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        payload_override = BaseModelV1Example(id="override-id", size=500, capacity=9.0001, active=False)
        category_override = "override-category!"
        params_override = ParamsModelV1Example(name="override-Name", color="override with orange!")
        api.get_data(payload_override, category_override, params_override)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + f"/v2/{category_override}/items",
            data=payload_override.json(),
            headers={"content-type": "application/json"},
            params=params_override,
        )

    def test_decorator_chaining_order(self):
        # Expected @request can access original function signature (it will raise otherwise)
        class TestAPIMixedOrder1(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            @versions("<2")
            def get_data(
                self, payload: BaseModelV1Example, category: str, params: ParamsModelV1Example
            ) -> None:  # type: ignore [empty-body]
                ...

        class TestAPIMixedOrder2(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            @versions("<2")
            @view({ProviderView})
            def get_data(
                self, payload: BaseModelV1Example, category: str, params: ParamsModelV1Example
            ) -> None:  # type: ignore [empty-body]
                ...

    def test_request_decorator_format_url_with_str_enum(self):
        class FruitEnum(str, Enum):
            BANANA = "banana"
            ORANGE = "orange"
            APPLE = "apple"

        class TestAPI(APIEndpoints):
            @request("GET", "/v1/data/{fruit_type}")
            def get_data(self, fruit_type: FruitEnum, payload: str) -> None:  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data(FruitEnum.ORANGE, "not a fruit")
        # Assert
        self.session_mock.request.assert_called_once_with("GET", self.base_path + "/v1/data/orange", data="not a fruit")

    def test_request_decorator_raises_when_format_url_is_not_str_subtype(self):
        with self.assertRaises(APIEndpointError):

            class FruitEnum(Enum):
                BANANA = 1
                ORANGE = 2
                APPLE = 3

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data/{fruit_type}")
                def get_data(self, fruit_type: FruitEnum) -> None:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_accept_union_of_models(self):
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/data")
            def get_data(
                self, payload: Union[BaseModelV2Example, BaseModelV2Example2]
            ) -> None:  # type: ignore [empty-body]
                ...

    def test_request_decorator_accept_annotated_union_of_models(self):
        class BaseModelV2_A(BaseModelV2):
            field: Literal["number"] = "number"
            num: float

        class BaseModelV2_B(BaseModelV2):
            field: Literal["name"] = "name"
            name: str

        AnyBaseModel = Annotated[Union[BaseModelV2_A, BaseModelV2_B], FieldV2(discriminator="field")]

        class TestAPI(APIEndpoints):
            @request("POST", "/v1/data")
            def create(self, payload: AnyBaseModel) -> None:  # type: ignore [empty-body]
                ...
