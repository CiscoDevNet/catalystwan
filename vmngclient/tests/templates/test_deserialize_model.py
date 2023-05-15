import unittest
from unittest import TestCase, mock
from parameterized import parameterized

class TestFeatureTemplate(TestCase):

    @parameterized.expand([
        ("cedge_aaa")
    ])
    # Mock _get_feature_templates
    # Mock get
    def test_get(self, template_type):
        # Arrange

        # Open definition file
        # Open schema file
        # Pin return value of response to corresponding files

        # Act


        # Assert
        
        raise NotImplementedError()


if __name__ == "__main__":
    unittest.main()
