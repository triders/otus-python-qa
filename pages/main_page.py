from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):

    LOCATORS = {
        "logo": (By.CSS_SELECTOR, "div#logo"),
        "navbar": (By.CSS_SELECTOR, ".navbar#menu"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
