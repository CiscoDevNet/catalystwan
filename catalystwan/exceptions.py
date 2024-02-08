class ManagerError(Exception):
    """Superclass of all catalystwan exception types."""


class InvalidOperationError(ManagerError):
    """The exception that is thrown when a method call is invalid for the object's current state."""

    pass


class RetrieveIntervalOutOfRange(ManagerError):
    pass


class VersionDeclarationError(ManagerError):
    """

    The exception that is thrown in one of two below cases.
    1. User passes software image and version, at the same time.
    2. User doesn't passes any of them.
    """

    pass


class ImageNotInRepositoryError(ManagerError):
    """The exception that is thrown, if image is not in vManage images Repository"""

    pass


class TemplateNotFoundError(ManagerError):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class AttachedError(ManagerError):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateTypeError(ManagerError):
    """Used when wrong type template."""

    def __init__(self, name):
        self.message = f"Template: {name} - wrong template type."


class AlreadyExistsError(ManagerError):
    """Raised when an entity that we attempted to create already exists."""

    pass


class APIVersionError(ManagerError):
    """Raised when API is unsupported in running vManage version."""

    def __init__(self, item, supported, current):
        self.message = f"vManage is running: {current} but {item} only supported in API version: {supported}"


class APIViewError(ManagerError):
    """Raised when API is not allowed for given session type / view."""

    def __init__(self, item, allowed, current):
        self.message = f"Current view is: {current} but {item} only allowed for views: {allowed}"


class APIRequestPayloadTypeError(ManagerError):
    """Raised when unsupported payload type is passed to vManage request."""

    def __init__(self, item):
        self.message = f"Unsupported payload type: {type(item)} for vManage request"


class EmptyTaskResponseError(ManagerError):
    """Raised if task is registred by vManage, but reponse content is empty"""

    pass


class TaskNotRegisteredError(ManagerError):
    """Raised if task_id is generated, but it's not registere in vManage"""

    pass


class TaskValidationError(ManagerError):
    """Raised if task has not been validated"""

    pass


class MultiplePersonalityError(ManagerError):
    """Raised if Device DataSequnce contains devices with multiples personalities"""


class SessionNotCreatedError(ManagerError):
    """Raised when vManage session cannot be created"""

    pass


class TenantSubdomainNotFound(ManagerError):
    """Raised when given subdomain does not exist"""

    pass


class APIEndpointError(Exception):
    """Raised when there is a problem with endpoint definition"""

    pass


class TenantMigrationExportFileNotFound(ManagerError):
    """Raised when client cannot find exported file name in export task result"""

    pass


class TenantMigrationPreconditionsError(ManagerError):
    """Raised when preconditions for tenant migration fail"""

    pass
