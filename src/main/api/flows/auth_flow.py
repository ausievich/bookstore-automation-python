"""High-level auth flow helpers."""

from src.main.api.clients.http_client import HttpClient
from src.main.api.controllers.auth_controller import AuthController
from src.main.common.constants.test_users import TestUsers


class AuthFlow:
    """Reusable login flows for test setup."""

    def __init__(self, client: HttpClient) -> None:
        self._auth = AuthController(client)

    def login_as_default_user(self) -> str:
        """Log in as the seed user and return the bearer token."""
        resp = self._auth.login(
            email=TestUsers.valid["email"],
            password=TestUsers.valid["password"],
        )
        return resp.token
