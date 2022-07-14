import pytest


def pytest_addoption(parser):
    parser.addoption('--url', action='store', default="https://ya.ru",
                     help="We request this URL to validate status code of response")
    parser.addoption('--status_code', action='store', default="200",
                     help="Expected status code")


@pytest.fixture
def cmdopt(request):
    return {"url": request.config.getoption('--url'), "status_code": int(request.config.getoption('--status_code'))}
