"""UI tests: Shopping cart interactions."""

import allure
from playwright.sync_api import Page

from src.main.common.annotations import AllureLayer, allure_metadata, tms_link
from src.main.ui.pages.cart_page import CartPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.cart_steps import CartSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


class TestShoppingCart:
    def setup_method(self) -> None:
        allure_metadata(layer=AllureLayer.UI, suite="Shopping Cart")

    @allure.title(f"{tms_link('C3001')} add book updates cart counter")
    def test_add_book_updates_cart_counter(self, authenticated_page: Page, base_url: str) -> None:
        catalog = CatalogPage(authenticated_page, base_url)
        steps = CatalogSteps(authenticated_page, base_url)

        with allure.step("Open catalog"):
            steps.open_catalog()

        with allure.step("Add book b1 to cart"):
            catalog.add_book_to_cart("b1")

        with allure.step("Assert cart counter is 1"):
            steps.expect_cart_counter(1)

    @allure.title(f"{tms_link('C3002')} multiple books in cart")
    def test_multiple_books_in_cart(self, authenticated_page: Page, base_url: str) -> None:
        catalog = CatalogPage(authenticated_page, base_url)
        cart_steps = CartSteps(authenticated_page, base_url)

        with allure.step("Open catalog and add two books"):
            catalog.open()
            catalog.add_book_to_cart("b1")
            catalog.add_book_to_cart("b3")

        with allure.step("Open cart and check item count"):
            cart_steps.open_cart()
            cart_steps.expect_items_count(2)

    @allure.title(f"{tms_link('C3003')} remove book from cart")
    def test_remove_book_from_cart(self, authenticated_page: Page, base_url: str) -> None:
        catalog = CatalogPage(authenticated_page, base_url)
        cart_steps = CartSteps(authenticated_page, base_url)

        with allure.step("Add two books to cart"):
            catalog.open()
            catalog.add_book_to_cart("b1")
            catalog.add_book_to_cart("b3")

        with allure.step("Open cart and remove b1"):
            cart_steps.open_cart()
            cart_steps.remove_item("b1")

        with allure.step("Assert only 1 item remains"):
            cart_steps.expect_items_count(1)

    @allure.title(f"{tms_link('C3004')} update quantity recalculates subtotal")
    def test_update_quantity_recalculates_subtotal(
        self, authenticated_page: Page, base_url: str
    ) -> None:
        catalog = CatalogPage(authenticated_page, base_url)
        cart_page = CartPage(authenticated_page, base_url)
        cart_steps = CartSteps(authenticated_page, base_url)

        with allure.step("Add book b3 (Dune $18.99)"):
            catalog.open()
            catalog.add_book_to_cart("b3")

        with allure.step("Open cart"):
            cart_page.open()

        with allure.step("Update quantity to 2"):
            cart_page.update_quantity("b3", 2)

        with allure.step("Assert subtotal reflects 2x price"):
            cart_steps.expect_subtotal_contains("37.98")

    @allure.title(f"{tms_link('C3005')} empty cart message")
    def test_empty_cart_message(self, authenticated_page: Page, base_url: str) -> None:
        cart_steps = CartSteps(authenticated_page, base_url)

        with allure.step("Open cart without adding items"):
            cart_steps.open_cart()

        with allure.step("Assert empty cart message visible"):
            cart_steps.expect_empty_cart()
