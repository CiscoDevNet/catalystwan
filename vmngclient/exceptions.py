class InvalidOperationError(Exception):
    """The exception that is thrown when a method call is invalid for the object's current state."""

    pass


class RetrieveIntervalOutOfRange(Exception):
    pass


class VersionDeclarationError(Exception):
    """The exception that is thrown in one of two below cases.
    1. User passes software image and version, at the same time.
    2. User doesn't passes any of them."""

    pass


class ImageNotInRepositoryError(Exception):
    """The exception that is thrown, if image is not in vManage images Repository"""

    pass


class TemplateNotFoundError(Exception):
    """Used when a template item is not found."""

    def __init__(self, template):
        self.message = f"No such template: '{template}'"


class AttachedError(Exception):
    """Used when delete attached template."""

    def __init__(self, template):
        self.message = f"Template: {template} is attached to device."


class TemplateTypeError(Exception):
    """Used when wrong type template."""

    def __init__(self, name):
        self.message = f"Template: {name} - wrong template type."


class AlreadyExistsError(Exception):
    """Raised when an entity that we attempted to create already exists."""

    pass


class APIVersionError(Exception):
    """Raised when API is unsupported in running vManage version."""

    def __init__(self, item, supported, current):
        self.message = f"vManage is running: {current} but {item} only supported in API version: {supported}"


class APIViewError(Exception):
    """Raised when API is not allowed for given session type / view."""

    def __init__(self, item, allowed, current):
        self.message = f"Current view is: {current} but {item} only allowed for views: {allowed}"


class APIRequestPayloadTypeError(Exception):
    """Raised when unsupported payload type is passed to vManage request."""

    def __init__(self, item):
        self.message = f"Unsupported payload type: {type(item)} for vManage request"


class AuthenticationError(Exception):
    pass


class CookieNotValidError(Exception):
    pass


class EmptyTaskResponseError(Exception):
    """Raised if task is registred by vManage, but reponse content is empty"""

    pass


class TaskNotRegisteredError(Exception):
    """Raised if task_id is generated, but it's not registere in vManage"""

    pass


class MultiplePersonalityError(Exception):
    """Raised if Device DataSequnce contains devices with multiples personalities"""
