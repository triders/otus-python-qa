import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def pytest_addoption(parser):
    parser.addoption('--base_url', action='store', default="http://192.168.0.105:8081/",
                     help="Opencart base url")

    parser.addoption('--browser_name', action='store', default="chrome",
                 help="Browser to run tests. Default is 'chrome'. Also available: 'safari', 'firefox', 'opera', 'yandex', 'edge'")


@pytest.fixture
def base_url(request):
    return request.config.getoption('--base_url')


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption('--browser_name')

    browser = None
    if browser_name == "chrome":
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
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
        raise ValueError(f"'{browser_name}' is not supported. Use 'chrome', 'safari', 'firefox', 'opera', 'yandex', 'edge'")

    yield browser

    browser.close()
