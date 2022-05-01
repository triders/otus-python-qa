import time
from pages.main_page import MainPage


def test_open_main_page(browser, base_url):
    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
