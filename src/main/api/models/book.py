"""Book-related Pydantic models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BookCategory(StrEnum):
    fiction = "Fiction"
    technology = "Technology"
    science = "Science"
    history = "History"


class BookDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    title: str
    author: str
    category: str
    price: float
    stock: int
    deleted: bool | None = None


class CreateBookRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str
    author: str
    category: str
    price: float
    stock: int


class UpdateBookRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    author: str | None = None
    category: str | None = None
    price: float | None = None
    stock: int | None = None


class BooksPageDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    items: list[BookDto]
    total: int
    page: int
    limit: int
