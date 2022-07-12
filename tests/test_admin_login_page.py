import pytest
from pages.admin_login_page import AdminLoginPage
from pages.auth import Users


@pytest.mark.parametrize("user", [Users.ADMIN])
def test_login(user, browser, base_url):
    login_page = AdminLoginPage(browser, base_url)
    login_page.open()
    login_page.wait_element(login_page.LOCATORS["username"])
    login_page.fill_field_login_page(**user)
    login_page.click(login_page.LOCATORS["login button"])
    assert login_page.LOGGED_IN_URL_APPENDIX_PART in browser.current_url, \
        f"Expected that user '{user['username']}' has been successfully logged in and redirected to " \
        f"'{base_url + login_page.LOGGED_IN_URL_APPENDIX_PART}'"


def test_page_title(browser, base_url):
    login_page = AdminLoginPage(browser, base_url)
    login_page.open()
    page_title = login_page.wait_element(login_page.LOCATORS["page title"])
    page_title_text = login_page.get_element_text(page_title)
    assert login_page.PAGE_TITLE in page_title_text, \
        f"Expected page title to be '{login_page.PAGE_TITLE}', but got '{page_title_text}'"


def test_click_forgotten_password_should_redirect_to_this_page(browser, base_url):
    login_page = AdminLoginPage(browser, base_url)
    login_page.open()
    forgotten_password_button = login_page.wait_element(login_page.LOCATORS["forgotten password"])
    login_page.click(forgotten_password_button)
    assert login_page.wait_element(login_page.LOCATORS["email"]) \
           and login_page.FORGOTTEN_PASSWORD_URL_APPENDIX in browser.current_url, \
           f"Expected to reach {base_url + login_page.FORGOTTEN_PASSWORD_URL_APPENDIX} " \
           f"after clicking 'forgotten password' but got {browser.current_url}"


def test_should_be_error_banner_with_message_if_non_existing_user(browser, base_url):
    login_page = AdminLoginPage(browser, base_url)
    login_page.open()
    login_page.wait_element(login_page.LOCATORS["username"])
    login_page.fill_field_login_page(**Users.NON_EXISTING_USER)
    login_page.click(login_page.LOCATORS["login button"])
    assert login_page.wait_element(login_page.LOCATORS["error banner"]), \
        f"Expected to get error banner when trying to login as non existing user, but didn't find one"
    actual_error_text = login_page.get_element_text(login_page.LOCATORS["error banner"])
    assert login_page.NO_SUCH_USER_ERROR in actual_error_text, \
        f"Expected that error text is '{login_page.NO_SUCH_USER_ERROR}', but got {actual_error_text}"
    assert login_page.LOGGED_IN_URL_APPENDIX_PART not in browser.current_url, \
        f"Expected that non-existing user '{Users.NON_EXISTING_USER['username']}' couldn't login"


def test_close_error_banner(browser, base_url):
    login_page = AdminLoginPage(browser, base_url)
    login_page.open()
    login_page.wait_element(login_page.LOCATORS["username"])
    login_page.fill_field_login_page(**Users.NON_EXISTING_USER)
    login_page.click(login_page.LOCATORS["login button"])
    assert login_page.wait_element(login_page.LOCATORS["error banner"]), \
        f"Expected to get error banner when trying to login as non existing user, but didn't find one"
    close_error_banner_button = login_page.wait_element(login_page.LOCATORS["close error banner button"])
    login_page.click(close_error_banner_button)
    assert login_page.wait_element_not_present(login_page.LOCATORS["error banner"]), \
        f"Expected error banner to disappear after clicking 'cross' icon, but it is still visible"
