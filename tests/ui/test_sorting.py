import pytest
import allure
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.mark.ui
@allure.feature("Inventory")
@allure.story("Sort products by price low to high")
def test_sort_price_low_to_high(page):
    login = LoginPage(page)
    login.open()
    inventory = login.login(STANDARD_USER, PASSWORD)

    inventory.sort_by("lohi")

    prices = inventory.get_item_prices()
    assert prices == sorted(prices), f"Prices not sorted ascending: {prices}"


@pytest.mark.ui
@allure.feature("Cart")
@allure.story("Cart badge updates on add and remove")
def test_cart_badge_updates_on_add_and_remove(page):
    login = LoginPage(page)
    login.open()
    inventory = login.login(STANDARD_USER, PASSWORD)

    item_name = "Sauce Labs Backpack"

    inventory.add_to_cart(item_name)
    assert inventory.get_cart_badge_count() == 1

    inventory.remove_from_cart(item_name)
    expect(inventory.cart_badge).not_to_be_visible()
