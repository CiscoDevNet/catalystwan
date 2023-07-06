import json
import unittest
from unittest.mock import MagicMock, patch

from attr import define  # type: ignore
from packaging.version import Version  # type: ignore
from parameterized import parameterized  # type: ignore
from pydantic import BaseModel

from vmngclient.dataclasses import DataclassBase  # type: ignore
from vmngclient.exceptions import APIRequestPayloadTypeError, APIVersionError, APIViewError
from vmngclient.primitives import BASE_PATH, APIPrimitiveBase
from vmngclient.primitives import logger as primitives_logger
from vmngclient.primitives import request, versions, view
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


class BaseModelExample2(BaseModel):
    example: BaseModelExample
    size: int


class TestAPIPrimitives(unittest.TestCase):
    @patch("vmngclient.session.vManageSession")
    def setUp(self, session_mock):
        self.base_path = BASE_PATH
        self.session_mock = session_mock
        self.session_mock.request = MagicMock()
        self.session_mock.api_version = None
        self.session_mock.session_type = None
        self.primitive = APIPrimitiveBase(self.session_mock)
        self.dict_payload = {
            "id": "XYZ-189",
            "size": 100,
            "capacity": 1.7,
            "active": True,
        }
        self.json_payload = json.dumps(self.dict_payload)
        self.attrs_payload = create_dataclass(AttrsModelExample, self.dict_payload)
        self.basemodel_payload = BaseModelExample.parse_obj(self.dict_payload)
        self.list_dict_payload = [self.dict_payload] * 2
        self.list_attrs_payload = [self.attrs_payload] * 2
        self.datasequence_payload = DataSequence(AttrsModelExample, self.list_attrs_payload)

    def test_get(self):
        self.primitive._get("/get_endpoint/1")
        self.session_mock.request.assert_called_once_with("GET", "/dataservice/get_endpoint/1")

    def test_post(self):
        self.primitive._post("/post_endpoint/2")
        self.session_mock.request.assert_called_once_with("POST", "/dataservice/post_endpoint/2")

    def test_put(self):
        self.primitive._put("/put_endpoint/3")
        self.session_mock.request.assert_called_once_with("PUT", "/dataservice/put_endpoint/3")

    def test_delete(self):
        self.primitive._delete("/delete_endpoint/4")
        self.session_mock.request.assert_called_once_with("DELETE", "/dataservice/delete_endpoint/4")

    @parameterized.expand(
        [
            ("<2.0", "1.9.9"),
            (">=1.9, !=3.0", "3.1"),
            (">0.9, <=1.3", "1.3"),
        ]
    )
    def test_versions_decorator_passes(self, supported_versions, current_version):
        class ExampleAPI(APIPrimitiveBase):
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
        class ExampleAPI(APIPrimitiveBase):
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

        class ExampleAPI(APIPrimitiveBase):
            @versions(supported_versions=supported_versions, raises=False)
            def versions_decorated_method(self):
                pass

        self.session_mock.api_version = Version(current_version)
        api = ExampleAPI(self.session_mock)
        with self.assertLogs(primitives_logger, level="WARNING") as log:
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
        class ExampleAPI(APIPrimitiveBase):
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
        class ExampleAPI(APIPrimitiveBase):
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

        class ExampleAPI(APIPrimitiveBase):
            @view(allowed_session_types=allowed_sessions)
            def versions_decorated_method(self):
                pass

        self.session_mock.session_type = current_session
        api = ExampleAPI(self.session_mock)
        with self.assertLogs(primitives_logger, level="WARNING") as log:
            api.versions_decorated_method()
            for allowed in allowed_sessions:
                assert str(allowed) in log.output[0]
            assert str(current_session) in log.output[0]

    def test_attrs_payload(self):
        self.primitive._get("/1", payload=self.attrs_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.dict_payload

    def test_basemodel_payload(self):
        self.primitive._get("/2", payload=self.basemodel_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.dict_payload

    def test_datasequence_payload(self):
        self.primitive._get("/3", payload=self.datasequence_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.list_dict_payload

    def test_list_payload(self):
        self.primitive._get("/4", payload=self.list_attrs_payload)
        _, kwargs = self.session_mock.request.call_args
        assert json.loads(kwargs.get("data")) == self.list_dict_payload

    def test_unexpected_payload(self):
        with self.assertRaises(APIRequestPayloadTypeError):
            self.primitive._get("/5", payload={1, 2, 3})

    def test_request_decorator_positional_arguments(self):
        class TestAPI(APIPrimitiveBase):
            @request("GET", "/v1/data/{id}")
            def get_data(self, id: str, payload: BaseModelExample):  # type: ignore [empty-body]
                ...

        api = TestAPI(self.session_mock)
        api.get_data("ID123", self.basemodel_payload)
        self.session_mock.request.assert_called_once_with(
            "GET",
            self.base_path + "/v1/data/ID123",
            data=self.json_payload,
            headers={"content-type": "application/json"},
        )
