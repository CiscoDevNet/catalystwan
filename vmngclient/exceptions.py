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


class AlreadyExistsError(Exception):
    """Raised when an entity that we attempted to create already exists."""

    pass
