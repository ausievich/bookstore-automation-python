"""High-level catalog step helpers."""

import allure
from playwright.sync_api import Page, expect

from src.main.ui.pages.catalog_page import CatalogPage


class CatalogSteps:
    def __init__(self, page: Page, base_url: str) -> None:
        self._catalog_page = CatalogPage(page, base_url)

    @allure.step("Open catalog")
    def open_catalog(self) -> None:
        self._catalog_page.open()

    @allure.step("Search books: {query}")
    def search_books(self, query: str) -> None:
        self._catalog_page.search(query)

    @allure.step("Filter by category: {category}")
    def filter_by_category(self, category: str) -> None:
        self._catalog_page.filter_by_category(category)

    @allure.step("Sort by price: {direction}")
    def sort_by_price(self, direction: str) -> None:
        self._catalog_page.sort_by_price(direction)

    @allure.step("Apply search filters")
    def apply_search(self) -> None:
        self._catalog_page.apply_filters()

    @allure.step("Expect books visible")
    def expect_books_visible(self) -> None:
        expect(self._catalog_page.get_book_items().first).to_be_visible()

    @allure.step("Expect no results message")
    def expect_no_results(self) -> None:
        expect(self._catalog_page.get_no_results_message()).to_be_visible()

    @allure.step("Expect cart counter to be {count}")
    def expect_cart_counter(self, count: int) -> None:
        expect(self._catalog_page.get_cart_counter()).to_have_text(str(count))
