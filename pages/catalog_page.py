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
        "add to cart buttons": (By.CSS_SELECTOR, ".button-group .fa-shopping-cart"),
        "add to wish list buttons": (By.CSS_SELECTOR, ".button-group .fa-heart"),
        "add to comparison buttons": (By.CSS_SELECTOR, ".button-group .fa-exchange"),
        "alert": (By.CSS_SELECTOR, "div.alert"),
    }
    NO_PRODUCTS_MESSAGE = "There are no products to list in this category."

    def __init__(self, catalog_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += catalog_id

    def add_to_cart(self, index=0):
        """Add n-th featured product to cart. Adding first item by default"""
        add_to_cart_button = self.get_element_if_present(
            locator=self.LOCATORS["add to cart buttons"])
        self.click(add_to_cart_button[index])
