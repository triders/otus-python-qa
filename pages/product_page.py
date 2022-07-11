import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class ProductPage(BasePage):
    LOCATORS = {
        "product name": (By.CSS_SELECTOR, "h1"),
        "product name in breadcrumb navigation": (By.CSS_SELECTOR, "ul.breadcrumb li:last-child"),
        "product description": (By.CSS_SELECTOR, "div#tab-description"),
        "product price": (By.CSS_SELECTOR, "li h2"),
        "product main image": (By.CSS_SELECTOR, "#content li:not(.image-additional) .thumbnail"),
        "product additional images": (By.CSS_SELECTOR, "#content .image-additional"),
        "add to cart required fields": (By.CSS_SELECTOR, "#product .form-group.required"),
        "add to wish list": (By.CSS_SELECTOR, ".btn-group .fa-heart"),
        "add to comparison": (By.CSS_SELECTOR, ".btn-group .fa-exchange"),
    }

    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += product_id

    @allure.step("Getting the product's price")
    def get_product_price(self, currency="$"):
        """Returns the products price. Currently, works only when currency is $"""
        if currency == "$":
            #  example is "$122.00"
            product_price = float(self.get_element_text(self.LOCATORS["product price"])[1:])
            LOGGER.debug(f"Found that the price of the product is ${product_price}")
            return product_price
