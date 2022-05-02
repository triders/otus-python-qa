from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec


class BasePage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url = base_url

    def go(self, url):
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, locator):
        try:
            return self.browser.find_element(*locator)
        except NoSuchElementException:
            return False

    def wait_element(self, locator, timeout=3):
        try:
            return WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            assert self.is_element_present(locator), \
                f"Unable to find element with locator '{locator}' in a given timeout: '{timeout}'"

    def get_element_text(self, locator):
        return self.is_element_present(locator).text
