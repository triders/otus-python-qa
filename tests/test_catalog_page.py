import time
import pytest
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage

CATALOG_IDS = ["laptop-notebook", "windows", "tablet", "software", "smartphone", "mp3-players"]
# CATALOG_IDS = ["laptop-notebook"]


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_catalog_name_the_same_as_tab_name(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    tab_name = catalog_page.get_tab_name()
    page_title = catalog_page.get_element_text(catalog_page.LOCATORS["catalog page title"])
    assert tab_name == page_title, \
        f"Expected tab name '{tab_name}' to be the same as catalog page title '{page_title}'"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_if_no_products_in_category_should_be_corresponding_message(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if not catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        page_description = catalog_page.get_element_text(catalog_page.LOCATORS["no products in category"])
        assert page_description == catalog_page.NO_PRODUCTS_MESSAGE, \
            f"Expected to see text '{catalog_page.NO_PRODUCTS_MESSAGE}' " \
            f"because catalog '{catalog_id}' does not have any products. But got '{page_description}'"
        assert catalog_page.wait_element(catalog_page.LOCATORS["no products in category > continue button"]), \
            f"Expected to see 'Continue' button on the page, but didn't find one"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_switch_products_view(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        # grid view is by default
        assert catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page grid"])
        assert not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page list"])
        # switch to list view
        catalog_page.click(catalog_page.LOCATORS["list view button"])
        assert catalog_page.wait_element(catalog_page.LOCATORS["products on page list"])
        assert not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page grid"])


@pytest.mark.parametrize("product_index", range(2))
@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_add_product_to_cart_should_be_success_message(catalog_id, product_index, browser, base_url):
    catalog_page = CatalogPage(catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        # we check only catalogs containing at least 1 product
        catalog_page.scroll_to_element(catalog_page.LOCATORS["add to cart buttons"])
        try:
            catalog_page.add_to_cart(product_index)
            time.sleep(1)  # url may change, we wait for it
            if browser.current_url != catalog_page.url:
                # if product has required fields it cannot be added from main - redirect to product page occurs.
                # We check that the product actually has at least 1 required field here
                catalog_page.scroll_to_element(ProductPage.LOCATORS["add to cart required fields"])
                assert catalog_page.get_element_if_present(ProductPage.LOCATORS["add to cart required fields"],
                                                           only_first=True)
            else:
                # other products can be added from main page, should be success message
                catalog_page.wait_element(
                    catalog_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
                success_message = catalog_page.get_element_if_present(catalog_page.LOCATORS["alert"], only_first=True)
                success_message_text = catalog_page.get_element_text(success_message)
                assert "Success: You have added" and " to your shopping cart!" in success_message_text, \
                    f"Expected success message to be ' Success: You have added ... to your shopping cart!', " \
                    f"but got {success_message_text}"
        except IndexError:
            # in this test we check adding to cart first N products in category
            # and ignore if category contains less than N products
            pass


@pytest.mark.parametrize("product_index", range(2))  # test first 2 products in each category
@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_add_product_to_cart_should_increase_cart_total(catalog_id, product_index, browser, base_url):
    catalog_page = CatalogPage(catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if catalog_page.wait_element(catalog_page.LOCATORS["products on page"]):
        # we check only catalogs containing at least 1 product
        catalog_page.scroll_to_element(catalog_page.LOCATORS["add to cart buttons"])
        try:
            catalog_page.add_to_cart(product_index)
            time.sleep(1)  # url may change, we wait for it
            if browser.current_url != catalog_page.url:
                # if product has required fields it cannot be added from main - redirect to product page occurs.
                # We check that the product actually has at least 1 required field here
                catalog_page.scroll_to_element(ProductPage.LOCATORS["add to cart required fields"])
                assert catalog_page.get_element_if_present(ProductPage.LOCATORS["add to cart required fields"],
                                                           only_first=True)
            else:
                # other products can be added from main page, should be success message
                catalog_page.wait_element(
                    catalog_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
                items_in_cart, total_price = catalog_page.get_cart_item_count_and_total_price()
                assert items_in_cart == 1 and total_price != 0, \
                    f"Should be 1 item in cart, but got {items_in_cart} items, total price is ${total_price}"
        except IndexError:
            # in this test we check adding to cart first N products in category
            # and ignore if category contains less than N products
            pass
