"""Cart page object."""

import allure
from playwright.sync_api import Locator, Page

from src.main.ui.locators.cart_locators import CartLocators


class CartPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    @allure.step("Open cart page")
    def open(self) -> "CartPage":
        self._page.goto(f"{self._base_url}/cart.html")
        return self

    @allure.step("Go to checkout")
    def go_to_checkout(self) -> "CartPage":
        self._page.click(CartLocators.CHECKOUT_LINK)
        return self

    @allure.step("Remove item {book_id} from cart")
    def remove_item(self, book_id: str) -> "CartPage":
        self._page.click(CartLocators.remove_btn(book_id))
        self._page.wait_for_timeout(300)
        return self

    @allure.step("Update quantity of {book_id} to {quantity}")
    def update_quantity(self, book_id: str, quantity: int) -> "CartPage":
        self._page.fill(CartLocators.qty_input(book_id), str(quantity))
        self._page.dispatch_event(CartLocators.qty_input(book_id), "change")
        self._page.wait_for_timeout(300)
        return self

    def get_items(self) -> Locator:
        return self._page.locator(f"{CartLocators.CART_ITEMS} tr")

    def get_empty_message(self) -> Locator:
        return self._page.locator(CartLocators.EMPTY_MESSAGE)

    def get_subtotal(self) -> Locator:
        return self._page.locator(CartLocators.SUBTOTAL)
