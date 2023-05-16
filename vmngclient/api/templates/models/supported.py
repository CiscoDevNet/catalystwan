from enum import Enum

from vmngclient.dataclasses import AlarmData

from .cisco_aaa_model import CiscoAAAModel


class FeatureTemplateType(Enum):
    cisco_aaa: str = "cedge_aaa"


supported_models = [CiscoAAAModel, AlarmData]  # AlarmData provided just for mypy (>1 class needed, only 1 model)
