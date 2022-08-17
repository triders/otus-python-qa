import time
import pytest
import logging.config

from opencart_ui_tests.pages.catalog_page import CatalogPage
from opencart_ui_tests.pages.product_page import ProductPage
from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")
CATALOG_IDS = ["laptop-notebook"]
# CATALOG_IDS = ["laptop-notebook", "windows", "tablet", "software", "smartphone", "mp3-players"]


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_catalog_name_the_same_as_tab_name(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    tab_name = catalog_page.get_tab_name()
    page_title = catalog_page.get_element_text(catalog_page.LOCATORS["catalog page title"])
    LOGGER.debug(f"ASSERT: tab name '{tab_name}' is the same as catalog page title '{page_title}'")
    assert tab_name == page_title, \
        f"Expected tab name '{tab_name}' to be the same as catalog page title '{page_title}'"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_if_no_products_in_category_should_be_corresponding_message(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if not catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        LOGGER.debug(f"There is no products in {catalog_id}")
        page_description = catalog_page.get_element_text(catalog_page.LOCATORS["no products in category"])
        LOGGER.debug(f"ASSERT: page description text is '{catalog_page.NO_PRODUCTS_MESSAGE}'")
        assert page_description == catalog_page.NO_PRODUCTS_MESSAGE, \
            f"Expected to see text '{catalog_page.NO_PRODUCTS_MESSAGE}' " \
            f"because catalog '{catalog_id}' does not have any products. But got '{page_description}'"
        LOGGER.debug(f"ASSERT: 'Continue' button is on the page")
        assert catalog_page.wait_element(catalog_page.LOCATORS["no products in category > continue button"]), \
            f"Expected to see 'Continue' button on the page, but didn't find one"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_switch_products_view(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        # grid view is by default
        LOGGER.debug(f"ASSERT: all products are shown in grid by default")
        assert (
                catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page grid"])
                and
                not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page list"])
        ), f"All products are NOT shown in grid (which should be the default view mode)"
        # switch to list view
        catalog_page.click(catalog_page.LOCATORS["list view button"])
        LOGGER.debug(f"ASSERT: all products are shown in list, after switching to the 'list' view")
        assert (
                catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page list"])
                and
                not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page grid"])
        ), f"All products are NOT shown in list (after switching to the 'list' view)"


@pytest.mark.parametrize("product_index", range(2))  # test first 2 products in each category
@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_add_product_to_cart_should_be_success_message_and_increase_cart_total(catalog_id, product_index, browser, base_url):
    catalog_page = CatalogPage(catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        # we check only catalogs containing at least 1 product
        LOGGER.debug(f"Catalog '{catalog_id}' contains at least 1 product")
        catalog_page.scroll_to_element(catalog_page.LOCATORS["add to cart buttons"])
        try:
            catalog_page.add_to_cart(product_index)
            time.sleep(1)  # url may change, we wait for it
            if browser.current_url != catalog_page.url:
                # if product has required fields it cannot be added from Catalog - redirect to product page occurs.
                # We check that the product actually has at least 1 required field here
                LOGGER.debug("User is redirected to the product page. Seems that this product has required fields...")
                catalog_page.scroll_to_element(ProductPage.LOCATORS["add to cart required fields"])
                LOGGER.debug(f"ASSERT: product '{browser.current_url}' has at least 1 required field")
                assert catalog_page.get_element_if_present(ProductPage.LOCATORS["add to cart required fields"],
                                                           only_first=True), \
                    f"Product '{browser.current_url}' doesn't have any required field. " \
                    f"So it should have been added to cart from main page (but wasn't)"
            else:
                # other products can be added from Catalog page, should be success message
                catalog_page.wait_element(
                    catalog_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
                success_message = catalog_page.get_element_if_present(catalog_page.LOCATORS["alert"], only_first=True)
                success_message_text = catalog_page.get_element_text(success_message)
                LOGGER.debug(f"ASSERT: there is success message")
                assert "Success: You have added" and " to your shopping cart!" in success_message_text, \
                    f"Expected success message to be ' Success: You have added ... to your shopping cart!', " \
                    f"but got {success_message_text}"
                items_in_cart, total_price = catalog_page.get_cart_item_count_and_total_price()
                LOGGER.debug(f"ASSERT: should be 1 item in cart")
                assert items_in_cart == 1 and total_price != 0, \
                    f"Should be 1 item in cart, but got {items_in_cart} items, total price is ${total_price}"

        except IndexError:
            # in this test we check adding to cart first N products in category
            # and ignore if category contains less than N products
            pass
