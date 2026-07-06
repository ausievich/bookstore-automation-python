"""In-memory data store for the bookstore mock server."""

from __future__ import annotations

import time
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Book:
    id: str
    title: str
    author: str
    category: str
    price: float
    stock: int
    deleted: bool = False


@dataclass
class User:
    id: str
    email: str
    password: str
    name: str


@dataclass
class CartItem:
    book_id: str
    quantity: int


@dataclass
class OrderItem:
    book_id: str
    title: str
    quantity: int
    unit_price: float


@dataclass
class ShippingInfo:
    name: str
    address: str
    city: str
    zip: str


@dataclass
class PaymentInfo:
    card_last4: str


@dataclass
class Order:
    id: str
    user_id: str
    items: list[OrderItem]
    shipping: ShippingInfo
    payment: PaymentInfo
    status: str
    total: float
    created_at: str


SEED_BOOKS: list[dict[str, Any]] = [
    {"id": "b1", "title": "Clean Code", "author": "Robert Martin", "category": "Technology", "price": 42.99, "stock": 10},
    {"id": "b2", "title": "The Pragmatic Programmer", "author": "Hunt & Thomas", "category": "Technology", "price": 39.50, "stock": 8},
    {"id": "b3", "title": "Dune", "author": "Frank Herbert", "category": "Fiction", "price": 18.99, "stock": 15},
    {"id": "b4", "title": "Sapiens", "author": "Yuval Harari", "category": "History", "price": 22.00, "stock": 12},
    {"id": "b5", "title": "A Brief History of Time", "author": "Stephen Hawking", "category": "Science", "price": 15.75, "stock": 6},
    {"id": "b6", "title": "Neuromancer", "author": "William Gibson", "category": "Fiction", "price": 14.25, "stock": 0},
]

SEED_USERS: list[dict[str, Any]] = [
    {"id": "u1", "email": "user@bookstore.test", "password": "password123", "name": "Test User"},
]


class BookstoreStore:
    """Singleton in-memory store for the bookstore mock server."""

    def __init__(self) -> None:
        self.books: list[Book] = []
        self.users: list[User] = []
        self.carts: dict[str, list[CartItem]] = {}
        self.orders: list[Order] = []
        self.tokens: dict[str, str] = {}  # token -> user_id
        self._order_counter: int = 1000

        self._init_users()
        self.reset()

    def _init_users(self) -> None:
        self.users = [User(**u) for u in SEED_USERS]

    def reset(self) -> None:
        """Restore seed data and clear transient state."""
        self.books = [Book(**b) for b in SEED_BOOKS]
        self.carts = {}
        self.orders = []
        self.tokens = {}
        self._order_counter = 1000

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def find_user_by_email(self, email: str) -> User | None:
        return next((u for u in self.users if u.email == email), None)

    def issue_token(self, user_id: str) -> str:
        ts = int(time.time() * 1000)
        token = f"tok_{user_id}_{ts}"
        self.tokens[token] = user_id
        return token

    def get_user_id_by_token(self, token: str) -> str | None:
        return self.tokens.get(token)

    # ------------------------------------------------------------------
    # Books
    # ------------------------------------------------------------------

    def list_books(
        self,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        category: str | None = None,
        sort: str | None = None,
    ) -> dict[str, Any]:
        items = [b for b in self.books if not b.deleted]

        if search:
            q = search.lower()
            items = [b for b in items if q in b.title.lower() or q in b.author.lower()]

        if category:
            items = [b for b in items if b.category.lower() == category.lower()]

        if sort == "price_asc":
            items = sorted(items, key=lambda b: b.price)
        elif sort == "price_desc":
            items = sorted(items, key=lambda b: b.price, reverse=True)

        total = len(items)
        start = (page - 1) * limit
        end = start + limit
        page_items = items[start:end]

        return {
            "items": [self._book_to_dict(b) for b in page_items],
            "total": total,
            "page": page,
            "limit": limit,
        }

    def get_book(self, book_id: str) -> Book | None:
        return next((b for b in self.books if b.id == book_id and not b.deleted), None)

    def create_book(self, data: dict[str, Any]) -> Book:
        new_id = f"b{len(self.books) + 1}"
        book = Book(id=new_id, **data)
        self.books.append(book)
        return book

    def update_book(self, book_id: str, patch: dict[str, Any]) -> Book | None:
        book = self.get_book(book_id)
        if not book:
            return None
        for key, value in patch.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)
        return book

    def delete_book(self, book_id: str) -> bool:
        book = self.get_book(book_id)
        if not book:
            return False
        book.deleted = True
        return True

    # ------------------------------------------------------------------
    # Cart
    # ------------------------------------------------------------------

    def _get_cart(self, user_id: str) -> list[CartItem]:
        if user_id not in self.carts:
            self.carts[user_id] = []
        return self.carts[user_id]

    def add_to_cart(self, user_id: str, book_id: str, quantity: int) -> dict[str, Any] | str:
        book = self.get_book(book_id)
        if not book:
            return "Book not found"

        cart = self._get_cart(user_id)
        existing = next((item for item in cart if item.book_id == book_id), None)
        current_qty = existing.quantity if existing else 0
        new_qty = current_qty + quantity

        if new_qty > book.stock:
            return f"Insufficient stock. Available: {book.stock}"

        if existing:
            existing.quantity = new_qty
        else:
            cart.append(CartItem(book_id=book_id, quantity=quantity))

        return self.cart_details(user_id)

    def update_cart_item(self, user_id: str, book_id: str, quantity: int) -> dict[str, Any] | str:
        book = self.get_book(book_id)
        if not book:
            return "Book not found"

        cart = self._get_cart(user_id)
        existing = next((item for item in cart if item.book_id == book_id), None)

        if quantity == 0:
            if existing:
                self.carts[user_id] = [i for i in cart if i.book_id != book_id]
            return self.cart_details(user_id)

        if quantity > book.stock:
            return f"Insufficient stock. Available: {book.stock}"

        if existing:
            existing.quantity = quantity
        else:
            cart.append(CartItem(book_id=book_id, quantity=quantity))

        return self.cart_details(user_id)

    def remove_cart_item(self, user_id: str, book_id: str) -> dict[str, Any]:
        if user_id in self.carts:
            self.carts[user_id] = [i for i in self.carts[user_id] if i.book_id != book_id]
        return self.cart_details(user_id)

    def cart_details(self, user_id: str) -> dict[str, Any]:
        cart = self._get_cart(user_id)
        items = []
        for ci in cart:
            book = self.get_book(ci.book_id)
            if book:
                line_total = round(book.price * ci.quantity, 2)
                items.append({
                    "bookId": ci.book_id,
                    "quantity": ci.quantity,
                    "title": book.title,
                    "price": book.price,
                    "lineTotal": line_total,
                })
        subtotal = round(sum(i["lineTotal"] for i in items), 2)
        return {"items": items, "subtotal": subtotal}

    def cart_subtotal(self, user_id: str) -> float:
        return self.cart_details(user_id)["subtotal"]

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def create_order(
        self, user_id: str, shipping: dict[str, Any], payment: dict[str, Any]
    ) -> Order | str:
        cart = self._get_cart(user_id)
        if not cart:
            return "Cart is empty"

        order_items: list[OrderItem] = []
        for ci in cart:
            book = self.get_book(ci.book_id)
            if not book:
                return f"Book {ci.book_id} not found"
            if ci.quantity > book.stock:
                return f"Insufficient stock for '{book.title}'"
            order_items.append(OrderItem(
                book_id=ci.book_id,
                title=book.title,
                quantity=ci.quantity,
                unit_price=book.price,
            ))

        # Decrement stock and clear cart
        for ci in cart:
            book = self.get_book(ci.book_id)
            if book:
                book.stock -= ci.quantity
        self.carts[user_id] = []

        self._order_counter += 1
        order_id = f"ORD-{self._order_counter}"
        total = round(sum(i.unit_price * i.quantity for i in order_items), 2)

        import datetime
        created_at = datetime.datetime.utcnow().isoformat() + "Z"

        order = Order(
            id=order_id,
            user_id=user_id,
            items=order_items,
            shipping=ShippingInfo(**shipping),
            payment=PaymentInfo(**payment),
            status="pending",
            total=total,
            created_at=created_at,
        )
        self.orders.append(order)
        return order

    def transition_order_status(self, user_id: str, order_id: str, status: str) -> Order | str:
        order = self.get_order(order_id, user_id)
        if not order:
            return "Order not found"

        valid_transitions: dict[str, str] = {
            "pending": "confirmed",
            "confirmed": "shipped",
        }

        if order.status not in valid_transitions:
            return f"Cannot transition from status '{order.status}'"

        if valid_transitions[order.status] != status:
            return f"Invalid transition from '{order.status}' to '{status}'"

        order.status = status
        return order

    def get_order(self, order_id: str, user_id: str | None = None) -> Order | None:
        order = next((o for o in self.orders if o.id == order_id), None)
        if not order:
            return None
        if user_id and order.user_id != user_id:
            return None
        return order

    def list_orders(self, user_id: str, page: int = 1, limit: int = 10) -> dict[str, Any]:
        user_orders = [o for o in self.orders if o.user_id == user_id]
        user_orders = sorted(user_orders, key=lambda o: o.created_at, reverse=True)
        total = len(user_orders)
        start = (page - 1) * limit
        end = start + limit
        page_items = user_orders[start:end]
        return {
            "items": [self._order_to_dict(o) for o in page_items],
            "total": total,
            "page": page,
            "limit": limit,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _book_to_dict(self, book: Book) -> dict[str, Any]:
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "price": book.price,
            "stock": book.stock,
        }

    def _order_to_dict(self, order: Order) -> dict[str, Any]:
        return {
            "id": order.id,
            "userId": order.user_id,
            "items": [
                {
                    "bookId": i.book_id,
                    "title": i.title,
                    "quantity": i.quantity,
                    "unitPrice": i.unit_price,
                }
                for i in order.items
            ],
            "shipping": {
                "name": order.shipping.name,
                "address": order.shipping.address,
                "city": order.shipping.city,
                "zip": order.shipping.zip,
            },
            "payment": {
                "cardLast4": order.payment.card_last4,
            },
            "status": order.status,
            "total": order.total,
            "createdAt": order.created_at,
        }


# Global singleton
store = BookstoreStore()
