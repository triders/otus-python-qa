import pytest
from opencart_ui_tests.pages.admin_products_page import AdminProductsPage
import logging.config

from opencart_ui_tests.logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


def test_click_add_new_product_should_open_this_page(browser, base_url, go_to_add_new_product_page):
    """Should be "Save" button on the "Add new product" page"""
    add_page = go_to_add_new_product_page
    LOGGER.debug("ASSERT: There is the 'Save' button on the 'Add New Product' page.")
    assert add_page.wait_element(add_page.LOCATORS["save"]), \
        f"Unable to find the 'Save' button on the 'Add New Product' page."


def test_add_new_product_page_contains_all_tabs(browser, base_url, go_to_add_new_product_page):
    """Should be all tabs on the "Add new product" page: "General", "Data", "Links", "Attribute", etc."""
    add_page = go_to_add_new_product_page
    LOGGER.debug("ASSERT: All settings tabs are present on the Add new product' page")
    for tab_name, locator in add_page.LOCATORS["tab"].items():
        LOGGER.debug(f"ASSERT: {tab_name}' tab is present")
        assert add_page.get_element_if_present(locator), \
            f"Unable to locate '{tab_name}' tab on the 'Add new product' page."

def test_general_tab_contains_all_fields(browser, base_url, go_to_add_new_product_page):
    """Check all fields are present on the "General" tab"""
    add_page = go_to_add_new_product_page
    LOGGER.debug("ASSERT: 'general' tab contains all fields (on the Add new product' page")
    for field_name, locator in add_page.LOCATORS["general"].items():
        LOGGER.debug(f"ASSERT: field '{field_name}' is present")
        assert add_page.get_element_if_present(locator), \
            f"Unable to locate '{field_name}' field on the 'General' tab."


@pytest.mark.xfail(reason="Fails in headless mode (only)")
def test_can_add_new_product_filling_only_required_fields(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: name, meta, model"""
    add_page = go_to_add_new_product_page
    created_product = add_page.create_product()
    products_list_filtered = AdminProductsPage(browser, base_url) \
        .filter_products_by(name=created_product['name'])
    LOGGER.debug(f"ASSERT: created product '{created_product['name']}' appeared in the Products list")
    assert products_list_filtered.get_product_by_name(created_product["name"]), \
        f"Unable to find newly created product '{created_product['name']}' in the Products list."


@pytest.mark.parametrize("fields", [{"name": "", "model": "foo", "meta": "bar"},
                                    {"name": "foo", "model": "", "meta": "bar"},
                                    {"name": "foo", "model": "bar", "meta": ""}])
def test_cannot_add_new_product_with_empty_required_field(fields, browser, base_url, go_to_add_new_product_page):
    """Should be not able to create product if any of required fields is empty: name, meta or model"""
    add_page = go_to_add_new_product_page
    add_page.create_product(**fields)
    LOGGER.debug(f"ASSERT: there is an error message when trying to save a product "
                 f"with one of the required fields empty: '{fields}'")
    assert add_page.wait_element(add_page.LOCATORS["error banner"]), \
        f"Expected to get error message when trying to save a product with one of the required fields empty: '{fields}'"


def test_page_title(browser, base_url, go_to_add_new_product_page):
    add_page = go_to_add_new_product_page
    page_title = add_page.get_element_text(add_page.LOCATORS["page title"])
    LOGGER.debug(f"ASSERT: Page title to be '{add_page.PAGE_TITLE}'")
    assert add_page.PAGE_TITLE in page_title, \
        f"Expected page title to be '{add_page.PAGE_TITLE}', but got '{page_title}'"
