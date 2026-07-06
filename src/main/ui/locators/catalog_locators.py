"""Locator constants for the catalog page."""


class CatalogLocators:
    DASHBOARD_HEADING = '[data-testid="dashboard-heading"]'
    SEARCH_INPUT = '[data-testid="search-input"]'
    CATEGORY_FILTER = '[data-testid="category-filter"]'
    SORT_SELECT = '[data-testid="sort-select"]'
    SEARCH_SUBMIT = '[data-testid="search-submit"]'
    BOOK_LIST = '[data-testid="book-list"]'
    NO_RESULTS = '[data-testid="no-results-message"]'
    CART_COUNTER = '[data-testid="cart-counter"]'
    BOOK_TITLE = '[data-testid="book-title"]'
    BOOK_AUTHOR = '[data-testid="book-author"]'
    BOOK_PRICE = '[data-testid="book-price"]'
    BOOK_CATEGORY = '[data-testid="book-category"]'

    @staticmethod
    def book_item(book_id: str) -> str:
        return f'[data-testid="book-item-{book_id}"]'

    @staticmethod
    def add_to_cart_btn(book_id: str) -> str:
        return f'[data-testid="add-to-cart-{book_id}"]'
