"""Cart API controller."""

from src.main.api.clients.http_client import HttpClient
from src.main.api.models.cart import CartDto


class CartController:
    """Wraps /api/cart endpoints."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def get(self) -> CartDto:
        response = self.client.get("/api/cart")
        response.raise_for_status()
        return CartDto.model_validate(response.json())

    def add_item(self, book_id: str, quantity: int = 1) -> CartDto:
        response = self.client.post(
            "/api/cart/items",
            json={"bookId": book_id, "quantity": quantity},
        )
        response.raise_for_status()
        return CartDto.model_validate(response.json())

    def update_item(self, book_id: str, quantity: int) -> CartDto:
        response = self.client.patch(
            f"/api/cart/items/{book_id}",
            json={"quantity": quantity},
        )
        response.raise_for_status()
        return CartDto.model_validate(response.json())

    def remove_item(self, book_id: str) -> CartDto:
        response = self.client.delete(f"/api/cart/items/{book_id}")
        response.raise_for_status()
        return CartDto.model_validate(response.json())
