class ValidationError(Exception):
    pass


class TokenValidationError(ValidationError):
    pass


class DBManagerError(Exception):
    pass


class CommitError(DBManagerError):
    pass
