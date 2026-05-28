import pytest
import allure
from playwright.sync_api import expect

ITEM_NAME = "Sauce Labs Backpack"
CONFIRMATION_TEXT = "Thank you for your order!"


@pytest.mark.ui
@allure.feature("Checkout")
@allure.story("End-to-end checkout")
def test_checkout_flow_completes_with_confirmation(logged_in_inventory):
    logged_in_inventory.add_to_cart(ITEM_NAME)

    cart = logged_in_inventory.go_to_cart()
    checkout = cart.checkout()

    checkout.fill_info("John", "Doe", "12345")
    checkout.finish()

    expect(checkout.complete_header).to_be_visible()
    assert checkout.get_confirmation_text() == CONFIRMATION_TEXT
