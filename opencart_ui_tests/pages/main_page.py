import allure
from selenium.webdriver.common.by import By
from opencart_ui_tests.pages.base_page import BasePage

import logging.config
from opencart_ui_tests.logging_settings import logger_config

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

    @allure.step("Adding #{index} 'featured product' to cart (by index, in order from left to right)")
    def add_to_cart(self, index=1):
        """Add n-th featured product to cart"""
        add_to_cart_button = self.get_element_if_present(
            locator=self.LOCATORS["featured: add to cart buttons"])
        self.click(add_to_cart_button[index - 1])
        LOGGER.debug(f"Added #{index} 'featured product' to cart (by index, in order from left to right)")
