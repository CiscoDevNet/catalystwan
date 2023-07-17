import io
import json
import unittest
from typing import Dict, List
from unittest.mock import MagicMock

from attr import define  # type: ignore
from packaging.version import Version  # type: ignore
from parameterized import parameterized  # type: ignore
from pydantic import BaseModel

from vmngclient.dataclasses import DataclassBase  # type: ignore
from vmngclient.endpoints import BASE_PATH, APIEndpoints, CustomPayloadType, PreparedPayload
from vmngclient.endpoints import logger as endpoints_logger
from vmngclient.endpoints import request, versions, view
from vmngclient.exceptions import APIEndpointError, APIRequestPayloadTypeError, APIVersionError, APIViewError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.session_type import ProviderAsTenantView, ProviderView, TenantView


@define
class AttrsModelExample(DataclassBase):
    id: str
    size: int
    capacity: float
    active: bool


class BaseModelExample(BaseModel):
    id: str
    size: int
    capacity: float
    active: bool


class ParamsExample(BaseModel):
    name: str
    color: str


class CustomTypeExample(CustomPayloadType):
    buff = io.BytesIO(b"\xF1CustomDataFileContent\x01")

    def __init__(self):
        self.payload = PreparedPayload(
            data=b"\xFFCustomData\x00",
            headers={"content-type": "application/custom"},
            files={"file": ("custom-data.bin", self.buff)},
        )

    def prepared(self) -> PreparedPayload:
        return self.payload


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
        self.attrs_payload = create_dataclass(AttrsModelExample, self.dict_payload)
        self.basemodel_payload = BaseModelExample.parse_obj(self.dict_payload)
        self.custom_payload = CustomTypeExample()
        self.list_dict_payload = [self.dict_payload] * 2
        self.list_attrs_payload = [self.attrs_payload] * 2
        self.dict_params = {
            "name": "purple",
            "color": "haze",
        }
        self.basemodel_params = ParamsExample.parse_obj(self.dict_params)
        self.attrs_sequence_payload = DataSequence(AttrsModelExample, self.list_attrs_payload)
        self.basemodel_sequence_payload = [self.basemodel_payload] * 2

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

    def test_attrs_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.attrs_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.dict_payload

    def test_basemodel_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.basemodel_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.dict_payload

    def test_attrs_sequence_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.attrs_sequence_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.list_dict_payload

    def test_basemodel_sequence_payload(self):
        self.endpoints._request("GET", f"/{__name__}", payload=self.basemodel_sequence_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.list_dict_payload

    def test_custom_payload(self):
        self.endpoints._request("POST", f"/{__name__}", payload=self.custom_payload)
        _, kwargs = self.session_mock.request.call_args
        prepared = self.custom_payload.prepared()
        assert kwargs.get("data") == prepared.data
        assert kwargs.get("headers") == prepared.headers
        assert kwargs.get("files")["file"][0] == prepared.files["file"][0]
        assert kwargs.get("files")["file"][1].read() == prepared.files["file"][1].read()

    def test_dict_payload(self):
        self.endpoints._request("POST", f"/{__name__}", payload=self.dict_payload)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("data") == self.json_payload

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

    def test_basemodel_params(self):
        self.endpoints._request("POST", f"/{__name__}", params=self.basemodel_params)
        _, kwargs = self.session_mock.request.call_args
        assert kwargs.get("params") == self.dict_params

    def test_request_decorator_forbidden_url_field_name(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("GET", "/v1/data/{payload}")
                def get_data(self, payload: str):  # type: ignore [empty-body]
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
                def get_data(self) -> List[BaseModelExample]:  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_payload_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, payload: DataSequence):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_payload_sequence_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, payload: List[str]):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_unsupported_payload_composite_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, payload: Dict[str, BaseModelExample]):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_not_annotated_params(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, params):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_not_supprted_param_type(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data")
                def get_data(self, params: List[str]):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_not_annotated_url_field_arguments(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data/{id}")
                def get_data(self, id):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_bogus_params(self):
        with self.assertRaises(APIEndpointError):

            class TestAPI(APIEndpoints):
                @request("POST", "/v1/data/{id}")
                def get_data(self, id: str, payload: BaseModelExample, bogus: str):  # type: ignore [empty-body]
                    ...

    def test_request_decorator_call_from_unsuitable_base_class(self):
        class TestAPI:
            @request("GET", "/v1/data")
            def get_data(self):  # type: ignore [empty-body]
                ...

        api = TestAPI()
        with self.assertRaises(APIEndpointError):
            api.get_data()

    def test_request_decorator_call_with_positional_arguments(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/data/{id}")
            def get_data(self, id: str, payload: BaseModelExample):  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data("ID123", self.basemodel_payload)
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
                self, payload: BaseModelExample, category: str, params: ParamsExample
            ):  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data(self.basemodel_payload, "clothes", self.basemodel_params)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v2/clothes/items",
            data=self.json_payload,
            headers={"content-type": "application/json"},
            params=self.basemodel_params,
        )

    def test_request_decorator_call_with_keyword_arguments(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self, payload: BaseModelExample, category: str, params: ParamsExample
            ):  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        # Act
        api.get_data(category="clothes", params=self.basemodel_params, payload=self.basemodel_payload)
        # Assert
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v2/clothes/items",
            data=self.json_payload,
            headers={"content-type": "application/json"},
            params=self.basemodel_params,
        )

    def test_request_decorator_call_and_return_model(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> BaseModelExample:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.dataobj = MagicMock(return_value=self.basemodel_payload)
        api = TestAPI(self.session_mock)
        # Act
        retval = api.get_data()
        # Assert
        self.session_mock.request.return_value.dataobj.assert_called_once()
        assert retval == self.basemodel_payload

    def test_request_decorator_call_and_return_model_datasequece(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v1/items")
            def get_data(self) -> DataSequence[BaseModelExample]:  # type: ignore [empty-body]
                ...

        self.session_mock.request.return_value.dataseq = MagicMock(return_value=self.basemodel_sequence_payload)
        api = TestAPI(self.session_mock)
        # Act
        retval = api.get_data()
        # Assert
        self.session_mock.request.return_value.dataseq.assert_called_once()
        assert retval == self.basemodel_sequence_payload

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

    def test_no_mutable_state_when_calling_endpoint(self):
        # Arrange
        class TestAPI(APIEndpoints):
            @request("GET", "/v2/{category}/items")
            def get_data(
                self, payload: BaseModelExample, category: str, params: ParamsExample
            ):  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        for category in ["clothes", "food"]:
            for dict_payload in [
                {"id": "id1", "size": 100, "capacity": 1.7, "active": True},
                {"id": "id2", "size": 120, "capacity": 1.9, "active": False},
            ]:
                for params in [
                    ParamsExample(name="submarine", color="yellow"),
                    ParamsExample(name="oyster", color="blue"),
                ]:
                    # Act
                    payload = BaseModelExample.parse_obj(dict_payload)
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
