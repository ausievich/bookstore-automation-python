"""High-level cart step helpers."""

import allure
from playwright.sync_api import Page, expect

from src.main.ui.pages.cart_page import CartPage


class CartSteps:
    def __init__(self, page: Page, base_url: str) -> None:
        self._cart_page = CartPage(page, base_url)

    @allure.step("Open cart page")
    def open_cart(self) -> None:
        self._cart_page.open()

    @allure.step("Expect {n} items in cart")
    def expect_items_count(self, n: int) -> None:
        expect(self._cart_page.get_items()).to_have_count(n)

    @allure.step("Remove item {book_id} from cart")
    def remove_item(self, book_id: str) -> None:
        self._cart_page.remove_item(book_id)

    @allure.step("Update quantity of {book_id} to {qty}")
    def update_quantity(self, book_id: str, qty: int) -> None:
        self._cart_page.update_quantity(book_id, qty)

    @allure.step("Expect cart to be empty")
    def expect_empty_cart(self) -> None:
        expect(self._cart_page.get_empty_message()).to_be_visible()

    @allure.step("Expect subtotal contains: {text}")
    def expect_subtotal_contains(self, text: str) -> None:
        expect(self._cart_page.get_subtotal()).to_contain_text(text)
