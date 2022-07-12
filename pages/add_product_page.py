import logging.config

import allure
from faker import Faker
from selenium.webdriver.common.by import By

from logging_settings import logger_config
from pages.base_page import BasePage

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class AddNewProductPage(BasePage):
    LOCATORS = {
        "save": (By.CSS_SELECTOR, 'button[data-original-title="Save"]'),
        "general": {
            "name": (By.CSS_SELECTOR, '#input-name1'),
            "description": (By.CSS_SELECTOR, 'div.note-editable'),
            "meta": (By.CSS_SELECTOR, '#input-meta-title1'),
            "meta description": (By.CSS_SELECTOR, '#input-meta-description1'),
            "meta keywords": (By.CSS_SELECTOR, '#input-meta-keyword1'),
            "product tags": (By.CSS_SELECTOR, '#input-tag1'),
        },
        "tab": {
            "general": (By.LINK_TEXT, 'General'),
            "data": (By.LINK_TEXT, 'Data'),
            "links": (By.LINK_TEXT, 'Links'),
            "attribute": (By.LINK_TEXT, 'Attribute'),
            "option": (By.LINK_TEXT, 'Option'),
            "recurring": (By.LINK_TEXT, 'Recurring'),
            "discount": (By.LINK_TEXT, 'Discount'),
            "special": (By.LINK_TEXT, 'Discount'),
            "image": (By.LINK_TEXT, 'Image')
        },
        "data": {
            "model": (By.CSS_SELECTOR, '#input-model')
        },
        "error banner": (By.CSS_SELECTOR, '.alert-danger'),
        "page title": (By.CSS_SELECTOR, 'h3.panel-title'),
    }
    ADD_NEW_URL_APPENDIX_PART = "admin/index.php?route=catalog/product/add"
    PAGE_TITLE = "Add Product"
    CREATE_NEW_PRODUCT_ERROR_TEXT = " Warning: Please check the form carefully for errors!"

    @allure.step("Switching to tab '{name}' at the 'Add new product' page configuration")
    def switch_to_tab(self, name):
        self.scroll_to_element(self.LOCATORS["tab"][name])
        self.click(self.LOCATORS["tab"][name])
        LOGGER.debug(f"Switched to tab '{name}'")

    @allure.step("Creating the product with parameters: name='{name}', model='{model}', meta='{meta}'")
    def create_product(self, name=None, model=None, meta=None):
        if name is None:
            f = Faker()
            name = "0" + f.aba()[:3] + f.user_name()
        if model is None:
            model = name + " 3000"
        if meta is None:
            meta = "cucumber"

        LOGGER.debug(f"Creating a product with parameters: name='{name}', model='{model}', meta='{meta}")
        self.fill_field(self.LOCATORS["general"]["name"], name)
        self.fill_field(self.LOCATORS["general"]["meta"], meta)
        self.switch_to_tab("data")
        self.fill_field(self.LOCATORS["data"]["model"], model)

        self.click(self.LOCATORS["save"])
        LOGGER.debug(f"Created the product")

        created_product = {"name": name, "model": model, "meta": meta}
        return created_product
