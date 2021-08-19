from typing import Dict, Type


class ValidationError(Exception):
    for_user = False
    error_text = ""


# Token exceptions
class TokenValidationError(ValidationError):
    for_user = True
    error_text = "Can't get valid token from hh.ru, try again later"


# HH HTTP exceptions
class HHError(ValidationError):
    ...


class InvalidResponseError(HHError):
    error_text = "Response doesn't contain valid data (must be json)"


class GetTokenError(HHError):
    error_text = "Unknown error getting token"


class InvalidRequestError(GetTokenError):
    error_text = "Invalid request"


class AccountNotFound(InvalidRequestError):
    error_text = "Invalid client_id and client_secret pair"


class AccountIsLocked(InvalidRequestError):
    error_text = "Account is locked, contact the support of hh.ru"
    for_user = True


class PasswordInvalidated(InvalidRequestError):
    error_text = "Password expired, visit hh.ru and restore password"
    for_user = True


class LoginNotVerified(InvalidRequestError):
    error_text = "Account not verified, contact the support of hh.ru"
    for_user = True


class BadRedirectUrl(InvalidRequestError):
    error_text = "Invalid redirect url"


class TokenIsEmpty(InvalidRequestError):
    error_text = "Empty refresh token"


class TokenNotFound(InvalidRequestError):
    error_text = "Invalid refresh token"


class CodeNotFound(InvalidRequestError):
    error_text = "authorization_code not found"


class InvalidClientError(GetTokenError):
    error_text = "client_id not found or invalid client_secret"


class InvalidGrantError(GetTokenError):
    error_text = "Invalid grant"


class TokenAlreadyRefreshed(InvalidGrantError):
    error_text = "Refresh token already used"


class TokenNotExpired(InvalidGrantError):
    error_text = "Token not expired"


class TokenWasRevoked(InvalidGrantError):
    error_text = "Token revoked, check the password expiration date"
    for_user = True


class BadToken(InvalidGrantError):
    error_text = "Invalid token"


class CodeAlreadyUsed(InvalidGrantError):
    error_text = "authorization_code already used"


class CodeExpired(InvalidGrantError):
    error_text = "authorization_code expired"
    for_user = True


class CodeRevoked(InvalidGrantError):
    error_text = "authorization_code revoked"
    for_user = True


class TokenDeactivated(InvalidGrantError):
    error_text = "Token deactivated"
    for_user = True


class UnsoportedGrantTypeError(GetTokenError):
    error_text = "Invalid grant_type value"


class ForbiddenError(GetTokenError):
    error_text = "Too many requests, try wait 5 minutes and try again"
    for_user = True


class OAuthError(HHError):
    error_text = "Unknwn auth error"


class BadAuthorizationError(OAuthError):
    error_text = "Token invalid or not found"


class TokenExpired(OAuthError):
    error_text = "access_token expired"


class TokenRevoked(OAuthError):
    error_text = "access_token revoked"


class ApplicationNotFound(OAuthError):
    error_text = "Application removed"


class ServiceUnavailableError(HHError):
    for_user = True
    error_text = "HH service is unavailable"


class InternalServiceError(HHError):
    for_user = True
    error_text = "Internal service error"


class UnknownError(HHError):
    for_user = True
    error_text = "Unknow error from hh api"


# DB manager exceptions
class DBManagerError(Exception):
    ...


class CommitError(DBManagerError):
    ...


TOKEN_ERR: Dict[str, Type[GetTokenError]] = {
    "invalid_request": InvalidRequestError,
    "invalid_client": InvalidClientError,
    "invalid_grant": InvalidGrantError,
    "unsupported_grant_type": UnsoportedGrantTypeError,
    "forbidden": ForbiddenError,
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


AUTH_ERR: Dict[str, Type[OAuthError]] = {
    "bad_authorization": BadAuthorizationError,
    "token_expired": TokenExpired,
    "token_revoked": TokenRevoked,
    "application_not_found": ApplicationNotFound,
}
