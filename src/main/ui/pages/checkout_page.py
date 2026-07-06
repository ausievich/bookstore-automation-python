"""Checkout page object."""

import allure
from playwright.sync_api import Locator, Page

from src.main.ui.locators.checkout_locators import CheckoutLocators


class CheckoutPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    @allure.step("Fill shipping info")
    def fill_shipping(self, name: str, address: str, city: str, zip_code: str) -> "CheckoutPage":
        self._page.fill(CheckoutLocators.SHIP_NAME, name)
        self._page.fill(CheckoutLocators.SHIP_ADDRESS, address)
        self._page.fill(CheckoutLocators.SHIP_CITY, city)
        self._page.fill(CheckoutLocators.SHIP_ZIP, zip_code)
        return self

    @allure.step("Continue to payment")
    def continue_to_payment(self) -> "CheckoutPage":
        self._page.click(CheckoutLocators.SHIPPING_NEXT)
        self._page.wait_for_timeout(300)
        return self

    @allure.step("Fill payment info")
    def fill_payment(self, card_number: str, card_last4: str) -> "CheckoutPage":
        self._page.fill(CheckoutLocators.CARD_NUMBER, card_number)
        self._page.fill(CheckoutLocators.CARD_LAST4, card_last4)
        return self

    @allure.step("Review order")
    def review_order(self) -> "CheckoutPage":
        self._page.click(CheckoutLocators.PAYMENT_NEXT)
        self._page.wait_for_timeout(500)
        return self

    @allure.step("Confirm order")
    def confirm_order(self) -> "CheckoutPage":
        self._page.click(CheckoutLocators.CONFIRM_ORDER)
        return self

    def get_order_summary(self) -> Locator:
        return self._page.locator(CheckoutLocators.ORDER_SUMMARY)
