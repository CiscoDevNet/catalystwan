from enum import Enum


class OperationStatus(Enum):
    IN_PROGRESS = "In progress"
    FAILURE = "Failure"
    SUCCESS = "Success"
    SCHEDULED = "Scheduled"
    DONE_SCHEDULED = "Done - Scheduled"
    VALIDATION_SUCCESS = "Validation success"


class OperationStatusId(Enum):
    IN_PROGRESS = "in_progress"
    FAILURE = "failure"
    SUCCESS = "success"
    SCHEDULED = "scheduled"
    DONE_SCHEDULED = "done_scheduled"
    VALIDATION_SUCCESS = "validation_success"
