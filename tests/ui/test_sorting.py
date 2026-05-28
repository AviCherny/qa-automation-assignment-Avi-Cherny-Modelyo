import pytest
import allure
from playwright.sync_api import expect


@pytest.mark.ui
@allure.feature("Inventory")
@allure.story("Sort products by price low to high")
def test_sort_price_low_to_high(logged_in_inventory):
    logged_in_inventory.sort_by("lohi")

    prices = logged_in_inventory.get_item_prices()
    assert prices == sorted(prices), f"Prices not sorted ascending: {prices}"


@pytest.mark.ui
@allure.feature("Cart")
@allure.story("Cart badge updates on add and remove")
def test_cart_badge_updates_on_add_and_remove(logged_in_inventory):
    item_name = "Sauce Labs Backpack"

    logged_in_inventory.add_to_cart(item_name)
    assert logged_in_inventory.get_cart_badge_count() == 1

    logged_in_inventory.remove_from_cart(item_name)
    expect(logged_in_inventory.cart_badge).not_to_be_visible()
