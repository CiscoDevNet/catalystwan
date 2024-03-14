# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.models.common import check_fields_exclusive
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class LocalAppListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    app_family: Optional[str] = Field(default=None, serialization_alias="appFamily", validation_alias="appFamily")
    app: Optional[str] = None

    @model_validator(mode="after")
    def check_app_xor_appfamily(self):
        check_fields_exclusive(self.__dict__, {"app", "app_family"}, True)
        return self


class LocalAppList(PolicyListBase):
    type: Literal["localApp"] = "localApp"
    entries: List[LocalAppListEntry] = []


class LocalAppListEditPayload(LocalAppList, PolicyListId):
    pass


class LocalAppListInfo(LocalAppList, PolicyListInfo):
    pass
