import pytest
from pages.product_page import ProductPage

# PRODUCT_IDS = ["iphone", "imac", "test", "canon-eos-5d", "nikon-d300", "samsung-syncmaster-941bw"]
PRODUCT_IDS = ["iphone"]


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_name_is_not_empty(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    product_name = product_page.get_element_text(product_page.LOCATORS["product name"])
    assert product_name != ""


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_price_in_dollar_currency(product_id, browser, base_url):
    product_page = ProductPage(product_id=product_id, browser=browser, base_url=base_url)
    product_page.open()
    product_price = product_page.get_element_text(product_page.LOCATORS["product price"])
    assert product_price[0] is "$"
    assert int(product_price[1:].split(".")[0]) > 0  # e.g. price = "$122.00", we check that 122 > 0
