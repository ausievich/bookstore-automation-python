"""Cart-related Pydantic models."""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CartItemDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    book_id: str = Field(alias="bookId")
    quantity: int
    title: str
    price: float
    line_total: float = Field(alias="lineTotal")


class CartDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    items: list[CartItemDto]
    subtotal: float
