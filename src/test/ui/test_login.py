"""UI tests: Login page."""

import allure
from playwright.sync_api import Page

from src.main.common.annotations import allure_metadata
from src.main.common.constants.test_users import TestUsers
from src.main.ui.steps.login_steps import LoginSteps


@allure.feature("Login UI")
class TestLogin:
    def setup_method(self) -> None:
        allure_metadata("UI")

    def test_valid_login_shows_catalog(self, page: Page, base_url: str) -> None:
        steps = LoginSteps(page, base_url)

        with allure.step("Open login page"):
            steps.open_login()

        with allure.step("Submit valid credentials"):
            steps.submit_credentials(TestUsers.valid["email"], TestUsers.valid["password"])

        with allure.step("Expect redirect to catalog"):
            steps.wait_for_catalog_redirect()

    def test_invalid_password_shows_error(self, page: Page, base_url: str) -> None:
        steps = LoginSteps(page, base_url)

        with allure.step("Open login page"):
            steps.open_login()

        with allure.step("Submit invalid credentials"):
            steps.submit_credentials(
                TestUsers.invalid_password["email"],
                TestUsers.invalid_password["password"],
            )

        with allure.step("Expect error message"):
            steps.expect_login_error()

    def test_empty_fields_show_validation(self, page: Page, base_url: str) -> None:
        steps = LoginSteps(page, base_url)

        with allure.step("Open login page"):
            steps.open_login()

        with allure.step("Submit empty form"):
            steps.submit_empty_form()

        with allure.step("Expect validation messages"):
            steps.expect_validation_messages()
