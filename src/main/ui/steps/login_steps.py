"""High-level login step helpers."""

import allure
from playwright.sync_api import Page, expect

from src.main.ui.pages.login_page import LoginPage


class LoginSteps:
    def __init__(self, page: Page, base_url: str) -> None:
        self._login_page = LoginPage(page, base_url)

    @allure.step("Open login page")
    def open_login(self) -> None:
        self._login_page.open()

    @allure.step("Submit credentials")
    def submit_credentials(self, email: str, password: str) -> None:
        self._login_page.fill_email(email).fill_password(password).submit()

    @allure.step("Submit empty form")
    def submit_empty_form(self) -> None:
        self._login_page.submit()

    @allure.step("Wait for catalog redirect")
    def wait_for_catalog_redirect(self) -> None:
        self._login_page.wait_for_catalog_redirect()

    @allure.step("Expect dashboard visible")
    def expect_dashboard_visible(self) -> None:
        self._login_page.wait_for_catalog_redirect()

    @allure.step("Expect login error to be visible")
    def expect_login_error(self) -> None:
        expect(self._login_page.get_error_locator()).to_be_visible()

    @allure.step("Expect validation messages to be visible")
    def expect_validation_messages(self) -> None:
        expect(self._login_page.get_email_validation_locator()).to_be_visible()
        expect(self._login_page.get_password_validation_locator()).to_be_visible()
