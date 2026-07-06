"""Allure metadata helpers."""

import allure


class Owner:
    BOOKSTORE = "bookstore-qa"


class AllureLayer:
    UI = "UI"
    API = "API"


def tms_link(case_id: str) -> str:
    """TestRail / traceability prefix for test titles."""
    return f"@TmsLink:{case_id}"


def allure_metadata(*, layer: str, suite: str, owner: str = Owner.BOOKSTORE) -> None:
    """Apply Allure labels for Suites (layer → suite) and owner."""
    allure.dynamic.parent_suite(layer)  # type: ignore[no-untyped-call]
    allure.dynamic.suite(suite)  # type: ignore[no-untyped-call]
    allure.dynamic.label("owner", owner)  # type: ignore[no-untyped-call]
