from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class CriteriaEnum(str, Enum):
    LOSS = "loss"
    LATENCY = "latency"
    JITTER = "jitter"
    LOSS_LATENCY = "loss-latency"
    LOSS_JITTER = "loss-jitter"
    LATENCY_LOSS = "latency-loss"
    LATENCY_JITTER = "latency-jitter"
    JITTER_LATENCY = "jitter-latency"
    JITTER_LOSS = "jitter-loss"
    LOSS_LATENCY_JITTER = "loss-latency-jitter"
    LOSS_JITTER_LATENCY = "loss-jitter-latency"
    LATENCY_LOSS_JITTER = "latency-loss-jitter"
    LATENCY_JITTER_LOSS = "latency-jitter-loss"
    JITTER_LATENCY_LOSS = "jitter-latency-loss"
    JITTER_LOSS_LATENCY = "jitter-loss-latency"


class Criteria(Global):
    value: CriteriaEnum


class Latency(Global):
    value: int = Field(ge=1, le=1000)


class Loss(Global):
    value: int = Field(ge=0, le=100)


class Jitter(Global):
    value: int = Field(ge=1, le=1000)


class LatencyVariance(Latency):
    ...


class LossVariance(Loss):
    ...


class JitterVariance(Jitter):
    ...


class AppProbeClassRefId(Global):
    value: UUID


class AppProbeClass(BaseModel):
    ref_id: AppProbeClassRefId = Field(alias="refId")


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: Criteria
    jitter_variance: Optional[JitterVariance] = Field(
        default=None,
        alias="jitterVariance",
        description="jitter variance in ms",
    )
    latency_variance: Optional[LatencyVariance] = Field(
        default=None,
        alias="latencyVariance",
        description="latency variance in ms",
    )
    loss_variance: Optional[LossVariance] = Field(
        default=None,
        alias="lossVariance",
        description="loss variance as percentage",
    )

    def add_criterias(
        self, jitter_variance: Union[int, None], latency_variance: Union[int, None], loss_variance: Union[int, None]
    ):
        expected_criterias = []
        if jitter_variance:
            self.jitter_variance = JitterVariance(value=jitter_variance)
            expected_criterias.append("jitter")
        if latency_variance:
            self.latency_variance = LatencyVariance(value=latency_variance)
            expected_criterias.append("latency")
        if loss_variance:
            self.loss_variance = LossVariance(value=loss_variance)
            expected_criterias.append("loss")
        for e in expected_criterias:
            if e not in self.criteria.value:
                raise ValueError(f"Criteria {e} is not in configured criteraias {self.criteria.value}")


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[Latency] = None
    loss: Optional[Loss] = None
    jitter: Optional[Jitter] = None
    app_probe_class: Optional[AppProbeClass] = Field(alias="appProbeClass")
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(default=None, alias="fallbackBestTunnel")


class SLAClassData(BaseModel):
    entries: List[SLAClassListEntry]


class SLAClassPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.SLA_CLASS)
    data: SLAClassData
