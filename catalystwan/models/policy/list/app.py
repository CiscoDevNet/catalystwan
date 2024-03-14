from typing import List, Literal

from catalystwan.models.policy.lists_entries import AppListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class AppList(PolicyListBase):
    type: Literal["app"] = "app"
    entries: List[AppListEntry] = []

    def add_app(self, app: str) -> None:
        self._add_entry(AppListEntry(app=app))

    def add_app_family(self, app_family: str) -> None:
        self._add_entry(AppListEntry(app_family=app_family))


class AppListEditPayload(AppList, PolicyListId):
    pass


class AppListInfo(AppList, PolicyListInfo):
    pass
