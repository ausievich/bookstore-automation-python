"""Catalog page object."""

import allure
from playwright.sync_api import Locator, Page

from src.main.ui.locators.catalog_locators import CatalogLocators


class CatalogPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self._page = page
        self._base_url = base_url

    @allure.step("Open catalog page")
    def open(self) -> "CatalogPage":
        self._page.goto(f"{self._base_url}/catalog.html")
        return self

    @allure.step("Search for: {query}")
    def search(self, query: str) -> "CatalogPage":
        self._page.fill(CatalogLocators.SEARCH_INPUT, query)
        return self

    @allure.step("Filter by category: {category}")
    def filter_by_category(self, category: str) -> "CatalogPage":
        self._page.select_option(CatalogLocators.CATEGORY_FILTER, category)
        return self

    @allure.step("Sort by price: {direction}")
    def sort_by_price(self, direction: str) -> "CatalogPage":
        value = "price_asc" if direction == "asc" else "price_desc"
        self._page.select_option(CatalogLocators.SORT_SELECT, value)
        return self

    @allure.step("Apply filters")
    def apply_filters(self) -> "CatalogPage":
        self._page.click(CatalogLocators.SEARCH_SUBMIT)
        self._page.wait_for_timeout(500)
        return self

    @allure.step("Add book {book_id} to cart")
    def add_book_to_cart(self, book_id: str) -> "CatalogPage":
        self._page.click(CatalogLocators.add_to_cart_btn(book_id))
        self._page.wait_for_timeout(300)
        return self

    def get_book_items(self) -> Locator:
        return self._page.locator(f"{CatalogLocators.BOOK_LIST} li")

    def get_book_titles(self) -> Locator:
        return self._page.locator(CatalogLocators.BOOK_TITLE)

    def get_book_categories(self) -> Locator:
        return self._page.locator(CatalogLocators.BOOK_CATEGORY)

    def get_book_prices(self) -> Locator:
        return self._page.locator(CatalogLocators.BOOK_PRICE)

    def get_cart_counter(self) -> Locator:
        return self._page.locator(CatalogLocators.CART_COUNTER).first

    def get_dashboard_heading(self) -> Locator:
        return self._page.locator(CatalogLocators.DASHBOARD_HEADING)

    def get_no_results_message(self) -> Locator:
        return self._page.locator(CatalogLocators.NO_RESULTS)
