import pytest
import allure
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"
INVALID_PASSWORD = "wrong_password"
EXPECTED_ERROR = "Epic sadface: Username and password do not match any user in this service"


@pytest.mark.ui
@allure.feature("Login")
@allure.story("Happy path")
def test_login_standard_user_lands_on_inventory(page):
    login = LoginPage(page)
    login.open()

    inventory = login.login(STANDARD_USER, PASSWORD)

    expect(page).to_have_url("**/inventory.html")
    expect(inventory.inventory_list).to_be_visible()
    assert inventory.inventory_items.count() > 0


@pytest.mark.ui
@allure.feature("Login")
@allure.story("Invalid credentials")
def test_login_invalid_credentials_shows_error(page):
    login = LoginPage(page)
    login.open()

    login.login_expecting_error(STANDARD_USER, INVALID_PASSWORD)

    expect(login.error_message).to_be_visible()
    assert EXPECTED_ERROR in login.get_error_message()
