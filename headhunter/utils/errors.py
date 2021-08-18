# fmt: off
from typing import Dict


class ValidationError(Exception): ...

# Token exceptions
class TokenValidationError(ValidationError): ...

# HH HTTP exceptions
class HHError(ValidationError): ...

class InvalidResponseError(HHError): ...

class GetTokenError(HHError): ...

class InvalidRequestError(GetTokenError): ...
class AccountNotFound(InvalidRequestError): ...
class AccountIsLocked(InvalidRequestError): ...
class PasswordInvalidated(InvalidRequestError): ...
class LoginNotVerified(InvalidRequestError): ...
class BadRedirectUrl(InvalidRequestError): ...
class TokenIsEmpty(InvalidRequestError): ...
class TokenNotFound(InvalidRequestError): ...
class CodeNotFound(InvalidRequestError): ...

class InvalidClientError(GetTokenError): ...

class InvalidGrantError(GetTokenError): ...
class TokenAlreadyRefreshed(InvalidGrantError): ...
class TokenNotExpired(InvalidGrantError): ...
class TokenWasRevoked(InvalidGrantError): ...
class BadToken(InvalidGrantError): ...
class CodeAlreadyUsed(InvalidGrantError): ...
class CodeExpired(InvalidGrantError): ...
class CodeRevoked(InvalidGrantError): ...
class TokenDeactivated(InvalidGrantError): ...

class UnsoportedGrantTypeError(GetTokenError): ...

class ForbiddenError(GetTokenError): ...

class UnknownError(GetTokenError): ...

class OAuthError(HHError): ...
class NotValidToken(OAuthError): ...
class TokenExpired(OAuthError): ...
class TokenRevoked(OAuthError): ...
class ApplicationNotFound(OAuthError): ...

class ServiceUnavailableError(HHError): ...

class InternalServiceError(HHError): ...


# DB manager exceptions
class DBManagerError(Exception): ...
class CommitError(DBManagerError): ...
# fmt: on


TOKEN_ERR: Dict[str, GetTokenError] = {
    "invalid_request": InvalidRequestError,
    "invalid_client": InvalidClientError,
    "invalid_grant": InvalidGrantError,
    "unsupported_grant_type": UnsoportedGrantTypeError,
    "forbidden": ForbiddenError,
}

TOKEN_ERR_DETAIL: Dict[str, GetTokenError] = {
    "account not found": AccountNotFound,
    "account is locked": AccountIsLocked,
    "password invalidated": PasswordInvalidated,
    "login not verified": LoginNotVerified,
    "bad redirect url": BadRedirectUrl,
    "token is empty": TokenIsEmpty,
    "token not found": TokenNotFound,
    "code not found": CodeNotFound,
    "token has already been refreshed": TokenAlreadyRefreshed,
    "token not expired": TokenNotExpired,
    "token was revoked": TokenWasRevoked,
    "bad token": BadToken,
    "code has already been used": CodeAlreadyUsed,
    "code expired": CodeExpired,
    "code was revoke": CodeRevoked,
    "token deactivated": TokenDeactivated,
}


AUTH_ERR: Dict[str, OAuthError] = {
    "bad_authorization": NotValidToken,
    "token_expired": TokenExpired,
    "token_revoked": TokenRevoked,
    "application_not_found": ApplicationNotFound,
}