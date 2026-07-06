"""UI-specific conftest: browser state reset before each UI test."""

from collections.abc import Generator

import pytest
from playwright.sync_api import Page


@pytest.fixture(autouse=True)
def reset_browser_state(page: Page, base_url: str) -> Generator[None, None, None]:
    """Clear localStorage before every UI test."""
    page.goto(f"{base_url}/login.html")
    page.evaluate("localStorage.clear()")
    yield


@pytest.fixture
def authenticated_page(page: Page, base_url: str, api_reset: None) -> Page:
    """Return a page with auth token already set in localStorage."""
    import httpx

    from src.main.common.constants.test_users import TestUsers

    resp = httpx.post(
        f"{base_url}/api/auth/login",
        json={"email": TestUsers.valid["email"], "password": TestUsers.valid["password"]},
    )
    token = resp.json()["token"]
    page.goto(f"{base_url}/login.html")
    page.evaluate(f"localStorage.setItem('token', '{token}')")
    return page
