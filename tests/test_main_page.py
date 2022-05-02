import time
from pages.main_page import MainPage


def test_logo_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element(main_page.LOCATORS["logo"])


def test_nav_bar_on_main_page_exists(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.wait_element(main_page.LOCATORS["navbar"])
