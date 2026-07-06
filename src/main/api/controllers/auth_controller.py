"""Authentication API controller."""

from src.main.api.clients.http_client import HttpClient
from src.main.api.models.auth import LoginResponse


class AuthController:
    """Wraps /api/auth endpoints."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def login(self, email: str, password: str) -> LoginResponse:
        response = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": password},
        )
        response.raise_for_status()
        return LoginResponse.model_validate(response.json())
