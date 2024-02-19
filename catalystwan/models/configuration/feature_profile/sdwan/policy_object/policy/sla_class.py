from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global

SLAClassCriteria = Literal[
    "loss",
    "latency",
    "jitter",
    "loss-latency",
    "loss-jitter",
    "latency-loss",
    "latency-jitter",
    "jitter-latency",
    "jitter-loss",
    "loss-latency-jitter",
    "loss-jitter-latency",
    "latency-loss-jitter",
    "latency-jitter-loss",
    "jitter-latency-loss",
    "jitter-loss-latency",
]


class SLAAppProbeClass(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ref_id: Global[UUID] = Field(serialization_alias="refId", validation_alias="refId")


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: Global[SLAClassCriteria]
    jitter_variance: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="jitterVariance",
        validation_alias="jitterVariance",
        description="jitter variance in ms",
    )
    latency_variance: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="latencyVariance",
        validation_alias="latencyVariance",
        description="latency variance in ms",
    )
    loss_variance: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="lossVariance",
        validation_alias="lossVariance",
        description="loss variance as percentage",
    )

    def add_criterias(
        self, jitter_variance: Union[int, None], latency_variance: Union[int, None], loss_variance: Union[int, None]
    ):
        expected_criterias = []
        if jitter_variance:
            self.jitter_variance = Global(value=jitter_variance)
            expected_criterias.append("jitter")
        if latency_variance:
            self.latency_variance = Global(value=latency_variance)
            expected_criterias.append("latency")
        if loss_variance:
            self.loss_variance = Global(value=loss_variance)
            expected_criterias.append("loss")
        for e in expected_criterias:
            if e not in self.criteria.value:
                raise ValueError(f"Criteria {e} is not in configured criteraias {self.criteria.value}")

    @field_validator("latency_variance")
    @classmethod
    def check_latency(cls, latency: Global):
        assert 1 <= latency.value <= 1000
        return latency

    @field_validator("loss_variance")
    @classmethod
    def check_loss(cls, loss: Global):
        assert 0 <= loss.value <= 100
        return loss

    @field_validator("jitter_variance")
    @classmethod
    def check_jitter(cls, jitter: Global):
        assert 1 <= jitter.value <= 1000
        return jitter


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[Global[int]] = None
    loss: Optional[Global[int]] = None
    jitter: Optional[Global[int]] = None
    app_probe_class: Optional[SLAAppProbeClass] = Field(
        validation_alias="appProbeClass", serialization_alias="appProbeClass"
    )
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(
        default=None, validation_alias="fallbackBestTunnel", serialization_alias="fallbackBestTunnel"
    )

    @field_validator("latency")
    @classmethod
    def check_latency(cls, latency: Global):
        assert 1 <= latency.value <= 1000
        return latency

    @field_validator("loss")
    @classmethod
    def check_loss(cls, loss: Global):
        assert 0 <= loss.value <= 100
        return loss

    @field_validator("jitter")
    @classmethod
    def check_jitter(cls, jitter: Global):
        assert 1 <= jitter.value <= 1000
        return jitter


class SLAClassParcel(_ParcelBase):
    entries: List[SLAClassListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_entry(self, app_probe_class_id: UUID, loss: Optional[int], jitter: Optional[int], latency: Optional[int]):
        self.entries.append(
            SLAClassListEntry(
                app_probe_class=SLAAppProbeClass(ref_id=as_global(app_probe_class_id)),
                loss=as_global(loss),
                jitter=as_global(jitter),
                latency=as_global(latency),
            )
        )

    def add_fallback(
        self,
        criteria: SLAClassCriteria,
        jitter_variance: Optional[int],
        latency_variance: Optional[int],
        loss_variance: Optional[int],
    ):
        fallback = FallbackBestTunnel(
            criteria=as_global(criteria),
            jitter_variance=as_global(jitter_variance),
            latency_variance=as_global(latency_variance),
            loss_variance=as_global(loss_variance),
        )
        self.entries[0].fallback_best_tunnel = fallback
