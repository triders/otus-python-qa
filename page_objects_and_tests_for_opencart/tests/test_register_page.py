import pytest
from page_objects_and_tests_for_opencart.pages.register_page import RegisterPage, EXAMPLE_USER


def test_registration(browser, base_url):
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    register_page.fill_field_register_page(**generated_user)
    register_page.click(register_page.LOCATORS["agree to privacy policy checkbox"])
    register_page.click(register_page.LOCATORS["continue"])
    assert register_page.SUCCESS_REGISTRATION_URL_APPENDIX in browser.current_url


def test_should_be_link_to_login_page(browser, base_url):
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    login_link = register_page.wait_element(register_page.LOCATORS["login link"])
    register_page.click(login_link)
    assert register_page.LOGIN_URL_APPENDIX in browser.current_url, \
        f"Expected to reach '{base_url + register_page.LOGIN_URL_APPENDIX}' after clicking 'login page' link"


def test_cannot_register_if_do_not_agree_to_policy(browser, base_url):
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    register_page.fill_field_register_page(**generated_user)
    # ... skip agree to Policy checkbox
    register_page.click(register_page.LOCATORS["continue"])
    error_banner = register_page.wait_element(register_page.LOCATORS["error banner"])
    error_banner_text = register_page.get_element_text(error_banner)
    assert register_page.ERROR_TEXT_POLICY in error_banner_text, \
        f"Expected to get error message: '{register_page.ERROR_TEXT_POLICY}', but got '{error_banner_text}'"
    assert browser.current_url == register_page.url  # url should not change if there is an error in registration


@pytest.mark.parametrize("user_data_item", EXAMPLE_USER.keys())
def test_cannot_register_if_any_of_mandatory_fields_is_empty(user_data_item, browser, base_url):
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    del (generated_user[user_data_item])
    register_page.fill_field_register_page(**generated_user)
    register_page.click(register_page.LOCATORS["agree to privacy policy checkbox"])
    register_page.click(register_page.LOCATORS["continue"])
    assert browser.current_url == register_page.url  # url should not change if there is an error in registration


def test_cannot_register_if_password_and_password_confirmation_do_not_match(browser, base_url):
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    generated_user["password_confirm"] += "$"
    register_page.fill_field_register_page(**generated_user)
    register_page.click(register_page.LOCATORS["agree to privacy policy checkbox"])
    register_page.click(register_page.LOCATORS["continue"])
    assert browser.current_url == register_page.url  # url should not change if there is an error in registration
