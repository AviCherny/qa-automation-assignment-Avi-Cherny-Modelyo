import allure
from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_list = page.locator("[data-test='inventory-list']")
        self.inventory_items = page.locator("[data-test='inventory-item']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")

    @allure.step("Add item '{item_name}' to cart")
    def add_to_cart(self, item_name: str) -> None:
        item = self.page.locator(f"[data-test='inventory-item']").filter(has_text=item_name)
        item.locator("[data-test^='add-to-cart']").click()

    @allure.step("Get cart badge count")
    def get_cart_badge_count(self) -> int:
        return int(self.cart_badge.inner_text())

    @allure.step("Go to cart")
    def go_to_cart(self) -> "CartPage":
        from ui.pages.cart_page import CartPage
        self.cart_link.click()
        return CartPage(self.page)

    @allure.step("Sort products by '{option}'")
    def sort_by(self, option: str) -> None:
        self.sort_dropdown.select_option(option)

    @allure.step("Remove item '{item_name}' from cart")
    def remove_from_cart(self, item_name: str) -> None:
        item = self.page.locator("[data-test='inventory-item']").filter(has_text=item_name)
        item.locator("[data-test^='remove']").click()

    def get_item_prices(self) -> list[float]:
        prices = self.page.locator("[data-test='inventory-item-price']").all_inner_texts()
        return [float(p.replace("$", "")) for p in prices]
