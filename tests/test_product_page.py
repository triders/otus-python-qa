import pytest
from pages.product_page import ProductPage


@pytest.mark.parametrize("product_id", ["iphone", "imac", "test"])
# @pytest.mark.parametrize("product_id", ["iphone"])
def test_product_name_is_not_empty(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    product_name = product_page.get_element_text(product_page.LOCATORS["product_name"])
    assert product_name != ""
