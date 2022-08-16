from opencart_ui_tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AdminLoginPage(BasePage):

    LOCATORS = {
        "username": (By.CSS_SELECTOR, "#input-username"),
        "password": (By.CSS_SELECTOR, "#input-password"),
        "login button": (By.CSS_SELECTOR, "[type=submit]"),
        "forgotten password": (By.CSS_SELECTOR, ".help-block a"),
        "logo": (By.CSS_SELECTOR, "#header-logo a"),
        "page title": (By.CSS_SELECTOR, "h1"),
        "error banner": (By.CSS_SELECTOR, ".alert-danger"),
        "close error banner button": (By.CSS_SELECTOR, "button.close"),
        "email": (By.CSS_SELECTOR, "#input-email"),
    }

    LOGGED_IN_URL_APPENDIX_PART = "admin/index.php?route=common/dashboard"
    FORGOTTEN_PASSWORD_URL_APPENDIX = "admin/index.php?route=common/forgotten"
    PAGE_TITLE = "Please enter your login details."
    NO_SUCH_USER_ERROR = "No match for Username and/or Password."

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url += "admin"

    def fill_field_login_page(self, username=None, password=None):
        if username:
            super().fill_field(self.LOCATORS["username"], username)
        if password:
            super().fill_field(self.LOCATORS["password"], password)
