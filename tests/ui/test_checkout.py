import pytest
import allure
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"
ITEM_NAME = "Sauce Labs Backpack"
CONFIRMATION_TEXT = "Thank you for your order!"


@pytest.mark.ui
@allure.feature("Checkout")
@allure.story("End-to-end checkout")
def test_checkout_flow_completes_with_confirmation(page):
    login = LoginPage(page)
    login.open()
    inventory = login.login(STANDARD_USER, PASSWORD)
    inventory.add_to_cart(ITEM_NAME)

    cart = inventory.go_to_cart()
    checkout = cart.checkout()

    checkout.fill_info("John", "Doe", "12345")
    checkout.finish()

    expect(checkout.complete_header).to_be_visible()
    assert checkout.get_confirmation_text() == CONFIRMATION_TEXT
