import time
import pytest

from pages.main_page import MainPage
from pages.product_page import ProductPage


def test_logo_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element(main_page.BASE_PAGE_LOCATORS["logo"])


def test_nav_bar_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element(main_page.BASE_PAGE_LOCATORS["navbar"])


def test_nav_bar_items_clickable(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    nav_bar_items = main_page.get_element_if_present(main_page.BASE_PAGE_LOCATORS["navbar items"])
    for item in nav_bar_items:
        main_page.wait_element_clickable(item)


def test_cart_is_empty_on_first_launch(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
    assert items_in_cart == 0 and total_price == 0, \
        f"Should be no items in cart, but got {items_in_cart} items, total price is ${total_price}"


@pytest.mark.parametrize("product_index", range(4))
def test_add_featured_product_to_cart_should_be_success_message(product_index, browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.scroll_to_element(main_page.LOCATORS["featured: add to cart buttons"])
    main_page.add_to_cart(product_index)
    time.sleep(1)  # url may change, we wait for it
    if browser.current_url != main_page.url:
        # if product has required fields it cannot be added from main - redirect to product page occurs.
        # We check that the product actually has at least 1 required field here
        main_page.scroll_to_element(ProductPage.LOCATORS["add to cart required fields"])
        assert main_page.get_element_if_present(ProductPage.LOCATORS["add to cart required fields"], only_first=True)
    else:
        # other products can be added from main page, should be success message
        main_page.wait_element(main_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
        success_message = main_page.get_element_if_present(main_page.LOCATORS["alert"], only_first=True)
        success_message_text = main_page.get_element_text(success_message)
        assert "Success: You have added" and " to your shopping cart!" in success_message_text, \
            f"Expected success message to be ' Success: You have added ... to your shopping cart!', " \
            f"but got {success_message_text}"


@pytest.mark.parametrize("product_index", range(4))
def test_add_featured_product_to_cart_should_increase_cart_total(product_index, browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.scroll_to_element(main_page.LOCATORS["featured: add to cart buttons"])
    main_page.add_to_cart(product_index)
    time.sleep(1)  # url may change, we wait for it
    if browser.current_url != main_page.url:
        # if product has required fields it cannot be added from main - redirect to product page occurs.
        # We check that the product actually has at least 1 required field here
        main_page.scroll_to_element(ProductPage.LOCATORS["add to cart required fields"])
        assert main_page.get_element_if_present(ProductPage.LOCATORS["add to cart required fields"], only_first=True)
    else:
        # other products can be added from main page, should be success message
        main_page.wait_element(main_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
        items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
        assert items_in_cart == 1 and total_price != 0, \
            f"Should be 1 items in cart, but got {items_in_cart} items, total price is ${total_price}"


def test_usd_should_be_default_currency(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    current_currency = main_page.get_current_currency()
    assert current_currency == main_page.CURRENCY_SIGNS["USD"], \
        f"Expected $ to be default currency, but got {current_currency}"


@pytest.mark.parametrize("currency", ["usd", "eur", "gbp"])
def test_change_currency(currency, browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.change_currency_to(currency=currency)
    current_currency = main_page.get_current_currency()
    assert current_currency == main_page.CURRENCY_SIGNS[currency.upper()], \
        f"Expected currency to be {main_page.CURRENCY_SIGNS[currency.upper()]}, but got {current_currency}"
