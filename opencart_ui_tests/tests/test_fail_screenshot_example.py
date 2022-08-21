import pytest
import logging.config

from opencart_ui_tests.pages.main_page import MainPage
from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


@pytest.mark.smoke
def test_no_logo_on_main_page_exists(browser, base_url):
    """Check there is NO OpenCart logo on 'Main page'"""
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    LOGGER.debug(f"ASSERT: there is NO opencart logo on main page!!!")
    assert not main_page.wait_element(main_page.BASE_PAGE_LOCATORS["logo"]), \
        f"Unfortunately, found opencart logo on main page!"


@pytest.mark.smoke
def test_rub_should_be_default_currency(browser, base_url):
    """Check that 'RUB' is default currency"""
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    current_currency = main_page.get_current_currency()
    LOGGER.debug(f"ASSERT: 'RUB' is default currency")
    assert current_currency == "RUB", \
        f"Expected 'RUB' to be default currency, but got {current_currency}"
