import pytest
import logging.config

from opencart_ui_tests.pages.product_page import ProductPage
from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

PRODUCT_IDS = [
    pytest.param("iphone", marks=pytest.mark.smoke),
    "imac", "nikon-d300", "samsung-syncmaster-941bw",
    "test", "canon-eos-5d"]
XFAIL_PRODUCT_IDS_FOR_test_product_name_the_same_as_tab_name = [
    pytest.param("test", marks=pytest.mark.xfail(strict=True)),
    pytest.param("canon-eos-5d", marks=pytest.mark.xfail(strict=True))]


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_name_is_not_empty(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    product_name = product_page.get_element_text(product_page.LOCATORS["product name"])
    LOGGER.debug(f"ASSERT: Product name '{product_name}' is not empty (blank)")
    assert not product_name.isspace(), f"The product name seems to be empty:'{product_name}'"


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_price_is_greater_than_zero(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    product_price = product_page.get_product_price(currency="$")
    LOGGER.debug(f"ASSERT: product '{product_page.get_tab_name()}' has non-zero price")
    assert product_price > 0, \
        f"Seems that product '{product_page.get_tab_name()}' has no price. Can I have 2 for free?"


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_has_main_image(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    LOGGER.debug(f"ASSERT: Product '{product_page.get_tab_name()}' has main image")
    assert product_page.wait_element(product_page.LOCATORS["product main image"]), \
        f"Product '{product_page.get_tab_name()}' doesn't have main image"


@pytest.mark.parametrize("product_id", XFAIL_PRODUCT_IDS_FOR_test_product_name_the_same_as_tab_name)
def test_product_name_the_same_as_tab_name(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    tab_name = product_page.get_tab_name()
    product_name = product_page.get_element_text(product_page.LOCATORS["product name"])
    LOGGER.debug(f"ASSERT: tab name '{tab_name}' is the same as product name '{product_name}'")
    assert tab_name == product_name, \
        f"Expected tab name '{tab_name}' to be the same as product name '{product_name}'"


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_name_the_same_in_title_and_breadcrumb_navigation(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    product_name_title = product_page.get_element_text(
        product_page.LOCATORS["product name"])
    product_name_breadcrumb = product_page.get_element_text(
        product_page.LOCATORS["product name in breadcrumb navigation"])
    LOGGER.debug(f"ASSERT: product name in breadcrumb navigation '{product_name_breadcrumb}' "
                 f"is the same as product name title '{product_name_title}'")
    assert product_name_breadcrumb == product_name_title, \
        f"Expected product name in breadcrumb navigation '{product_name_breadcrumb}' " \
        f"to be the same as product name title '{product_name_title}'"
