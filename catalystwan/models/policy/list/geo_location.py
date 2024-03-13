from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import GeoLocationListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class GeoLocationList(PolicyListBase):
    type: Literal["geoLocation"] = "geoLocation"
    entries: List[GeoLocationListEntry] = []


class GeoLocationListEditPayload(GeoLocationList, PolicyListId):
    pass


class GeoLocationListInfo(GeoLocationList, PolicyListInfo):
    pass
