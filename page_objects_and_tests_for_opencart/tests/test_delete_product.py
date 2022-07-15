import pytest
import allure
import logging.config

from page_objects_and_tests_for_opencart.pages.admin_products_page import AdminProductsPage

from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


@pytest.mark.xfail(reason="Fails in headless mode (only)")
def test_add_new_product_and_delete(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: name, meta, model"""
    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()
    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_the_exact_product(created_product["name"])
    products_page.delete_selected_products()
    product_number_after_deletion = products_page. \
        filter_products_by(name=created_product["name"]). \
        get_products_number_on_page()
    LOGGER.debug("ASSERT: There is no products on page (deleted product and filtered product by its name")
    try:
        assert product_number_after_deletion == 0, \
            f"Didn't expect to find the product '{created_product['name']}' on page after deletion, but found it!"
    except Exception as e:
        allure.attach(browser.get_screenshot_as_png(), "Screenshot on failure", allure.attachment_type.PNG)
        raise e


@pytest.mark.xfail(reason="Fails in headless mode (only)")
def test_should_be_alert_on_delete_action(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: name, meta, model"""
    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()
    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_the_exact_product(created_product["name"])
    products_page.click(products_page.LOCATORS["delete"])
    LOGGER.debug("ASSERT: There is browser alert, after clicking the 'Delete' button")
    try:
        assert products_page.wait_alert(), \
            f"Expected to get an alert after pressing the delete button, but didn't find one."
        products_page.wait_alert().accept()
    except Exception as e:
        allure.attach(browser.get_screenshot_as_png(), "Screenshot on failure", allure.attachment_type.PNG)
        raise e


@pytest.mark.xfail(reason="Fails in headless mode (only)")
def test_should_not_delete_product_if_dismiss_alert(browser, base_url, go_to_add_new_product_page):
    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()
    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_the_exact_product(created_product["name"])
    products_page.click(products_page.LOCATORS["delete"])
    products_page.wait_alert().dismiss()
    product_number_after_deletion = products_page. \
        filter_products_by(name=created_product["name"]). \
        get_products_number_on_page()
    LOGGER.debug(f"ASSERT: There is '{created_product['name']}' on page, because we didn't confirm deleting it")
    try:
        assert product_number_after_deletion == 1, \
            f"Expected to find the product '{created_product['name']}' on page, because it should not been deleted, " \
            f"but didn't found it!"
    except Exception as e:
        allure.attach(browser.get_screenshot_as_png(), "Screenshot on failure", allure.attachment_type.PNG)
        raise e
