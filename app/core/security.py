"""Authentication module using OAuth2, Auth0 and JWT.

The token is verified using the PyJWT library.
We use Auth0 to issue the tokens.

"""

# pylint: disable=too-few-public-methods

from collections.abc import Awaitable, Callable
from os import getenv

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.exceptions import UnauthenticatedException, UnauthorizedException

load_dotenv()
oauth2_scheme = HTTPBearer(auto_error=False)


NAMESPACE = getenv("AUTH_NAMESPACE", "https://fastapiexample.com").rstrip("/")


def claim(user: dict, name: str, default: str | None = None) -> str | None:
    """Return a namespaced custom claim from the token payload."""
    return user.get(f"{NAMESPACE}/{name}", default)


def has_perm(user: dict, permission: str) -> bool:
    """Check whether a user has required permissions."""
    return permission in set(user.get("permissions", []))


class VerifyToken:
    """A class to verify the token using PyJWT."""

    def __init__(self) -> None:
        """Initialise the class."""
        self.config = get_settings()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f"https://{self.config.auth0_domain}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
        self,
        token: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
    ) -> dict:
        """Verify token and return the payload."""
        if not token or not token.credentials:
            raise UnauthenticatedException

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials,
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(
                detail=f"Unable to verify token: {error!s}",
            ) from error
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(
                detail=f"Invalid token format: {error!s}",
            ) from error

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience,
                issuer=self.config.auth0_issuer,
            )
        except jwt.ExpiredSignatureError as err:
            raise UnauthorizedException(
                detail="Token has expired",
            ) from err
        except jwt.InvalidTokenError as err:
            raise UnauthorizedException(
                detail=f"Invalid token: {err!s}",
            ) from err
        except Exception as error:
            raise UnauthorizedException(
                detail=f"Token verification failed: {error!s}",
            ) from error

        return payload


# Singleton instance for dependency injection
token_verifier = VerifyToken()


async def get_current_user(
    payload: dict = Depends(token_verifier.verify),
) -> dict:
    """Dependency to get the current authenticated user from token payload.

    Args:
        payload: Decoded JWT token payload.

    Returns:
        User information from token payload.

    Example:
    ```python
        @router.get("/me")
        async def get_me(user: dict = Depends(get_current_user)):
            return user
    ```

    """
    return payload


def require_permission(required_permission: str) -> Callable[[dict], Awaitable[dict]]:
    """Dependency factory to check for specific permissions.

    Args:
        required_permission: The permission string required (e.g., "read:rentals").

    Returns:
        Dependency function that validates the permission.

    Example:
    ```python
        @router.delete("/{id}")
        async def delete_rental(
            id: int,
            user: dict = Depends(require_permission("delete:rentals"))
        ):
            pass
    ```

    """

    async def permission_checker(user: dict = Depends(get_current_user)) -> dict:
        if not has_perm(user, required_permission):
            raise UnauthorizedException(
                detail=f"Permission '{required_permission}' required",
            )
        return user

    return permission_checker


def require_customer(
    required_scope: str | None = None,
) -> Callable[[dict], Awaitable[dict]]:
    """Ensure the caller is a customer.

    If required_scope is provided, also ensure the caller has that permission
     (e.g., 'read:customers:self').
    """

    async def customer_checker(user: dict = Depends(get_current_user)) -> dict:
        user_type = claim(user, "user_type")
        if user_type != "customer":
            raise UnauthorizedException(detail="Customer required")
        if required_scope and not has_perm(user, required_scope):
            raise UnauthorizedException(
                detail=f"Permission '{required_scope}' required",
            )
        return user

    return customer_checker
