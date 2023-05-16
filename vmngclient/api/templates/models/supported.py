from enum import Enum

from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel
from vmngclient.dataclasses import AlarmData


class FeatureTemplateType(Enum):
    cisco_aaa: str = "cedge_aaa"


supported_models = [CiscoAAAModel, AlarmData]  # AlarmData provided just for mypy (>1 class needed, only 1 model)
