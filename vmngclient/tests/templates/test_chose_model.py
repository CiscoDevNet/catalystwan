import unittest

from parameterized import parameterized  # type: ignore

from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel
from vmngclient.api.templates.models.omp_vsmart_model import OMPvSmart
from vmngclient.api.templates.models.security_vsmart_model import SecurityvSmart
from vmngclient.api.templates.models.system_vsmart_model import SystemVsmart
from vmngclient.utils.feature_template import choose_model


class TestChooseModel(unittest.TestCase):
    @parameterized.expand(
        [
            ("cedge_aaa", CiscoAAAModel),
            ("omp-vsmart", OMPvSmart),
            ("security-vsmart", SecurityvSmart),
            ("system-vsmart", SystemVsmart),
        ]
    )
    def test_choose_model(self, model_type, model_cls):
        # Arrange
        name = "My model name"
        description = "My model description"
        model_from_cls = model_cls(name=name, description=description)

        # Act
        chosen_model = choose_model(model_type)
        model_from_choice = chosen_model(name=name, description=description)

        # Assert
        self.assertEqual(model_from_choice, model_from_cls)
