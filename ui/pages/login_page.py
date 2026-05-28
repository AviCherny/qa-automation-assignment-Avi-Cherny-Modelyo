import allure
from playwright.sync_api import Page
from config import UI_BASE_URL
from ui.pages.base_page import BasePage
from ui.pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    @allure.step("Open login page")
    def open(self) -> None:
        self.navigate_to(UI_BASE_URL)

    @allure.step("Login as {username}")
    def login(self, username: str, password: str) -> "InventoryPage":
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)

    @allure.step("Login with invalid credentials")
    def login_expecting_error(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        return self.error_message.inner_text()
