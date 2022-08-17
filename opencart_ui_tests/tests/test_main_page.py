import time
import pytest
import logging.config

from opencart_ui_tests.pages.main_page import MainPage
from opencart_ui_tests.pages.product_page import ProductPage
from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


def test_logo_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    LOGGER.debug(f"ASSERT: there is opencart logo on main page")
    assert main_page.wait_element(main_page.BASE_PAGE_LOCATORS["logo"]), \
        f"Unable to find opencart logo on main page"


def test_usd_should_be_default_currency(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    current_currency = main_page.get_current_currency()
    LOGGER.debug(f"ASSERT: USD ($) to be default currency")
    assert current_currency == main_page.CURRENCY_SIGNS["USD"], \
        f"Expected 'USD' ($) to be default currency, but got {current_currency}"


@pytest.mark.parametrize("currency", ["USD", "EUR", "GBP"])
def test_change_currency(currency, browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.change_currency_to(currency=currency)
    current_currency = main_page.get_current_currency()
    LOGGER.debug(f"ASSERT: currency changed to '{main_page.CURRENCY_SIGNS[currency.upper()]}'")
    assert current_currency == main_page.CURRENCY_SIGNS[currency.upper()], \
        f"Expected currency to be '{main_page.CURRENCY_SIGNS[currency.upper()]}', but got '{current_currency}'"


@pytest.mark.smoke
def test_nav_bar_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    LOGGER.debug(f"ASSERT: there is navigation bar on the Main page")
    assert main_page.wait_element(main_page.BASE_PAGE_LOCATORS["navbar"]), \
        f"Unable to find navigation bar on the Main page"


def test_nav_bar_items_clickable(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    nav_bar_items = main_page.get_element_if_present(main_page.BASE_PAGE_LOCATORS["navbar items"])
    LOGGER.debug(f"ASSERT: navigation bar items are clickable")
    for item in nav_bar_items:
        assert main_page.wait_element_clickable(item)


def test_cart_is_empty_on_first_launch(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
    LOGGER.debug(f"ASSERT: cart is empty when a user opens Opencart for the first time")
    assert items_in_cart == 0 and total_price == 0, \
        f"Should be no items in cart, but got {items_in_cart} items, total price is ${total_price}"


@pytest.mark.parametrize("product_index", [
    pytest.param(1, marks=pytest.mark.smoke),
    2, 3])
def test_add_featured_product_to_cart_should_be_success_message(product_index, browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.scroll_to_element(main_page.LOCATORS["featured: add to cart buttons"])
    main_page.add_to_cart(product_index)
    time.sleep(1)  # url may change, we wait for it
    if browser.current_url != main_page.url:
        # if product has required fields it cannot be added from Main - redirect to product page occurs.
        # We check that the product actually has at least 1 required field here
        LOGGER.debug("User is redirected to the product page. Seems that this product has required fields...")
        main_page.scroll_to_element(ProductPage.LOCATORS["add to cart required fields"])
        LOGGER.debug(f"ASSERT: product '{browser.current_url}' has at least 1 required field")
        assert main_page.get_element_if_present(ProductPage.LOCATORS["add to cart required fields"],
                                                only_first=True), \
            f"Product '{browser.current_url}' doesn't have any required field. " \
            f"So it should have been added to cart from main page (but wasn't)"
    else:
        # other products can be added from Main page, should be success message
        main_page.wait_element(
            main_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
        success_message = main_page.get_element_if_present(main_page.LOCATORS["alert"], only_first=True)
        success_message_text = main_page.get_element_text(success_message)
        LOGGER.debug(f"ASSERT: there is success message")
        assert "Success: You have added" and " to your shopping cart!" in success_message_text, \
            f"Expected success message to be ' Success: You have added ... to your shopping cart!', " \
            f"but got {success_message_text}"
        items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
        LOGGER.debug(f"ASSERT: should be 1 item in cart")
        assert items_in_cart == 1 and total_price != 0, \
            f"Should be 1 item in cart, but got {items_in_cart} items, total price is ${total_price}"
