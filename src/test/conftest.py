"""Root conftest: fixtures shared across all tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from src.main.api.clients.http_client import HttpClient
from src.main.api.controllers.auth_controller import AuthController
from src.main.api.controllers.books_controller import BooksController
from src.main.api.controllers.cart_controller import CartController
from src.main.api.controllers.orders_controller import OrdersController
from src.main.api.flows.auth_flow import AuthFlow
from src.main.common.config.environment import Environment
from src.main.common.constants.test_users import TestUsers

# ---------------------------------------------------------------------------
# Base URL
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def base_url() -> str:
    return Environment.base_url


# ---------------------------------------------------------------------------
# HTTP client (one per test, closed after)
# ---------------------------------------------------------------------------


@pytest.fixture
def http_client(base_url: str) -> Generator[HttpClient, None, None]:
    client = HttpClient(base_url)
    yield client
    client.close()


# ---------------------------------------------------------------------------
# State reset (autouse so every test starts clean)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def api_reset(http_client: HttpClient) -> None:
    http_client.post("/api/test/reset")


# ---------------------------------------------------------------------------
# Controller fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def auth_controller(http_client: HttpClient) -> AuthController:
    return AuthController(http_client)


@pytest.fixture
def books_api(http_client: HttpClient) -> BooksController:
    return BooksController(http_client)


@pytest.fixture
def cart_api(http_client: HttpClient) -> CartController:
    return CartController(http_client)


@pytest.fixture
def orders_api(http_client: HttpClient) -> OrdersController:
    return OrdersController(http_client)


# ---------------------------------------------------------------------------
# Authenticated token (sets token on the shared client)
# ---------------------------------------------------------------------------


@pytest.fixture
def auth_token(http_client: HttpClient, api_reset: None) -> Generator[str, None, None]:
    flow = AuthFlow(http_client)
    token = flow.login_as_default_user()
    http_client.set_auth_token(token)
    yield token
    http_client.set_auth_token(None)


# ---------------------------------------------------------------------------
# Catalog page fixture (injects auth token into browser localStorage)
# ---------------------------------------------------------------------------


@pytest.fixture
def catalog_page(page: Page, base_url: str, api_reset: None) -> Page:
    import httpx

    resp = httpx.post(
        f"{base_url}/api/auth/login",
        json={"email": TestUsers.valid["email"], "password": TestUsers.valid["password"]},
    )
    token = resp.json()["token"]
    page.goto(f"{base_url}/catalog.html")
    page.evaluate(f"localStorage.setItem('token', '{token}')")
    page.goto(f"{base_url}/catalog.html")
    return page
