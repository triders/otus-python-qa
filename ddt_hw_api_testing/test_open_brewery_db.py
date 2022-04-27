import pytest
import requests
import urllib.parse as up

BASE_URL = "https://api.openbrewerydb.org"
ENDPOINTS = {
    "get brewery": BASE_URL + "/breweries/{brewery_id}",
    "list breweries": BASE_URL + "/breweries",
    "list breweries in city": BASE_URL + "/breweries?by_city={city_name}",
    "search brewery by query": BASE_URL + "/breweries/search?query={query}",
    "autocomplete brewery name": BASE_URL + "/breweries/autocomplete?query={query}",
}


def get_breweries_attribute(brewery_id=None, city=None, website_url=None, name=None):
    r = requests.get(ENDPOINTS["list breweries"])
    breweries_list = r.json()

    if brewery_id:
        for brewery in breweries_list:
            yield brewery["id"]

    elif city:
        for brewery in breweries_list:
            yield up.quote(brewery["city"])

    elif website_url:
        for brewery in breweries_list:
            if brewery["website_url"] == "http://www.cyclersbrewing.com":
                yield pytest.param("http://www.cyclersbrewing.com]", marks=pytest.mark.xfail(strict=True))
            else:
                yield brewery["website_url"]

    elif name:
        for brewery in breweries_list:
            yield brewery["name"]


@pytest.mark.parametrize("brewery_id", get_breweries_attribute(brewery_id=True))
def test_get_brewery_by_id(brewery_id):
    r = requests.get(ENDPOINTS["get brewery"].format(brewery_id=brewery_id))
    assert r.status_code == 200

    brewery = r.json()
    assert brewery["id"] == brewery_id


@pytest.mark.parametrize("city", get_breweries_attribute(city=True))
def test_filter_breweries_by_city(city):
    """Test filter breweries by city works.
    https://api.openbrewerydb.org/breweries?by_city=san_diego"""
    r = requests.get(ENDPOINTS["list breweries in city"].format(city_name=city))
    breweries = r.json()
    for brewery in breweries:
        assert (up.unquote(city).lower() in brewery["city"].lower())


@pytest.mark.parametrize("website_url", get_breweries_attribute(website_url=True))
def test_if_brewery_has_website_it_must_respond_200(website_url):
    """Test that website responds with status 200.
       We ignore breweries with 'website_url': None" in this tests"""
    if website_url:
        brewery_website = requests.get(website_url)
        assert brewery_website.status_code == 200


@pytest.mark.parametrize("query", get_breweries_attribute(name=True))
def test_search_breweries_by_name(query):
    """Test search breweries by query.
       https://api.openbrewerydb.org/breweries/search?query=dog"""
    r = requests.get(ENDPOINTS["search brewery by query"].format(query=up.quote(query)))
    assert r.status_code == 200

    search_results_breweries = r.json()
    assert search_results_breweries
    assert query in search_results_breweries[0]["name"]


@pytest.mark.parametrize("query", ["pub", "dog", "cycle"])
def test_autocomplete_brewery_name(query):
    r = requests.get(ENDPOINTS["autocomplete brewery name"].format(query=query))
    assert r.status_code == 200

    breweries = r.json()
    for brewery in breweries:
        assert query in brewery["name"].lower()
