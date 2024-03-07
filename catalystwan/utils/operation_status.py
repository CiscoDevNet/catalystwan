# Copyright 2022 Cisco Systems, Inc. and its affiliates

from enum import Enum


class OperationStatus(Enum):
    IN_PROGRESS = "In progress"
    FAILURE = "Failure"
    SUCCESS = "Success"
    SCHEDULED = "Scheduled"
    SUCCESS_SCHEDULED = "Done - Scheduled"
    VALIDATION_SUCCESS = "Validation success"
    VALIDATION_FAILURE = "Validation failure"


class OperationStatusId(Enum):
    IN_PROGRESS = "in_progress"
    FAILURE = "failure"
    SUCCESS = "success"
    SCHEDULED = "scheduled"
    SUCCESS_SCHEDULED = "success_scheduled"
    VALIDATION_SUCCESS = "validation_success"
