"""Fluent builder for CreateBookRequest."""

from src.main.api.models.book import BookCategory, CreateBookRequest


class BookBuilder:
    """Fluent builder that produces a CreateBookRequest with sensible defaults."""

    def __init__(self) -> None:
        self._title: str = "Test Book"
        self._author: str = "Test Author"
        self._category: str = BookCategory.technology
        self._price: float = 29.99
        self._stock: int = 5

    def with_title(self, title: str) -> "BookBuilder":
        self._title = title
        return self

    # alias kept for JS parity
    withTitle = with_title  # type: ignore[assignment]

    def with_author(self, author: str) -> "BookBuilder":
        self._author = author
        return self

    def with_category(self, category: str) -> "BookBuilder":
        self._category = category
        return self

    def with_price(self, price: float) -> "BookBuilder":
        self._price = price
        return self

    def with_stock(self, stock: int) -> "BookBuilder":
        self._stock = stock
        return self

    def build(self) -> CreateBookRequest:
        return CreateBookRequest(
            title=self._title,
            author=self._author,
            category=self._category,
            price=self._price,
            stock=self._stock,
        )
