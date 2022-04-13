import pytest
import requests

BASE_URL = "https://dog.ceo/api"

ENDPOINTS = {
    "list all breeds": BASE_URL + "/breeds/list/all",
    "pick random picture for breed": BASE_URL + "/breed/{breed}/images/random"
}


def get_breed():
    r = requests.get(ENDPOINTS["list all breeds"]).json()
    breeds = r["message"]
    for breed in breeds:
        yield breed


@pytest.mark.parametrize("breed", get_breed())
def test_random_picture_pick_works_for_all_breeds(breed):
    """RANDOM IMAGE FROM A BREED COLLECTION
    https://dog.ceo/api/breed/hound/images/random
    Returns a random dog image from a breed, e.g. hound"""

    r = requests.get(ENDPOINTS["pick random picture for breed"].format(breed=breed))
    assert r.status_code == 200

    breeds = r.json()
    assert breeds["status"] == "success"

