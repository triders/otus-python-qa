import requests


def test_validate_response_status_code(cmdopt):
    url = cmdopt["url"]
    expected_status_code = cmdopt["status_code"]
    r = requests.get(url)
    assert r.status_code == expected_status_code, \
        f"Expected status code ='{expected_status_code}', but request to '{url}' returned '{r.status_code}'"
