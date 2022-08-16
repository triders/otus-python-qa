from faker import Faker
from selenium.webdriver.common.by import By
from opencart_ui_tests.pages.base_page import BasePage

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


EXAMPLE_USER = {
    "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com",
    "telephone": "+123456", "password": "qwerty", "password_confirm": "qwerty"
}


class RegisterPage(BasePage):
    LOCATORS = {
        "first name": (By.CSS_SELECTOR, "#input-firstname"),
        "last name": (By.CSS_SELECTOR, "#input-lastname"),
        "email": (By.CSS_SELECTOR, "#input-email"),
        "telephone": (By.CSS_SELECTOR, "#input-telephone"),
        "password": (By.CSS_SELECTOR, "#input-password"),
        "password confirm": (By.CSS_SELECTOR, "#input-confirm"),
        "newsletter: yes": (By.CSS_SELECTOR, "[name=newsletter][value=1]"),
        "newsletter: no": (By.CSS_SELECTOR, "[name=newsletter][value=0]"),
        "agree to privacy policy checkbox": (By.CSS_SELECTOR, "[name=agree]"),
        "continue": (By.CSS_SELECTOR, "[value=Continue]"),
        "success message title": (By.CSS_SELECTOR, "#content h1"),
        "error banner": (By.CSS_SELECTOR, ".alert-danger"),
        "login link": (By.CSS_SELECTOR, "#content>p>a"),
    }
    SUCCESS_REGISTRATION_URL_APPENDIX = "index.php?route=account/success"
    LOGIN_URL_APPENDIX = "index.php?route=account/login"
    ERROR_TEXT_POLICY = "Warning: You must agree to the Privacy Policy!"

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url += "index.php?route=account/register"

    def fill_field_register_page(self, first_name=None, last_name=None, email=None, telephone=None, password=None,
                                 password_confirm=None):
        if first_name:
            super().fill_field(self.LOCATORS["first name"], first_name)
        if last_name:
            super().fill_field(self.LOCATORS["last name"], last_name)
        if email:
            super().fill_field(self.LOCATORS["email"], email)
        if telephone:
            super().fill_field(self.LOCATORS["telephone"], telephone)
        if password:
            super().fill_field(self.LOCATORS["password"], password)
        if password_confirm:
            super().fill_field(self.LOCATORS["password confirm"], password_confirm)

    def generate_user(self):
        f = Faker()
        password = f.password()
        generated_user = {
            "first_name": f.first_name(), "last_name": f.last_name(), "email": f.email(),
            "telephone": f.phone_number(), "password": password, "password_confirm": password
        }
        LOGGER.debug(f"Generated user with data: {generated_user}")
        return generated_user
