# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Any, Optional, Union

from pydantic import BaseModel
from requests import HTTPError, RequestException


class ManagerErrorInfo(BaseModel):
    message: Union[str, None]
    details: Union[str, None]
    code: Union[str, None]


class CatalystwanException(Exception):
    """Superclass of all catalystwan SDK exception types."""


class ManagerRequestException(RequestException, CatalystwanException):
    """Exception raised when there is ambigous problem during sending of request to Manager"""

    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects."""
        super().__init__(*args, **kwargs)


class ManagerHTTPError(HTTPError, ManagerRequestException):
    def __init__(self, *, error_info: Optional[ManagerErrorInfo], request: Any, response: Any):
        """Initialize RequestException with `error_info`, `request` and `response` objects."""
        self.info = error_info
        super().__init__(request=request, response=response)


class DefaultPasswordError(CatalystwanException):
    """Default password for SDWAN Manager user was detected and needs to be changed."""

    pass


class InvalidOperationError(CatalystwanException):
    """The exception that is thrown when a method call is invalid for the object's current state."""

    pass


class RetrieveIntervalOutOfRange(CatalystwanException):
    pass


class VersionDeclarationError(CatalystwanException):
    """

    The exception that is thrown in one of two below cases.
    1. User passes software image and version, at the same time.
    2. User doesn't passes any of them.
    """

    pass


class ImageNotInRepositoryError(CatalystwanException):
    """The exception that is thrown, if image is not in vManage images Repository"""

    pass


class EmptyVersionPayloadError(CatalystwanException):
    """Used when a version is not found in device available or current versions."""

    pass


class TemplateNotFoundError(CatalystwanException):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class AttachedError(CatalystwanException):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateTypeError(CatalystwanException):
    """Used when wrong type template."""

    def __init__(self, name):
        self.message = f"Template: {name} - wrong template type."


class AlreadyExistsError(CatalystwanException):
    """Raised when an entity that we attempted to create already exists."""

    pass


class APIVersionError(CatalystwanException):
    """Raised when API is unsupported in running vManage version."""

    def __init__(self, item, supported, current):
        self.message = f"vManage is running: {current} but {item} only supported in API version: {supported}"


class APIViewError(CatalystwanException):
    """Raised when API is not allowed for given session type / view."""

    def __init__(self, item, allowed, current):
        self.message = f"Current view is: {current} but {item} only allowed for views: {allowed}"


class APIRequestPayloadTypeError(CatalystwanException):
    """Raised when unsupported payload type is passed to vManage request."""

    def __init__(self, item):
        self.message = f"Unsupported payload type: {type(item)} for vManage request"


class EmptyTaskResponseError(CatalystwanException):
    """Raised if task is registred by vManage, but reponse content is empty"""

    pass


class TaskNotRegisteredError(CatalystwanException):
    """Raised if task_id is generated, but it's not registere in vManage"""

    pass


class TaskValidationError(CatalystwanException):
    """Raised if task has not been validated"""

    pass


class MultiplePersonalityError(CatalystwanException):
    """Raised if Device DataSequnce contains devices with multiples personalities"""


class SessionNotCreatedError(CatalystwanException):
    """Raised when vManage session cannot be created"""

    pass


class TenantSubdomainNotFound(CatalystwanException):
    """Raised when given subdomain does not exist"""

    pass


class APIEndpointError(CatalystwanException):
    """Raised when there is a problem with endpoint definition"""

    pass


class TenantMigrationExportFileNotFound(CatalystwanException):
    """Raised when client cannot find exported file name in export task result"""

    pass


class TenantMigrationPreconditionsError(CatalystwanException):
    """Raised when preconditions for tenant migration fail"""

    pass


class ManagerReadyTimeout(CatalystwanException):
    """Raised when waiting for server ready flag took longer than expected"""

    pass


class CatalystwanDeprecationWarning(DeprecationWarning):
    """Warning issued when using deprecated features or functionality in the Catalystwan SDK.

    This warning indicates that the current usage of certain features or functionality within the Catalystwan SDK
    is deprecated and may be removed in future versions. It serves as a notice to developers to update their code
    to use the recommended alternatives.
    """

    message: str

    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        message = (
            f"{self.message}. Deprecated in catalystwan (0.y.z), will be removed in (1.y.z)."
            f" Major version zero (0.y.z) is for initial development. Anything MAY change at any time."
            f" The public API SHOULD NOT be considered stable."
        )
        return message
