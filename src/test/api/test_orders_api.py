"""API tests: Orders."""

import allure

from src.main.api.controllers.cart_controller import CartController
from src.main.api.controllers.orders_controller import OrdersController
from src.main.api.models.order import PaymentInfo, ShippingInfo
from src.main.common.annotations import allure_metadata

SHIPPING = ShippingInfo(name="Test User", address="123 Main St", city="Testville", zip="12345")
PAYMENT = PaymentInfo(card_last4="4242")


def _setup_cart(cart_api: CartController) -> None:
    cart_api.add_item("b3", 1)


@allure.feature("Orders API")
class TestOrdersApi:
    def setup_method(self) -> None:
        allure_metadata("API")

    def test_create_order(
        self, cart_api: CartController, orders_api: OrdersController, auth_token: str
    ) -> None:
        with allure.step("Add item to cart"):
            _setup_cart(cart_api)

        with allure.step("Create order"):
            order = orders_api.create(SHIPPING, PAYMENT)

        with allure.step("Assert order created"):
            assert order.id.startswith("ORD-")
            assert order.status == "pending"
            assert order.total > 0
            assert len(order.items) == 1

    def test_list_orders(
        self, cart_api: CartController, orders_api: OrdersController, auth_token: str
    ) -> None:
        with allure.step("Create two orders"):
            _setup_cart(cart_api)
            orders_api.create(SHIPPING, PAYMENT)
            cart_api.add_item("b4", 1)
            orders_api.create(SHIPPING, PAYMENT)

        with allure.step("List orders"):
            page = orders_api.list()

        with allure.step("Assert 2 orders returned"):
            assert page.total == 2
            assert len(page.items) == 2

    def test_get_order_by_id(
        self, cart_api: CartController, orders_api: OrdersController, auth_token: str
    ) -> None:
        with allure.step("Create order"):
            _setup_cart(cart_api)
            created = orders_api.create(SHIPPING, PAYMENT)

        with allure.step("Get order by id"):
            fetched = orders_api.get_by_id(created.id)

        with allure.step("Assert correct order returned"):
            assert fetched.id == created.id
            assert fetched.status == "pending"

    def test_update_order_status(
        self, cart_api: CartController, orders_api: OrdersController, auth_token: str
    ) -> None:
        with allure.step("Create order"):
            _setup_cart(cart_api)
            order = orders_api.create(SHIPPING, PAYMENT)

        with allure.step("Transition to confirmed"):
            updated = orders_api.update_status(order.id, "confirmed")

        with allure.step("Assert status is confirmed"):
            assert updated.status == "confirmed"

        with allure.step("Transition to shipped"):
            shipped = orders_api.update_status(order.id, "shipped")
            assert shipped.status == "shipped"
