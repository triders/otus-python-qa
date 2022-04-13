import pytest
import requests

BASE_URL = "https://dog.ceo/api"

ENDPOINTS = {
    "list all breeds": BASE_URL + "/breeds/list/all",
    "pick random picture for breed": BASE_URL + "/breed/{breed}/images/random",
    "pick random picture for sub breed": BASE_URL + "/breed/{breed}/{sub_breed}/images/random",
    "get all pictures of given breed": BASE_URL + "/breed/{breed}/images",
    "get all pictures of given sub breed": BASE_URL + "/breed/{breed}/{sub_breed}/images"
}


def get_breeds():
    r = requests.get(ENDPOINTS["list all breeds"]).json()
    breeds = r["message"]
    for breed in breeds:
        yield breed


def get_breeds_which_have_sub_breeds():
    r = requests.get(ENDPOINTS["list all breeds"]).json()
    breeds = r["message"]
    print(breeds)
    while breeds:
        breed = breeds.popitem()
        if breed[1]:
            yield breed


@pytest.mark.parametrize("breed", get_breeds())
def test_random_picture_pick_works_for_all_breeds(breed):
    """RANDOM IMAGE FROM A BREED COLLECTION
    https://dog.ceo/api/breed/hound/images/random
    Returns a random dog image from a breed, e.g. hound"""

    r = requests.get(ENDPOINTS["pick random picture for breed"].format(breed=breed))
    assert r.status_code == 200

    breeds = r.json()
    assert breeds["status"] == "success"


@pytest.mark.parametrize("breed, sub_breed_list", get_breeds_which_have_sub_breeds())
def test_random_picture_pick_works_for_all_sub_breeds_of_breed(breed, sub_breed_list):
    """SINGLE RANDOM IMAGE FROM A SUB BREED COLLECTION
    https://dog.ceo/api/breed/hound/afghan/images/random"""
    for sub_breed in sub_breed_list:
        r = requests.get(ENDPOINTS["pick random picture for sub breed"].format(breed=breed, sub_breed=sub_breed))
        assert r.status_code == 200
        assert r.json()["status"] == "success"


@pytest.mark.parametrize("breed", get_breeds())
def test_images_of_breed_in_results(breed):
    """Test that returned images of breed are correct (by checking if there is a name of the breed in the file names).
    https://dog.ceo/api/breed/hound/images
    Returns an array of all the images from a breed, e.g. hound"""

    r = requests.get(ENDPOINTS["get all pictures of given breed"].format(breed=breed))
    assert r.status_code == 200
    assert r.json()["status"] == "success"

    photos = r.json()["message"]
    for photo in photos:
        assert "https://images.dog.ceo/breeds/" + breed in photo, f"Requested photos of '{breed}', but got '{photo}'"


@pytest.mark.parametrize("breed, sub_breed_list", get_breeds_which_have_sub_breeds())
def test_images_of_sub_breed_in_results(breed, sub_breed_list):
    """Test that returned images of sub breed are correct
    (by checking if there is a name of the sub breed in the file names).
    https://dog.ceo/api/breed/hound/afghan/images
    Returns an array of all the images from a breed, e.g. hound afghan"""
    for sub_breed in sub_breed_list:
        r = requests.get(ENDPOINTS["get all pictures of given sub breed"].format(breed=breed, sub_breed=sub_breed))
        assert r.status_code == 200
        assert r.json()["status"] == "success"

        photos = r.json()["message"]
        for photo in photos:
            assert f"https://images.dog.ceo/breeds/{breed}-{sub_breed}" in photo, \
                f"Requested photos of '{breed}-{sub_breed}', but got '{photo}'"
