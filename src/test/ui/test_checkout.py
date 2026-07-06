"""UI tests: Checkout flow."""

import allure
from playwright.sync_api import Page

from src.main.common.annotations import allure_metadata
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.checkout_steps import CheckoutSteps


@allure.feature("Checkout UI")
class TestCheckout:
    def setup_method(self) -> None:
        allure_metadata("UI")

    def test_complete_checkout_flow(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        catalog = CatalogPage(authenticated_page, base_url)
        checkout_steps = CheckoutSteps(authenticated_page, base_url)

        with allure.step("Add a book to cart"):
            catalog.open()
            catalog.add_book_to_cart("b3")

        with allure.step("Navigate to checkout"):
            authenticated_page.goto(f"{base_url}/checkout.html")

        with allure.step("Complete shipping form"):
            checkout_steps.complete_shipping(
                name="Jane Doe",
                address="42 Elm Street",
                city="Springfield",
                zip_code="12345",
            )

        with allure.step("Complete payment form"):
            checkout_steps.complete_payment(
                card_number="4111111111111111",
                last4="1111",
            )

        with allure.step("Confirm order"):
            checkout_steps.complete_review()

        with allure.step("Expect order success page"):
            checkout_steps.expect_order_success()
