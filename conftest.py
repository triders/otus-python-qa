import os
import pytest
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
START_LOGGER = logging.getLogger("file_logger_start")


def pytest_addoption(parser):
    parser.addoption('--base_url', action='store', default="http://localhost:8081/",
                     help="Opencart base url")

    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Browser to run tests. Default is 'chrome'. "
                          "Also available: 'safari', 'firefox', 'opera', 'yandex', 'edge'")

    parser.addoption('--headless', action='store_true')

    parser.addoption('--username', action='store', default="user")

    parser.addoption('--password', action='store', default="bitnami")


@pytest.fixture
def base_url(request):
    base_url = request.config.getoption('--base_url')
    if base_url[-1] != "/":
        base_url += "/"
    return base_url


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption('--browser_name')
    headless = request.config.getoption('--headless')

    browser = None
    options = None
    if browser_name == "chrome":
        if headless:
            options = ChromiumOptions()
            options.headless = True
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    elif browser_name == "safari":
        browser = webdriver.Safari()
    elif browser_name == "firefox":
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "opera":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('w3c', True)
        browser = webdriver.Opera(executable_path=OperaDriverManager().install(), options=options)
    elif browser_name == "yandex":
        browser = webdriver.Chrome(executable_path="./drivers/yandexdriver")
    elif browser_name == "edge":
        browser = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
    else:
        raise ValueError(
            f"'{browser_name}' is not supported. Use 'chrome', 'safari', 'firefox', 'opera', 'yandex' or 'edge'")

    browser.maximize_window()

    yield browser

    browser.close()


@pytest.fixture(scope="function")
def user(request):
    username = request.config.getoption('--username')
    password = request.config.getoption('--password')
    yield {"username": username, "password": password}


@pytest.fixture(scope="function", autouse=True)
def log():
    current_test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    START_LOGGER.debug(f"{current_test_name}")
