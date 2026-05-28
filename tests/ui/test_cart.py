import pytest
import allure

ITEMS = [
    {"name": "Sauce Labs Backpack", "price": "$29.99"},
    {"name": "Sauce Labs Bike Light", "price": "$9.99"},
]


@pytest.mark.ui
@allure.feature("Cart")
@allure.story("Add to cart and verify state")
def test_add_two_items_updates_badge_and_cart_contents(logged_in_inventory):
    for item in ITEMS:
        logged_in_inventory.add_to_cart(item["name"])

    assert logged_in_inventory.get_cart_badge_count() == len(ITEMS)

    cart = logged_in_inventory.go_to_cart()
    cart_names = cart.get_item_names()
    cart_prices = cart.get_item_prices()

    for item in ITEMS:
        assert item["name"] in cart_names
        assert item["price"] in cart_prices
