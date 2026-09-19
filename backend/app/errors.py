class DomainError(Exception):
    """Base class for errors the API layer translates to HTTP responses."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass
