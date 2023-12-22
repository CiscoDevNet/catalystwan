from typing import Optional

from pydantic import BaseModel


class GetServiceFeatureProfilesQuery(BaseModel):
    limit: Optional[int]
    offset: Optional[int]
    details: Optional[bool]


class GetServiceFeatureProfileQuery(BaseModel):
    details: Optional[bool]
