from enum import Enum


class OperationStatus(Enum):
    IN_PROGRESS = "In progress"
    FAILURE = "Failure"
    SUCCESS = "Success"
    SCHEDULED = "Scheduled"
