import pytest
import logging.config

from opencart_ui_tests.pages.register_page import RegisterPage, EXAMPLE_USER
from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


@pytest.mark.smoke
def test_registration(browser, base_url):
    """Test simple valid registration flow"""
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    register_page.fill_field_register_page(**generated_user)
    register_page.click(register_page.LOCATORS["agree to privacy policy checkbox"])
    register_page.click(register_page.LOCATORS["continue"])
    LOGGER.debug(f"ASSERT: successfully registered and redirected to {register_page.SUCCESS_REGISTRATION_URL_APPENDIX}")
    assert register_page.SUCCESS_REGISTRATION_URL_APPENDIX in browser.current_url, \
        f"Expected to reach {register_page.SUCCESS_REGISTRATION_URL_APPENDIX} after registration, " \
        f"but got {browser.current_url}"


def test_should_be_link_to_login_page(browser, base_url):
    """Check that user can go to 'login' page from 'register' (there should be link)"""
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    login_link = register_page.wait_element(register_page.LOCATORS["login link"])
    register_page.click(login_link)
    LOGGER.debug(f"ASSERT: reached '{base_url + register_page.LOGIN_URL_APPENDIX}' after clicking 'login page' link")
    assert register_page.LOGIN_URL_APPENDIX in browser.current_url, \
        f"Expected to reach '{base_url + register_page.LOGIN_URL_APPENDIX}' after clicking 'login page' link"


def test_cannot_register_if_do_not_agree_to_policy(browser, base_url):
    """Check that user cannot register if he doesn't enable 'Agree to policy' checkbox"""
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    register_page.fill_field_register_page(**generated_user)
    # ... skip agree to Policy checkbox
    LOGGER.debug(f"Skipping 'Agree to policy' checkbox, not clicking on it...")
    register_page.click(register_page.LOCATORS["continue"])
    error_banner = register_page.wait_element(register_page.LOCATORS["error banner"])
    error_banner_text = register_page.get_element_text(error_banner)
    LOGGER.debug(f"ASSERT: There is error message: '{register_page.ERROR_TEXT_POLICY}'")
    assert register_page.ERROR_TEXT_POLICY in error_banner_text, \
        f"Expected to get error message: '{register_page.ERROR_TEXT_POLICY}', but got '{error_banner_text}'"


@pytest.mark.smoke
@pytest.mark.parametrize("user_data_item", EXAMPLE_USER.keys())
def test_cannot_register_if_any_of_mandatory_fields_is_empty(user_data_item, browser, base_url):
    """"Check that user cannot register if he doesn't fill all required fields; user remains on 'register page'"""
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    del (generated_user[user_data_item])
    register_page.fill_field_register_page(**generated_user)
    register_page.click(register_page.LOCATORS["agree to privacy policy checkbox"])
    register_page.click(register_page.LOCATORS["continue"])
    LOGGER.debug(f"ASSERT: cannot register if one of mandatory field is empty, user remains on 'register page'")
    assert browser.current_url == register_page.url, \
        f"Expected that user remains on register page if there is an error in registration, " \
        f"but URL changed to {browser.current_url}"


def test_cannot_register_if_password_and_password_confirmation_do_not_match(browser, base_url):
    """Check that user cannot register if password confirmation fails"""
    register_page = RegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(register_page.LOCATORS["first name"])
    generated_user = register_page.generate_user()
    generated_user["password_confirm"] += "$"
    register_page.fill_field_register_page(**generated_user)
    register_page.click(register_page.LOCATORS["agree to privacy policy checkbox"])
    register_page.click(register_page.LOCATORS["continue"])
    LOGGER.debug(f"ASSERT: cannot register if password confirmation failed, user remains on 'register page'")
    assert browser.current_url == register_page.url, \
        f"Expected that user remains on register page if password confirmation failed, " \
        f"but URL changed to {browser.current_url}"
