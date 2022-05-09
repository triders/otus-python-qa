from pages.main_page import MainPage


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


def test_cart_is_empty(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
    assert items_in_cart == 0 and total_price == 0, \
        f"Should be no items in cart, but got {items_in_cart} items, total price is ${total_price}"


def test_add_first_featured_product_to_cart_should_be_success_message(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.scroll_to_element(main_page.LOCATORS["featured: add to cart buttons"])
    add_to_cart_button = main_page.get_element_if_present(locator=main_page.LOCATORS["featured: add to cart buttons"],
                                                          only_first=True)
    main_page.click(add_to_cart_button)
    main_page.wait_element(main_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
    success_message = main_page.get_element_if_present(main_page.LOCATORS["alert"], only_first=True)
    success_message_text = main_page.get_element_text(success_message)
    assert "Success: You have added MacBook to your shopping cart!" in success_message_text, \
        f"Expected success message to be ' Success: You have added MacBook to your shopping cart!', " \
        f"but got {success_message_text}"


def test_add_first_featured_product_to_cart_should_increase_cart_total(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.scroll_to_element(main_page.LOCATORS["featured: add to cart buttons"])
    add_to_cart_button = main_page.get_element_if_present(locator=main_page.LOCATORS["featured: add to cart buttons"],
                                                          only_first=True)
    main_page.click(add_to_cart_button)
    main_page.wait_element(main_page.LOCATORS["alert"])  # page automatically scrolls to top, but it takes some time
    items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
    assert items_in_cart == 1 and total_price != 0, \
        f"Should be 1 items in cart, but got {items_in_cart} items, total price is ${total_price}"
