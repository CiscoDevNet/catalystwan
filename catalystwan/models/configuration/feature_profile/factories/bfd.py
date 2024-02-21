from catalystwan.models.configuration.feature_profile.factories.base import BaseFactory
from catalystwan.models.configuration.feature_profile.sdwan.system import BFD


class BFDFactory(BaseFactory):
    DELETE_PROPERTIES: tuple = tuple()

    def create_parcel(self):
        """
        Creates an BFD object based on the provided template values.

        Returns:
            BFD: An BFD object with the provided template values.
        """
        self.template_values["colors"] = self.template_values["color"]
        del self.template_values["color"]
        return BFD(**self.template_values)
