from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):

    LOCATORS = {
        "product name": (By.CSS_SELECTOR, "h1"),
        "product price": (By.CSS_SELECTOR, "li h2"),
    }

    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += "/" + product_id
