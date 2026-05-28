import allure
from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator("[data-test='cart-item']")
        self.checkout_button = page.locator("[data-test='checkout']")

    @allure.step("Get cart item names")
    def get_item_names(self) -> list[str]:
        return self.page.locator("[data-test='inventory-item-name']").all_inner_texts()

    @allure.step("Get cart item prices")
    def get_item_prices(self) -> list[str]:
        return self.page.locator("[data-test='inventory-item-price']").all_inner_texts()

    @allure.step("Proceed to checkout")
    def checkout(self) -> "CheckoutPage":
        from ui.pages.checkout_page import CheckoutPage
        self.checkout_button.click()
        return CheckoutPage(self.page)
