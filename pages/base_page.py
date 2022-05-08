from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


class BasePage:

    LOCATORS = {
        "logo": (By.CSS_SELECTOR, "div#logo"),
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

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url = base_url

    def go(self, url):
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, locator):
        """Returns element or elements list if found"""
        elements_list = self.browser.find_elements(*locator)
        return elements_list[0] if len(elements_list) == 1 else elements_list

    def click(self, locator):
        self.is_element_present(locator).click()

    def wait_element(self, locator, timeout=3):
        try:
            return WebDriverWait(self.browser, timeout).until(ec.visibility_of_all_elements_located(locator))
        except TimeoutException:
            raise NoSuchElementException(
                f"Unable to find element with locator '{locator}' in a given timeout: '{timeout}'")

    def wait_element_clickable(self, locator, timeout=3):
        try:
            return WebDriverWait(self.browser, timeout).until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            raise NoSuchElementException(
                f"Unable to find clickable element with locator '{locator}' in a given timeout: '{timeout}'")

    def get_element_text(self, locator):
        return self.is_element_present(locator).text

    def get_tab_name(self):
        return self.browser.title
