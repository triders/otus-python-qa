from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):

    LOCATORS = {
        "product_name": (By.CSS_SELECTOR, "h1")
    }

    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += "/" + product_id
