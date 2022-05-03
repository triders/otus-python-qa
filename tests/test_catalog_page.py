import pytest
from pages.catalog_page import CatalogPage

# CATALOG_IDS = ["laptop-notebook", "windows", "tablet", "software", "smartphone", "mp3-players"]
CATALOG_IDS = ["laptop-notebook"]


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_catalog_page_tab_name_the_same_as_title(catalog_id, browser, base_url):
    catalog_page = CatalogPage(catalog_id=catalog_id, browser=browser, base_url=base_url)
    catalog_page.open()
    tab_name = catalog_page.get_tab_name()
    page_title = catalog_page.get_element_text(catalog_page.LOCATORS["catalog page title"])
    assert tab_name == page_title, \
        f"Expected tab name '{tab_name}' to be the same as catalog page title '{page_title}'"
