# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest

from parameterized import parameterized  # type: ignore

from catalystwan.api.templates.models.cisco_aaa_model import CiscoAAAModel
from catalystwan.api.templates.models.cisco_system import CiscoSystemModel
from catalystwan.api.templates.models.omp_vsmart_model import OMPvSmart
from catalystwan.api.templates.models.security_vsmart_model import SecurityvSmart
from catalystwan.api.templates.models.system_vsmart_model import SystemVsmart
from catalystwan.utils.feature_template.choose_model import choose_model


class TestChooseModel(unittest.TestCase):
    @parameterized.expand(
        [
            ("cedge_aaa", CiscoAAAModel),
            ("omp-vsmart", OMPvSmart),
            ("security-vsmart", SecurityvSmart),
            ("system-vsmart", SystemVsmart),
            ("cisco_system", CiscoSystemModel),
        ]
    )
    def test_choose_model(self, model_type, model_cls):
        # Arrange
        name = "My model name"
        description = "My model description"
        model_from_cls = model_cls(template_name=name, template_description=description)

        # Act
        chosen_model = choose_model(model_type)
        model_from_choice = chosen_model(template_name=name, template_description=description)

        # Assert
        self.assertEqual(model_from_choice, model_from_cls)
