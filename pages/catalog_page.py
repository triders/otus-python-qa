from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):

    LOCATORS = {
        "catalog page title": (By.CSS_SELECTOR, "h2")
    }

    def __init__(self, catalog_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += "/" + catalog_id
