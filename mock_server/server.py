"""FastAPI mock server for the bookstore application."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles

from mock_server.store import Book, Order, store

app = FastAPI(title="Bookstore Mock Server")

DEMO_DIR = Path(__file__).parent.parent / "demo"


# ------------------------------------------------------------------
# Auth helpers
# ------------------------------------------------------------------

def get_token(request: Request) -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return None


def require_auth(request: Request) -> str:
    token = get_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user_id = store.get_user_id_by_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# ------------------------------------------------------------------
# Test helpers
# ------------------------------------------------------------------

@app.post("/api/test/reset", status_code=204)
def reset_store() -> Response:
    store.reset()
    return Response(status_code=204)


# ------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------

@app.post("/api/auth/login")
def login(body: dict[str, Any]) -> dict[str, Any]:
    email = body.get("email", "")
    password = body.get("password", "")

    user = store.find_user_by_email(email)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = store.issue_token(user.id)
    return {
        "token": token,
        "user": {"id": user.id, "email": user.email, "name": user.name},
    }


# ------------------------------------------------------------------
# Books
# ------------------------------------------------------------------

@app.get("/api/books")
def list_books(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    category: str | None = None,
    sort: str | None = None,
) -> dict[str, Any]:
    return store.list_books(page=page, limit=limit, search=search, category=category, sort=sort)


@app.get("/api/books/{book_id}")
def get_book(book_id: str) -> dict[str, Any]:
    book = store.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return store._book_to_dict(book)


@app.post("/api/books", status_code=201)
def create_book(
    body: dict[str, Any],
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    required = ["title", "author", "category", "price", "stock"]
    for f in required:
        if f not in body:
            raise HTTPException(status_code=400, detail=f"Missing field: {f}")
    data = {
        "title": body["title"],
        "author": body["author"],
        "category": body["category"],
        "price": float(body["price"]),
        "stock": int(body["stock"]),
    }
    book = store.create_book(data)
    return store._book_to_dict(book)


@app.put("/api/books/{book_id}")
def update_book(
    book_id: str,
    body: dict[str, Any],
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    patch: dict[str, Any] = {}
    for key in ["title", "author", "category", "price", "stock"]:
        if key in body:
            patch[key] = body[key]
    book = store.update_book(book_id, patch)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return store._book_to_dict(book)


@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(
    book_id: str,
    user_id: str = Depends(require_auth),
) -> Response:
    ok = store.delete_book(book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=204)


# ------------------------------------------------------------------
# Cart
# ------------------------------------------------------------------

@app.get("/api/cart")
def get_cart(user_id: str = Depends(require_auth)) -> dict[str, Any]:
    return store.cart_details(user_id)


@app.post("/api/cart/items", status_code=201)
def add_cart_item(
    body: dict[str, Any],
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    book_id = body.get("bookId", "")
    quantity = int(body.get("quantity", 1))
    result = store.add_to_cart(user_id, book_id, quantity)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result


@app.patch("/api/cart/items/{book_id}")
def update_cart_item(
    book_id: str,
    body: dict[str, Any],
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    quantity = int(body.get("quantity", 0))
    result = store.update_cart_item(user_id, book_id, quantity)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result


@app.delete("/api/cart/items/{book_id}")
def remove_cart_item(
    book_id: str,
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    return store.remove_cart_item(user_id, book_id)


# ------------------------------------------------------------------
# Orders
# ------------------------------------------------------------------

@app.post("/api/orders", status_code=201)
def create_order(
    body: dict[str, Any],
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    shipping = body.get("shipping")
    payment = body.get("payment")
    if not shipping or not payment:
        raise HTTPException(status_code=400, detail="Missing shipping or payment info")

    # Normalise camelCase -> snake_case for payment
    if "cardLast4" in payment and "card_last4" not in payment:
        payment = {"card_last4": payment["cardLast4"]}

    result = store.create_order(user_id, shipping, payment)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return store._order_to_dict(result)


@app.get("/api/orders")
def list_orders(
    page: int = 1,
    limit: int = 10,
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    return store.list_orders(user_id, page=page, limit=limit)


@app.get("/api/orders/{order_id}")
def get_order(
    order_id: str,
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    order = store.get_order(order_id, user_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return store._order_to_dict(order)


@app.patch("/api/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    body: dict[str, Any],
    user_id: str = Depends(require_auth),
) -> dict[str, Any]:
    status = body.get("status", "")
    result = store.transition_order_status(user_id, order_id, status)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return store._order_to_dict(result)


# ------------------------------------------------------------------
# Static files (must be last)
# ------------------------------------------------------------------

if DEMO_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DEMO_DIR), html=True), name="static")
