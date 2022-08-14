import logging.config

import allure
import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class BasePage:
    BASE_PAGE_LOCATORS = {
        "logo": (By.CSS_SELECTOR, "div#logo"),
        "currency": {
            "current": (By.CSS_SELECTOR, "#form-currency button strong"),
            "dropdown": (By.CSS_SELECTOR, "#form-currency .dropdown-toggle"),
            "USD": (By.CSS_SELECTOR, ".currency-select[name='USD']"),
            "EUR": (By.CSS_SELECTOR, ".currency-select[name='EUR']"),
            "GBP": (By.CSS_SELECTOR, ".currency-select[name='GBP']"),
        },
        "header: contact us": (By.CSS_SELECTOR, "#top-links .fa-phone"),
        "header: login/register dd": (By.CSS_SELECTOR, "#top-links .fa-user"),
        "header: wish list": (By.CSS_SELECTOR, "#top-links .fa-heart"),
        "header: cart": (By.CSS_SELECTOR, "#top-links .fa-shopping-cart"),
        "header: share": (By.CSS_SELECTOR, "#top-links .fa-share"),
        "navbar": (By.CSS_SELECTOR, ".navbar#menu"),
        "navbar items": (By.CSS_SELECTOR, "ul.navbar-nav>li"),
        "cart button": (By.CSS_SELECTOR, "#cart>button"),
        "search input": (By.CSS_SELECTOR, "#search>input"),
        "search button": (By.CSS_SELECTOR, "#search button"),
    }
    TIMEOUT = 3
    CURRENCY_DROPDOWN_STATE = "area-expanded"
    CURRENCY_SIGNS = {"USD": "$", "EUR": "€", "GBP": "£"}

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url = base_url

    def open(self):
        with allure.step(f"Opening page: {self.url}"):
            self.browser.get(self.url)
            LOGGER.debug(f"Opened page: {self.url}")

    @allure.step("Trying to find element(s): {locator}")
    def get_element_if_present(self, locator, only_first=False):
        """Returns the element or elements list if found"""
        elements_list = self.browser.find_elements(*locator)
        if only_first:
            LOGGER.debug(f"Found, and returning only first element: '{locator}' ")
            return elements_list[0]
        else:
            LOGGER.debug(f"Found, and returning elements: '{locator}' ")
            return elements_list

    @allure.step("Clicking on element: {element_or_locator}")
    def click(self, element_or_locator):
        if isinstance(element_or_locator, WebElement):
            element_or_locator.click()
        else:
            self.get_element_if_present(element_or_locator, only_first=True).click()
        LOGGER.debug(f"Clicked on element: '{element_or_locator}' ")

    @allure.step("Filling the field: {locator}, with text: '{text}'")
    def fill_field(self, locator, text):
        self.wait_element(locator).send_keys(text)
        LOGGER.debug(f"Filled the field: {locator}, with text: '{text}'")

    @allure.step("Emptying the field: {locator}")
    def clear_field(self, locator):
        self.wait_element(locator).clear()
        LOGGER.debug(f"Cleared the field: {locator}")

    @allure.step("Scrolling to element: {element_or_locator}")
    def scroll_to_element(self, element_or_locator):
        try:
            if isinstance(element_or_locator, WebElement):
                self.browser.execute_script("arguments[0].scrollIntoView();", element_or_locator)
            else:
                # we expect 'element_or_locator' to be a locator
                self.browser.execute_script("arguments[0].scrollIntoView();",
                                            self.browser.find_element(*element_or_locator))
            LOGGER.debug(f"Scrolled to element: '{element_or_locator}'")
        except NoSuchElementException:
            LOGGER.warning(f"Tried to scroll to element, but didn't find it: '{element_or_locator}' ")
            return False

    @allure.step("Waiting element to be present: {locator} for {timeout} seconds. Returning it if found")
    def wait_element(self, locator, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting element to be present: {locator} for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            LOGGER.warning(f"Failed to find element: {locator}; waited for {timeout} seconds")
            return False

    @allure.step("Waiting element NOT to be present: {locator} for {timeout} seconds")
    def wait_element_not_present(self, locator, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting element NOT to be present: {locator} for {timeout} seconds")
            WebDriverWait(self.browser, timeout).until_not(ec.visibility_of_element_located(locator))
        except TimeoutException:
            LOGGER.warning(f"Didn't expect to find element: {locator}; waited for {timeout} seconds ")
            return False

    @allure.step("Waiting element to be clickable: {locator} for {timeout} seconds. Returning it if found")
    def wait_element_clickable(self, locator, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting element to be clickable: {locator} for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            LOGGER.warning(f"Failed to find CLICKABLE element: {locator}; waited for {timeout} seconds")
            return False

    @allure.step("Waiting alert to be present for {timeout} seconds. Returning it if found")
    def wait_alert(self, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting alert to be present for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until(ec.alert_is_present())
        except TimeoutException:
            LOGGER.warning(f"Didn't find alert; waited for {timeout} seconds")
            return False

    @allure.step("Extracting the text from element: {element_or_locator}")
    def get_element_text(self, element_or_locator):
        if isinstance(element_or_locator, WebElement):
            element_text = element_or_locator.text
        else:
            element_text = self.get_element_if_present(element_or_locator, only_first=True).text
        LOGGER.debug(f"Extracted the text '{element_text}' from the element: {element_or_locator}")
        return element_text

    @allure.step("Getting the current tab name")
    def get_tab_name(self):
        LOGGER.debug(f"Current tab name is '{self.browser.title}'")
        return self.browser.title

    @allure.step("Getting current currency")
    def get_current_currency(self):
        current_currency = self.get_element_text(self.BASE_PAGE_LOCATORS["currency"]["current"])
        LOGGER.debug(f"Current currency is '{current_currency}'")
        return current_currency

    def is_currency_dropdown_opened(self):
        currency_dropdown = self.get_element_if_present(self.BASE_PAGE_LOCATORS["currency"]["dropdown"],
                                                        only_first=True)
        currency_dropdown_state = currency_dropdown.get_attribute(self.CURRENCY_DROPDOWN_STATE)
        LOGGER.debug(f"Currency dropdown is {'' if currency_dropdown_state else 'NOT'} opened")
        return currency_dropdown_state

    @allure.step("Changing currency to {currency}")
    def change_currency_to(self, currency):
        """Change opencart currency to 'USD', 'EUR' or 'GBP'"""
        if not self.is_currency_dropdown_opened():
            self.click(self.BASE_PAGE_LOCATORS["currency"]["dropdown"])
        self.click(self.BASE_PAGE_LOCATORS["currency"][currency.upper()])
        LOGGER.debug(f"Changed currency to {currency}")

    @allure.step("Getting total items count and price from cart")
    def get_cart_item_count_and_total_price(self):
        """Get items number and total cart price from the cart button text (on the top-right)"""
        cart_text = self.get_element_text(BasePage.BASE_PAGE_LOCATORS["cart button"]).strip()  # "2 item(s) - $724.00"
        LOGGER.debug(f"Cart has {cart_text} in total ")
        cart_text_split = cart_text.split(" item(s) - $")
        items_in_cart, total_price = int(cart_text_split[0]), float(cart_text_split[1])
        return items_in_cart, total_price
