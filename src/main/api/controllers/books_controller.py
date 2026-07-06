"""Books API controller."""

from typing import Any

import httpx

from src.main.api.clients.http_client import HttpClient
from src.main.api.models.book import BookDto, BooksPageDto, CreateBookRequest, UpdateBookRequest


class BooksController:
    """Wraps /api/books endpoints."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def list(
        self,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        category: str | None = None,
        sort: str | None = None,
    ) -> BooksPageDto:
        params: dict[str, Any] = {"page": page, "limit": limit}
        if search:
            params["search"] = search
        if category:
            params["category"] = category
        if sort:
            params["sort"] = sort
        response = self.client.get("/api/books", params=params)
        response.raise_for_status()
        return BooksPageDto.model_validate(response.json())

    def get_by_id(self, book_id: str) -> BookDto:
        response = self.client.get(f"/api/books/{book_id}")
        response.raise_for_status()
        return BookDto.model_validate(response.json())

    def create(self, body: CreateBookRequest) -> BookDto:
        response = self.client.post("/api/books", json=body.model_dump())
        response.raise_for_status()
        return BookDto.model_validate(response.json())

    def update(self, book_id: str, body: UpdateBookRequest) -> BookDto:
        response = self.client.put(
            f"/api/books/{book_id}",
            json=body.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return BookDto.model_validate(response.json())

    def delete(self, book_id: str) -> httpx.Response:
        response = self.client.delete(f"/api/books/{book_id}")
        return response
