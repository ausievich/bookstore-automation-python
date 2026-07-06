"""API tests: Cart."""

import allure

from src.main.api.controllers.books_controller import BooksController
from src.main.api.controllers.cart_controller import CartController
from src.main.common.annotations import allure_metadata


@allure.feature("Cart API")
class TestCartApi:
    def setup_method(self) -> None:
        allure_metadata("API")

    def test_add_item_to_cart(
        self, cart_api: CartController, books_api: BooksController, auth_token: str
    ) -> None:
        with allure.step("Add book b1 to cart"):
            cart = cart_api.add_item("b1", 1)

        with allure.step("Assert item in cart"):
            assert len(cart.items) == 1
            assert cart.items[0].book_id == "b1"
            assert cart.items[0].quantity == 1

    def test_get_cart(self, cart_api: CartController, auth_token: str) -> None:
        with allure.step("Add items to cart"):
            cart_api.add_item("b1", 2)
            cart_api.add_item("b3", 1)

        with allure.step("Get cart"):
            cart = cart_api.get()

        with allure.step("Assert cart has 2 items"):
            assert len(cart.items) == 2
            assert cart.subtotal > 0

    def test_update_cart_item_quantity(self, cart_api: CartController, auth_token: str) -> None:
        with allure.step("Add book b3 to cart"):
            cart_api.add_item("b3", 1)

        with allure.step("Update quantity to 3"):
            cart = cart_api.update_item("b3", 3)

        with allure.step("Assert quantity updated"):
            item = next(i for i in cart.items if i.book_id == "b3")
            assert item.quantity == 3

    def test_remove_cart_item(self, cart_api: CartController, auth_token: str) -> None:
        with allure.step("Add books to cart"):
            cart_api.add_item("b1", 1)
            cart_api.add_item("b3", 1)

        with allure.step("Remove b1"):
            cart = cart_api.remove_item("b1")

        with allure.step("Assert only b3 remains"):
            assert len(cart.items) == 1
            assert cart.items[0].book_id == "b3"

    def test_add_item_exceeding_stock_returns_400(
        self, cart_api: CartController, auth_token: str
    ) -> None:
        with allure.step("Attempt to add 999 copies of b1 (stock=10)"):
            response = cart_api.client.post(
                "/api/cart/items",
                json={"bookId": "b1", "quantity": 999},
            )

        with allure.step("Assert 400 Bad Request"):
            assert response.status_code == 400
