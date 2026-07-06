"""Order-related Pydantic models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OrderStatus(StrEnum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"


class OrderItemDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    book_id: str = Field(alias="bookId")
    title: str
    quantity: int
    unit_price: float = Field(alias="unitPrice")


class ShippingInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    address: str
    city: str
    zip: str


class PaymentInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    card_last4: str = Field(alias="cardLast4")


class OrderDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    items: list[OrderItemDto]
    shipping: ShippingInfo
    payment: PaymentInfo
    status: str
    total: float
    created_at: str = Field(alias="createdAt")


class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    shipping: ShippingInfo
    payment: PaymentInfo


class OrdersPageDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    items: list[OrderDto]
    total: int
    page: int
    limit: int
