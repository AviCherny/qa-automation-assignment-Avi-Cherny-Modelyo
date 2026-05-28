import pytest
import allure
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"

ITEMS = [
    {"name": "Sauce Labs Backpack", "price": "$29.99"},
    {"name": "Sauce Labs Bike Light", "price": "$9.99"},
]


@pytest.mark.ui
@allure.feature("Cart")
@allure.story("Add to cart and verify state")
def test_add_two_items_updates_badge_and_cart_contents(page):
    login = LoginPage(page)
    login.open()
    inventory = login.login(STANDARD_USER, PASSWORD)

    for item in ITEMS:
        inventory.add_to_cart(item["name"])

    assert inventory.get_cart_badge_count() == len(ITEMS)

    cart = inventory.go_to_cart()
    cart_names = cart.get_item_names()
    cart_prices = cart.get_item_prices()

    for item in ITEMS:
        assert item["name"] in cart_names
        assert item["price"] in cart_prices
