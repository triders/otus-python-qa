from pages.main_page import MainPage


def test_logo_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element(main_page.LOCATORS["logo"])


def test_nav_bar_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element(main_page.LOCATORS["navbar"])


def test_nav_bar_items_clickable(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element_clickable(main_page.LOCATORS["navbar items"])


def test_cart_is_empty(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    cart_button_text = main_page.wait_element(main_page.LOCATORS["cart button"]).text
    assert cart_button_text == "0 item(s) - $0.00"
