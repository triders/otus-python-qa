from selenium import webdriver
import time


def test_open_opencart(browser, base_url):
    browser.get(base_url)
    time.sleep(4)
