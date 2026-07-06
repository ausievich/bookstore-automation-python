"""Fluent builder for LoginRequest."""

from src.main.api.models.auth import LoginRequest


class UserBuilder:
    """Fluent builder that produces a LoginRequest with sensible defaults."""

    def __init__(self) -> None:
        self._email: str = "user@bookstore.test"
        self._password: str = "password123"

    def with_email(self, email: str) -> "UserBuilder":
        self._email = email
        return self

    def with_password(self, password: str) -> "UserBuilder":
        self._password = password
        return self

    def build(self) -> LoginRequest:
        return LoginRequest(email=self._email, password=self._password)
