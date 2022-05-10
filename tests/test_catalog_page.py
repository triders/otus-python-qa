import time
import pytest
from pages.catalog_page import CatalogPage

CATALOG_IDS = ["laptop-notebook", "windows", "tablet", "software", "smartphone", "mp3-players"]


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_catalog_name_the_same_as_tab_name(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    tab_name = catalog_page.get_tab_name()
    page_title = catalog_page.get_element_text(catalog_page.LOCATORS["catalog page title"])
    assert tab_name == page_title, \
        f"Expected tab name '{tab_name}' to be the same as catalog page title '{page_title}'"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_if_no_products_in_category(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page"]):
        page_description = catalog_page.get_element_text(catalog_page.LOCATORS["no products in category"])
        assert page_description == catalog_page.NO_PRODUCTS_MESSAGE
        assert catalog_page.wait_element(catalog_page.LOCATORS["no products in category > continue button"])


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_switch_products_view(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    if catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page"]):
        # grid view is by default
        assert catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page grid"])
        assert not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page list"])
        # switch to list view
        catalog_page.click(catalog_page.LOCATORS["list view button"])
        assert catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page list"])
        assert not catalog_page.get_element_if_present(catalog_page.LOCATORS["products on page grid"])
