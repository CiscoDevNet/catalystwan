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
