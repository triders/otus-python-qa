import allure
from selenium.webdriver.common.by import By
from opencart_ui_tests.pages.base_page import BasePage

import logging.config
from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class AdminDashboardPage(BasePage):
    LOCATORS = {
        "open catalog": (By.CSS_SELECTOR, "#menu-catalog>a"),
        "catalog: products": (By.LINK_TEXT, "Products"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @allure.step("Go from 'Dashboard' to 'Products'")
    def go_to_products(self):
        LOGGER.debug("Going from 'Dashboard' to 'Products'")
        open_catalog_button = self.wait_element(self.LOCATORS["open catalog"])
        open_catalog_button.click()
        open_products_button = self.wait_element(self.LOCATORS["catalog: products"])
        open_products_button.click()
