import allure
import pytest
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"
BACKPACK_NAME = "Sauce Labs Backpack"
EXPECTED_PRICE = 1.00   # Wrong on purpose — actual price is $29.99


@pytest.mark.xfail(reason="Intentional failure to demo Allure failure artifacts", strict=True)
@pytest.mark.ui
@allure.feature("Inventory")
@allure.story("Product pricing")
@allure.title("Backpack price should be $1.00 [INTENTIONAL FAILURE — artifact demo]")
def test_backpack_price_is_discounted(page):
    """
    Intentionally failing test to demonstrate Allure failure artifacts:
    screenshot, video, and Playwright trace are all attached on failure.

    The assertion is wrong by design — the backpack costs $29.99, not $1.00.
    """
    login = LoginPage(page)

    with allure.step("Open login page and sign in"):
        login.open()
        inventory = login.login(STANDARD_USER, PASSWORD)

    with allure.step("Verify inventory list is visible"):
        expect(inventory.inventory_list).to_be_visible()

    with allure.step(f"Get price of '{BACKPACK_NAME}'"):
        prices = inventory.get_item_prices()
        actual_price = prices[0]
        allure.attach(
            f"All prices on page: {prices}",
            name="prices_snapshot",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"Assert '{BACKPACK_NAME}' costs ${EXPECTED_PRICE:.2f}"):
        assert actual_price == EXPECTED_PRICE, (
            f"Expected '{BACKPACK_NAME}' to cost ${EXPECTED_PRICE:.2f} "
            f"but got ${actual_price:.2f}"
        )
