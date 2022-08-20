import logging.config

import allure
from selenium.webdriver.common.by import By

from opencart_ui_tests.logging_settings import logger_config
from opencart_ui_tests.pages.base_page import BasePage

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class AdminProductsPage(BasePage):
    LOCATORS = {
        "add new": (By.CSS_SELECTOR, 'a[data-original-title="Add New"]'),
        "delete": (By.CSS_SELECTOR, 'button[data-original-title="Delete"]'),
        "filter: name": (By.CSS_SELECTOR, '#input-name'),
        "filter: model": (By.CSS_SELECTOR, '#input-model'),
        "filter": (By.CSS_SELECTOR, '#button-filter'),
        "products on page": (By.CSS_SELECTOR, 'td input'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += "/admin/index.php?route=catalog/product"

    @allure.step("Clicking on 'Add new product'")
    def click_add_new_product(self):
        self.click(self.LOCATORS["add new"])
        LOGGER.debug("Clicked on 'Add new product'")

    @allure.step("Finding product with name: '{name}'")
    def get_product_by_name(self, name):
        self.scroll_to_element((By.XPATH, "//*[contains(text(), '{0}')]".format(name)))
        product = self.get_element_if_present((By.XPATH, "//*[contains(text(), '{0}')]".format(name)))
        LOGGER.debug("Product with name: '{name}' has been found")
        return product

    @allure.step("Filtering products list by: product name='{name}' and/or model={model}")
    def filter_products_by(self, name=None, model=None):
        if name:
            self.clear_field(self.LOCATORS["filter: name"])
            self.fill_field(self.LOCATORS["filter: name"], name)
            LOGGER.debug(f"Filtered products list by product name='{name}'")
        if model:
            self.clear_field(self.LOCATORS["filter: model"])
            self.fill_field(self.LOCATORS["filter: model"], model)
            LOGGER.debug(f"Filtered products list by model='{model}'")
        self.click(self.LOCATORS["filter"])
        return self

    @allure.step("Counting products in list on 'Products page'")
    def get_products_number_on_page(self):
        """Generally used to understand how many products left after filter is applied"""
        products = self.get_element_if_present(self.LOCATORS["products on page"])
        products_number = len(products) - 1  # because first item is the "Select all" checkbox
        LOGGER.debug(f"Found {products_number} products in list")
        return products_number

    def filter_and_select_the_exact_product(self, name=None, model=None):
        """First we make sure that there is only ONE product on the page, then -- select it's checkbox."""
        self.filter_products_by(name=name, model=model)
        assert self.get_products_number_on_page() == 1
        select_all_checkbox = self.get_element_if_present(self.LOCATORS["products on page"], only_first=True)
        self.click(select_all_checkbox)
        LOGGER.debug(f"Checked that there is only one product left after filtering, and then -- selected it")

    @allure.step("Deleting selected product")
    def delete_selected_products(self):
        self.click(self.LOCATORS["delete"])
        delete_alert = self.browser.switch_to.alert
        delete_alert.accept()
        LOGGER.debug("Deleted selected product")
