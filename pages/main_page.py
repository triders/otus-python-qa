from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):

    LOCATORS = {
        "featured: add to cart buttons": (By.CSS_SELECTOR, ".button-group .fa-shopping-cart"),
        "featured: add to wish list buttons": (By.CSS_SELECTOR, ".button-group .fa-heart"),
        "featured: add to comparison buttons": (By.CSS_SELECTOR, ".button-group .fa-exchange"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
