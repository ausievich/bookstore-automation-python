"""API tests: Books CRUD."""

import allure

from src.main.api.builders.book_builder import BookBuilder
from src.main.api.controllers.books_controller import BooksController
from src.main.api.models.book import UpdateBookRequest
from src.main.common.annotations import AllureLayer, allure_metadata, tms_link


class TestBooksCrud:
    def setup_method(self) -> None:
        allure_metadata(layer=AllureLayer.API, suite="Books CRUD API")

    @allure.title(f"{tms_link('C5001')} GET /api/books returns paginated list")
    def test_list_books_returns_paginated_data(
        self, books_api: BooksController, api_reset: None
    ) -> None:
        with allure.step("List books with default pagination"):
            result = books_api.list(page=1, limit=5)

        with allure.step("Assert pagination fields present"):
            assert result.total >= 6
            assert result.page == 1
            assert result.limit == 5
            assert len(result.items) == 5

    @allure.title(f"{tms_link('C5002')} GET /api/books/:id returns single book")
    def test_get_book_by_id(self, books_api: BooksController, api_reset: None) -> None:
        with allure.step("Get book b1"):
            book = books_api.get_by_id("b1")

        with allure.step("Assert correct book returned"):
            assert book.id == "b1"
            assert book.title == "Clean Code"
            assert book.author == "Robert Martin"

    @allure.title(f"{tms_link('C5003')} POST /api/books creates book when authenticated")
    def test_create_book_with_auth(self, books_api: BooksController, auth_token: str) -> None:
        payload = BookBuilder().with_title("My New Book").with_price(9.99).build()

        with allure.step("Create book"):
            created = books_api.create(payload)

        with allure.step("Assert book created"):
            assert created.title == "My New Book"
            assert created.price == 9.99
            assert created.id.startswith("b")

    @allure.title(f"{tms_link('C5004')} PUT /api/books/:id updates book fields")
    def test_update_book(self, books_api: BooksController, auth_token: str) -> None:
        with allure.step("Update book b1 price"):
            updated = books_api.update("b1", UpdateBookRequest(price=99.99))

        with allure.step("Assert price updated"):
            assert updated.price == 99.99
            assert updated.id == "b1"

    @allure.title(f"{tms_link('C5005')} DELETE /api/books/:id soft-deletes book")
    def test_delete_book(self, books_api: BooksController, auth_token: str) -> None:
        with allure.step("Delete book b1"):
            response = books_api.delete("b1")

        with allure.step("Assert 204 response"):
            assert response.status_code == 204

        with allure.step("Verify book is no longer accessible"):
            get_response = books_api.client.get("/api/books/b1")
            assert get_response.status_code == 404

    @allure.title(f"{tms_link('C5006')} POST /api/books without auth returns 401")
    def test_create_book_without_auth_returns_401(
        self, books_api: BooksController, api_reset: None
    ) -> None:
        payload = BookBuilder().build()

        with allure.step("Attempt to create book without auth token"):
            response = books_api.client.post("/api/books", json=payload.model_dump())

        with allure.step("Assert 401 Unauthorized"):
            assert response.status_code == 401
