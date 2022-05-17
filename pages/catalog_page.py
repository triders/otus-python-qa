from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CatalogPage(BasePage):

    LOCATORS = {
        "catalog page title": (By.CSS_SELECTOR, "h2"),
        "products on page": (By.CSS_SELECTOR, ".product-layout"),
        "products on page list": (By.CSS_SELECTOR, ".product-layout.product-list"),
        "products on page grid": (By.CSS_SELECTOR, ".product-layout.product-grid"),
        "no products in category": (By.CSS_SELECTOR, "div#content>p"),
        "no products in category > continue button": (By.CSS_SELECTOR, ".buttons .pull-right"),
        "grid view button": (By.CSS_SELECTOR, "#grid-view"),
        "list view button": (By.CSS_SELECTOR, "#list-view"),
    }
    NO_PRODUCTS_MESSAGE = "There are no products to list in this category."

    def __init__(self, catalog_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += catalog_id
