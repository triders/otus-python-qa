import allure
from selenium.webdriver.common.by import By
from page_objects_and_tests_for_opencart.pages.base_page import BasePage

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class MainPage(BasePage):
    LOCATORS = {
        "featured: add to cart buttons": (By.CSS_SELECTOR, ".button-group .fa-shopping-cart"),
        "featured: add to wish list buttons": (By.CSS_SELECTOR, ".button-group .fa-heart"),
        "featured: add to comparison buttons": (By.CSS_SELECTOR, ".button-group .fa-exchange"),
        "alert": (By.CSS_SELECTOR, "div.alert"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @allure.step("Adding to cart the featured product #{index} (from left to right)")
    def add_to_cart(self, index=1):
        """Add n-th featured product to cart. Index = 1 (first item) by default"""
        add_to_cart_button = self.get_element_if_present(
            locator=self.LOCATORS["featured: add to cart buttons"])
        self.click(add_to_cart_button[index - 1])
        LOGGER.debug(f"Added to cart the featured product #{index} (from left to right)")
