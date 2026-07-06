"""Locator constants for the cart page."""


class CartLocators:
    CART_ITEMS = '[data-testid="cart-items"]'
    EMPTY_MESSAGE = '[data-testid="empty-cart-message"]'
    SUBTOTAL = '[data-testid="cart-subtotal"]'
    CHECKOUT_LINK = '[data-testid="checkout-link"]'

    @staticmethod
    def cart_item(book_id: str) -> str:
        return f'[data-testid="cart-item-{book_id}"]'

    @staticmethod
    def qty_input(book_id: str) -> str:
        return f'[data-testid="qty-{book_id}"]'

    @staticmethod
    def remove_btn(book_id: str) -> str:
        return f'[data-testid="remove-{book_id}"]'
