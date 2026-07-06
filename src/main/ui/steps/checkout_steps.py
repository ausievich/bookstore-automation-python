"""High-level checkout step helpers."""

import allure
from playwright.sync_api import Page

from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._checkout_page = CheckoutPage(page, base_url)

    @allure.step("Complete shipping form")
    def complete_shipping(self, name: str, address: str, city: str, zip_code: str) -> None:
        self._checkout_page.fill_shipping(name, address, city, zip_code).continue_to_payment()

    @allure.step("Complete payment form")
    def complete_payment(self, card_number: str, last4: str) -> None:
        self._checkout_page.fill_payment(card_number, last4).review_order()

    @allure.step("Complete review and place order")
    def complete_review(self) -> None:
        self._checkout_page.confirm_order()

    @allure.step("Expect order success page")
    def expect_order_success(self) -> None:
        self._page.wait_for_url("**/order-success.html**", timeout=10_000)
