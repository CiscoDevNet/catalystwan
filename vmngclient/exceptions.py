class vManageClientError(Exception):
    """Superclass of all vmngclient exception types."""


class InvalidOperationError(vManageClientError):
    """The exception that is thrown when a method call is invalid for the object's current state."""

    pass


class RetrieveIntervalOutOfRange(vManageClientError):
    pass


class VersionDeclarationError(vManageClientError):
    """

    The exception that is thrown in one of two below cases.
    1. User passes software image and version, at the same time.
    2. User doesn't passes any of them.
    """

    pass


class ImageNotInRepositoryError(vManageClientError):
    """The exception that is thrown, if image is not in vManage images Repository"""

    pass


class TemplateNotFoundError(vManageClientError):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class AttachedError(vManageClientError):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateTypeError(vManageClientError):
    """Used when wrong type template."""

    def __init__(self, name):
        self.message = f"Template: {name} - wrong template type."


class AlreadyExistsError(vManageClientError):
    """Raised when an entity that we attempted to create already exists."""

    pass


class APIVersionError(vManageClientError):
    """Raised when API is unsupported in running vManage version."""

    def __init__(self, item, supported, current):
        self.message = f"vManage is running: {current} but {item} only supported in API version: {supported}"


class APIViewError(vManageClientError):
    """Raised when API is not allowed for given session type / view."""

    def __init__(self, item, allowed, current):
        self.message = f"Current view is: {current} but {item} only allowed for views: {allowed}"


class APIRequestPayloadTypeError(vManageClientError):
    """Raised when unsupported payload type is passed to vManage request."""

    def __init__(self, item):
        self.message = f"Unsupported payload type: {type(item)} for vManage request"


class EmptyTaskResponseError(vManageClientError):
    """Raised if task is registred by vManage, but reponse content is empty"""

    pass


class TaskNotRegisteredError(vManageClientError):
    """Raised if task_id is generated, but it's not registere in vManage"""

    pass


class TaskValidationError(vManageClientError):
    """Raised if task has not been validated"""

    pass


class MultiplePersonalityError(vManageClientError):
    """Raised if Device DataSequnce contains devices with multiples personalities"""


class SessionNotCreatedError(vManageClientError):
    """Raised when vManage session cannot be created"""

    pass


class TenantSubdomainNotFound(vManageClientError):
    """Raised when given subdomain does not exist"""

    pass


class APIEndpointError(vManageClientError):
    """Raised when there is a problem with endpoint definition"""

    pass


class TenantMigrationExportFileNotFound(vManageClientError):
    """Raised when client cannot find exported file name in export task result"""

    pass


class TenantMigrationPreconditionsError(vManageClientError):
    """Raised when preconditions for tenant migration fail"""

    pass
