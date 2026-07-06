"""UI tests: Book search and filtering."""

import allure
from playwright.sync_api import Page, expect

from src.main.common.annotations import AllureLayer, allure_metadata, tms_link
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps


class TestBookSearch:
    def setup_method(self) -> None:
        allure_metadata(layer=AllureLayer.UI, suite="Book Search & Filtering")

    @allure.title(f"{tms_link('C2001')} search by title shows matching books")
    def test_search_by_title(self, authenticated_page: Page, base_url: str) -> None:
        steps = CatalogSteps(authenticated_page, base_url)
        page_obj = CatalogPage(authenticated_page, base_url)

        with allure.step("Open catalog"):
            steps.open_catalog()

        with allure.step("Search for 'Dune'"):
            steps.search_books("Dune")
            steps.apply_search()

        with allure.step("Expect only Dune visible"):
            titles = page_obj.get_book_titles()
            expect(titles).to_have_count(1)
            expect(titles.first).to_contain_text("Dune")

    @allure.title(f"{tms_link('C2002')} filter by category")
    def test_filter_by_category(self, authenticated_page: Page, base_url: str) -> None:
        steps = CatalogSteps(authenticated_page, base_url)
        page_obj = CatalogPage(authenticated_page, base_url)

        with allure.step("Open catalog"):
            steps.open_catalog()

        with allure.step("Filter by Fiction category"):
            steps.filter_by_category("Fiction")
            steps.apply_search()

        with allure.step("Expect only Fiction books"):
            categories = page_obj.get_book_categories()
            count = categories.count()
            assert count > 0
            for i in range(count):
                expect(categories.nth(i)).to_have_text("Fiction")

    @allure.title(f"{tms_link('C2003')} sort by price ascending")
    def test_sort_by_price_ascending(self, authenticated_page: Page, base_url: str) -> None:
        steps = CatalogSteps(authenticated_page, base_url)
        page_obj = CatalogPage(authenticated_page, base_url)

        with allure.step("Open catalog"):
            steps.open_catalog()

        with allure.step("Sort by price ascending"):
            steps.sort_by_price("asc")
            steps.apply_search()

        with allure.step("Assert prices are in ascending order"):
            price_locators = page_obj.get_book_prices()
            count = price_locators.count()
            assert count > 1
            prices = [
                float(price_locators.nth(i).inner_text().replace("$", "")) for i in range(count)
            ]
            assert prices == sorted(prices), f"Prices not sorted ascending: {prices}"

    @allure.title(f"{tms_link('C2004')} no results message")
    def test_no_results_message(self, authenticated_page: Page, base_url: str) -> None:
        steps = CatalogSteps(authenticated_page, base_url)

        with allure.step("Open catalog"):
            steps.open_catalog()

        with allure.step("Search for non-existent book"):
            steps.search_books("xyzzy_nonexistent_12345")
            steps.apply_search()

        with allure.step("Expect no results message"):
            steps.expect_no_results()
