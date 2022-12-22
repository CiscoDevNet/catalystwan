from enum import Enum


    IN_PROGRESS = "In progress"
    FAILURE = "Failure"
    SUCCESS = "Success"
    SCHEDULED = "Scheduled"


class OperationStatusId(Enum):
    IN_PROGRESS = "in progress"
    FAILURE = "failure"
    SUCCESS = "success"
    SCHEDULED = "scheduled"
