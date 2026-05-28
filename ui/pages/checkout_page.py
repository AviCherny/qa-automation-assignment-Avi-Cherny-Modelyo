import allure
from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.zip_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.complete_header = page.locator("[data-test='complete-header']")
        self.item_total = page.locator("[data-test='subtotal-label']")

    @allure.step("Fill checkout info: {first_name} {last_name} {zip_code}")
    def fill_info(self, first_name: str, last_name: str, zip_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_input.fill(zip_code)
        self.continue_button.click()

    @allure.step("Finish order")
    def finish(self) -> None:
        self.finish_button.click()

    def get_confirmation_text(self) -> str:
        return self.complete_header.inner_text()
