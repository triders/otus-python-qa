from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement


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

    def go(self, url):
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def get_element_if_present(self, locator, only_first=None):
        """Returns the element or elements list if found"""
        elements_list = self.browser.find_elements(*locator)
        return elements_list[0] if only_first else elements_list

    def click(self, element_or_locator):
        if isinstance(element_or_locator, WebElement):
            element_or_locator.click()
        else:
            self.get_element_if_present(element_or_locator, only_first=True).click()

    def fill_field(self, locator, text):
        self.wait_element(locator).send_keys(text)

    def clear_field(self, locator):
        self.wait_element(locator).clear()

    def scroll_to_element(self, element_or_locator):
        try:
            if isinstance(element_or_locator, WebElement):
                self.browser.execute_script("arguments[0].scrollIntoView();", element_or_locator)
            else:
                # we expect 'element_or_locator' to be a locator
                self.browser.execute_script("arguments[0].scrollIntoView();",
                                            self.browser.find_element(*element_or_locator))
        except NoSuchElementException:
            return False

    def wait_element(self, locator, timeout=TIMEOUT):
        try:
            return WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            return False

    def wait_element_not_present(self, locator, timeout=TIMEOUT):
        try:
            return WebDriverWait(self.browser, timeout).until_not(ec.visibility_of_element_located(locator))
        except TimeoutException:
            return False

    def wait_element_clickable(self, locator, timeout=TIMEOUT):
        try:
            return WebDriverWait(self.browser, timeout).until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            return False

    def wait_alert(self, timeout=TIMEOUT):
        try:
            return WebDriverWait(self.browser, timeout).until(ec.alert_is_present())
        except TimeoutException:
            return False

    def get_element_text(self, element_or_locator):
        if isinstance(element_or_locator, WebElement):
            return element_or_locator.text
        else:
            return self.get_element_if_present(element_or_locator, only_first=True).text

    def get_tab_name(self):
        return self.browser.title

    def get_current_currency(self):
        return self.get_element_text(self.BASE_PAGE_LOCATORS["currency"]["current"])

    def is_currency_dropdown_opened(self):
        currency_dropdown = self.get_element_if_present(self.BASE_PAGE_LOCATORS["currency"]["dropdown"],
                                                        only_first=True)
        return currency_dropdown.get_attribute(self.CURRENCY_DROPDOWN_STATE)

    def change_currency_to(self, currency):
        if not self.is_currency_dropdown_opened():
            self.click(self.BASE_PAGE_LOCATORS["currency"]["dropdown"])
        if currency.upper() == "USD":
            self.click(self.BASE_PAGE_LOCATORS["currency"]["USD"])
        elif currency.upper() == "EUR":
            self.click(self.BASE_PAGE_LOCATORS["currency"]["EUR"])
        elif currency.upper() == "GBP":
            self.click(self.BASE_PAGE_LOCATORS["currency"]["GBP"])
        else:
            raise ValueError("Please, select currency: 'USD', 'EUR' or 'GBP'")

    def get_cart_item_count_and_total_price(self):
        """Get items number and total cart price from the cart button text (on the top-right)"""
        cart_text = self.get_element_text(BasePage.BASE_PAGE_LOCATORS["cart button"]).strip()  # "2 item(s) - $724.00"
        cart_text_split = cart_text.split(" item(s) - $")
        items_in_cart, total_price = int(cart_text_split[0]), float(cart_text_split[1])
        return items_in_cart, total_price
