from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    LOCATORS = {
        "open catalog": (By.CSS_SELECTOR, "#menu-catalog>a"),
        "catalog: products": (By.LINK_TEXT, "Products"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def go_to_products(self):
        open_catalog_button = self.wait_element(self.LOCATORS["open catalog"])
        open_catalog_button.click()
        open_products_button = self.wait_element(self.LOCATORS["catalog: products"])
        open_products_button.click()
