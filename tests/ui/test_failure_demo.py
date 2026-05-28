import allure
import pytest
from playwright.sync_api import expect

BACKPACK_NAME = "Sauce Labs Backpack"
EXPECTED_PRICE = 1.00   # Wrong on purpose — actual price is $29.99


@pytest.mark.xfail(reason="Intentional failure to demo Allure failure artifacts", strict=True)
@pytest.mark.ui
@allure.feature("Inventory")
@allure.story("Product pricing")
@allure.title("Backpack price should be $1.00 [INTENTIONAL FAILURE — artifact demo]")
def test_backpack_price_is_discounted(logged_in_inventory):
    """
    Intentionally failing test to demonstrate Allure failure artifacts:
    screenshot, video, and Playwright trace are all attached on failure.

    The assertion is wrong by design — the backpack costs $29.99, not $1.00.
    """
    expect(logged_in_inventory.inventory_list).to_be_visible()

    prices = logged_in_inventory.get_item_prices()
    actual_price = prices[0]

    assert actual_price == EXPECTED_PRICE, (
        f"Expected '{BACKPACK_NAME}' to cost ${EXPECTED_PRICE:.2f} "
        f"but got ${actual_price:.2f}"
    )
