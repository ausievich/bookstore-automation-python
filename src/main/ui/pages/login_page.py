"""Login page object."""

import allure
from playwright.sync_api import Locator, Page

from src.main.ui.locators.login_locators import LoginLocators


class LoginPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    @allure.step("Open login page")
    def open(self) -> "LoginPage":
        self._page.goto(f"{self._base_url}/login.html")
        return self

    @allure.step("Fill email: {email}")
    def fill_email(self, email: str) -> "LoginPage":
        self._page.fill(LoginLocators.EMAIL, email)
        return self

    @allure.step("Fill password")
    def fill_password(self, password: str) -> "LoginPage":
        self._page.fill(LoginLocators.PASSWORD, password)
        return self

    @allure.step("Submit login form")
    def submit(self) -> "LoginPage":
        self._page.click(LoginLocators.SUBMIT)
        return self

    @allure.step("Wait for catalog redirect")
    def wait_for_catalog_redirect(self) -> "LoginPage":
        self._page.wait_for_url("**/catalog.html", timeout=10_000)
        return self

    def get_error_locator(self) -> Locator:
        return self._page.locator(LoginLocators.ERROR)

    def get_email_validation_locator(self) -> Locator:
        return self._page.locator(LoginLocators.EMAIL_VALIDATION)

    def get_password_validation_locator(self) -> Locator:
        return self._page.locator(LoginLocators.PASSWORD_VALIDATION)
