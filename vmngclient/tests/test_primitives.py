import unittest
from unittest.mock import MagicMock, patch

from packaging.version import Version  # type: ignore
from parameterized import parameterized  # type: ignore

from vmngclient.exceptions import APIVersionError
from vmngclient.primitives import APIPrimitiveBase, Versions
from vmngclient.primitives import logger as primitives_logger


class TestAPIPrimitives(unittest.TestCase):
    @patch("vmngclient.session.vManageSession")
    def setUp(self, session_mock) -> None:
        self.session_mock = session_mock
        self.session_mock.request = MagicMock()
        self.session_mock.api_version = None
        self.primitive = APIPrimitiveBase(self.session_mock)

    def test_get(self):
        self.primitive.get("/get_endpoint/1")
        self.session_mock.request.assert_called_once_with("GET", "/dataservice/get_endpoint/1")

    def test_post(self):
        self.primitive.post("/post_endpoint/2")
        self.session_mock.request.assert_called_once_with("POST", "/dataservice/post_endpoint/2")

    def test_put(self):
        self.primitive.put("/put_endpoint/3")
        self.session_mock.request.assert_called_once_with("PUT", "/dataservice/put_endpoint/3")

    def test_delete(self):
        self.primitive.delete("/delete_endpoint/4")
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
            @Versions(versions=supported_versions, raises=True)
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
            @Versions(versions=supported_versions, raises=True)
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
            @Versions(versions=supported_versions, raises=False)
            def versions_decorated_method(self):
                pass

        self.session_mock.api_version = Version(current_version)
        api = ExampleAPI(self.session_mock)
        with self.assertLogs(primitives_logger, level="WARNING") as log:
            api.versions_decorated_method()
            assert supported_versions in log.output[0]
            assert current_version in log.output[0]
