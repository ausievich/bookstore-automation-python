"""Allure metadata helpers."""

import allure


class Owner:
    BOOKSTORE = "bookstore-qa"


def allure_metadata(layer: str, owner: str = Owner.BOOKSTORE) -> None:
    """Attach layer and owner labels to the current Allure test."""
    allure.dynamic.label("layer", layer)  # type: ignore[no-untyped-call]
    allure.dynamic.label("owner", owner)  # type: ignore[no-untyped-call]
