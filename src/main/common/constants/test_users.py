"""Test user constants."""


class TestUsers:
    valid: dict[str, str] = {"email": "user@bookstore.test", "password": "password123"}
    invalid_password: dict[str, str] = {"email": "user@bookstore.test", "password": "wrong-password"}
