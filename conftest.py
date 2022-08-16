import os
import pytest
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.opera.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER_START = logging.getLogger("file_logger_start")
LOGGER_ENV = logging.getLogger("file_logger_env")


def pytest_addoption(parser):
    parser.addoption('--base_url', action='store', default="http://localhost",
                     help="Opencart base url")
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Browser to run tests. Default is 'chrome'. "
                          "Also available: 'safari', 'firefox', 'opera', 'yandex', 'edge'")
    parser.addoption('--headless', action='store_true')
    parser.addoption("--executor", action="store", default="local",
                     help="Specify IP of Selenoid. Or 'local' to run without Selenoid. Default is 'localhost'")
    parser.addoption("--mobile", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--videos", action="store_true")
    parser.addoption("--bv", default=None)
    parser.addoption('--username', action='store')
    parser.addoption('--password', action='store')


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
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--bv")
    vnc = request.config.getoption("--vnc")
    videos = request.config.getoption("--videos")

    browser = None
    options = None
    if executor == "local":
        if browser_name == "chrome":
            options = None
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

    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        caps = {
            "browserName": browser_name,
            "browserVersion": version,
            # # "screenResolution": "1280x720",
            "name": "Timofei",
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": videos
            },
            'acceptSslCerts': True,
            'acceptInsecureCerts': True,
            'timeZone': 'Europe/Moscow',
            'goog:chromeOptions': {}
        }
        options = None
        if browser_name == "opera":
            options = Options()
            options.add_experimental_option('w3c', True)

        browser = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps,
            options=options
        )

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
    LOGGER_START.debug(f"{current_test_name}")


@pytest.fixture(scope="session", autouse=True)
def log_env(request):
    browser_name = request.config.getoption('--browser_name')
    headless = request.config.getoption('--headless')
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--bv")
    vnc = request.config.getoption("--vnc")

    if executor == "local":
        LOGGER_ENV.info(f"Running tests locally in {browser_name}")
    else:
        LOGGER_ENV.info(f"Running tests on http://{executor}/wd/hub via Selenoid in {browser_name} "
                        f"(parameters: headless={headless}, vnc={vnc}, browser version={version})")
