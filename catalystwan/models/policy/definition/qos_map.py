# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)

QoSScheduling = Literal[
    "llq",
    "wrr",
]

QoSDropType = Literal[
    "tail-drop",
    "red-drop",
]


class QoSScheduler(BaseModel):
    queue: IntStr = Field(ge=0, le=8)
    class_map_ref: Optional[UUID] = Field(
        default=None, serialization_alias="classMapRef", validation_alias="classMapRef"
    )
    bandwidth_percent: IntStr = Field(
        default=1, ge=1, le=100, serialization_alias="bandwidthPercent", validation_alias="bandwidthPercent"
    )
    buffer_percent: IntStr = Field(
        default=1, ge=1, le=100, serialization_alias="bufferPercent", validation_alias="bufferPercent"
    )
    burst: Optional[IntStr] = Field(default=None, ge=5000, le=10_000_000)
    scheduling: QoSScheduling = "wrr"
    drops: QoSDropType = "tail-drop"
    temp_key_values: Optional[str] = Field(
        default=None, serialization_alias="tempKeyValues", validation_alias="tempKeyValues"
    )

    @staticmethod
    def get_default_control_scheduler() -> "QoSScheduler":
        return QoSScheduler(
            queue=0,
            bandwidth_percent=100,
            buffer_percent=100,
            burst=15000,
            scheduling="llq",
            drops="tail-drop",
        )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("class_map_ref", mode="before")
    @classmethod
    def check_optional_class_map_ref(cls, class_map_ref: Union[str, None]):
        # None and "" indicates missing value, both can be found in server responses
        if not class_map_ref:
            return None
        return class_map_ref


class QoSMapDefinition(BaseModel):
    qos_schedulers: List[QoSScheduler] = Field(serialization_alias="qosSchedulers", validation_alias="qosSchedulers")
    model_config = ConfigDict(populate_by_name=True)


class QoSMapPolicy(PolicyDefinitionBase):
    type: Literal["qosMap"] = "qosMap"
    definition: QoSMapDefinition = QoSMapDefinition(qos_schedulers=[])
    model_config = ConfigDict(populate_by_name=True)

    def add_scheduler(
        self,
        queue: int,
        class_map_ref: UUID,
        bandwidth: int = 1,
        buffer: int = 1,
        scheduling: QoSScheduling = "wrr",
        drops: QoSDropType = "tail-drop",
        burst: Optional[int] = None,
    ) -> None:
        self.definition.qos_schedulers.append(
            QoSScheduler(
                queue=queue,
                class_map_ref=class_map_ref,
                bandwidth_percent=bandwidth,
                buffer_percent=buffer,
                burst=burst,
                scheduling=scheduling,
                drops=drops,
            )
        )

    @model_validator(mode="after")
    def generate_default_control_scheduler(self):
        if not self.definition.qos_schedulers:
            # Only when creating (not when value obtained from remote is present)
            self.definition = QoSMapDefinition(qos_schedulers=[QoSScheduler.get_default_control_scheduler()])
        return self


class QoSMapPolicyEditPayload(QoSMapPolicy, PolicyDefinitionId):
    pass


class QoSMapPolicyGetResponse(QoSMapPolicy, PolicyDefinitionGetResponse):
    pass
