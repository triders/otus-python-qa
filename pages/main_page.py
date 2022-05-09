from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    LOCATORS = {
        "featured: add to cart buttons": (By.CSS_SELECTOR, ".button-group .fa-shopping-cart"),
        "featured: add to wish list buttons": (By.CSS_SELECTOR, ".button-group .fa-heart"),
        "featured: add to comparison buttons": (By.CSS_SELECTOR, ".button-group .fa-exchange"),
        "alert": (By.CSS_SELECTOR, "div.alert"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_to_cart(self, index):
        add_to_cart_button = self.scroll_to_element(self.LOCATORS["featured: add to cart buttons"])
        add_to_cart_button.click()
