"""Orders API controller."""

from typing import Any

from src.main.api.clients.http_client import HttpClient
from src.main.api.models.order import OrderDto, OrdersPageDto, ShippingInfo, PaymentInfo


class OrdersController:
    """Wraps /api/orders endpoints."""

    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def create(self, shipping: ShippingInfo, payment: PaymentInfo) -> OrderDto:
        response = self.client.post(
            "/api/orders",
            json={
                "shipping": shipping.model_dump(),
                "payment": {"cardLast4": payment.card_last4},
            },
        )
        response.raise_for_status()
        return OrderDto.model_validate(response.json())

    def list(self, page: int = 1, limit: int = 10) -> OrdersPageDto:
        params: dict[str, Any] = {"page": page, "limit": limit}
        response = self.client.get("/api/orders", params=params)
        response.raise_for_status()
        return OrdersPageDto.model_validate(response.json())

    def get_by_id(self, order_id: str) -> OrderDto:
        response = self.client.get(f"/api/orders/{order_id}")
        response.raise_for_status()
        return OrderDto.model_validate(response.json())

    def update_status(self, order_id: str, status: str) -> OrderDto:
        response = self.client.patch(
            f"/api/orders/{order_id}/status",
            json={"status": status},
        )
        response.raise_for_status()
        return OrderDto.model_validate(response.json())
