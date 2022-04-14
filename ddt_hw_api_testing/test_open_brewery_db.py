import pytest
import requests
import urllib.parse as up


BASE_URL = "https://api.openbrewerydb.org"
ENDPOINTS = {
    "list breweries": BASE_URL + "/breweries",
    "list breweries in city": BASE_URL + "/breweries?by_city={city_name}",
    "search brewery by query": BASE_URL + "/breweries/search?query={query}",
}


def get_breweries_attribute(city=None, website_url=None, name=None):

    r = requests.get(ENDPOINTS["list breweries"])
    breweries_list = r.json()

    if city:
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


breweries = [
    {'id': 'banjo-brewing-fayetteville', 'name': 'Banjo Brewing', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Fayetteville', 'state': 'West Virginia', 'county_province': None,
     'postal_code': '25840', 'country': 'United States', 'longitude': None, 'latitude': None, 'phone': '3042164231',
     'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'barrel-brothers-brewing-company-windsor', 'name': 'Barrel Brothers Brewing Company',
     'brewery_type': 'micro', 'street': '399 Business Park Ct Ste 506', 'address_2': None, 'address_3': None,
     'city': 'Windsor', 'state': 'California', 'county_province': None, 'postal_code': '95492-6652',
     'country': 'United States', 'longitude': None, 'latitude': None, 'phone': '7076969487',
     'website_url': 'http://www.barrelbrothersbrewing.com', 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'bay-brewing-company-miami', 'name': 'Bay Brewing Company', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Miami', 'state': 'Florida', 'county_province': None,
     'postal_code': '33130-3488', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': '18134763767', 'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'bent-shovel-brewing-oregon-city', 'name': 'Bent Shovel Brewing', 'brewery_type': 'micro',
     'street': '21678 S Latourette Rd', 'address_2': None, 'address_3': None, 'city': 'Oregon City', 'state': 'Oregon',
     'county_province': None, 'postal_code': '97045-9453', 'country': 'United States', 'longitude': None,
     'latitude': None, 'phone': '5038980220', 'website_url': 'http://www.bentshovelbrewing.com',
     'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'snow-belt-brew-chardon', 'name': 'Snow Belt Brew', 'brewery_type': 'micro', 'street': '9511 Kile Rd',
     'address_2': None, 'address_3': None, 'city': 'Chardon', 'state': 'Ohio', 'county_province': None,
     'postal_code': '44024', 'country': 'United States', 'longitude': None, 'latitude': None, 'phone': None,
     'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'boring-brewing-co-llc-boring', 'name': 'Boring Brewing Co., LLC', 'brewery_type': 'micro',
     'street': '29300 SE Haley Road Ste B', 'address_2': None, 'address_3': None, 'city': 'Boring', 'state': 'Oregon',
     'county_province': None, 'postal_code': '97009', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': '5034278619', 'website_url': 'http://www.boringbrewing.com', 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'brubakers-brewery-and-pub-sylvania', 'name': "Brubaker's Brewery & Pub", 'brewery_type': 'planning',
     'street': None, 'address_2': None, 'address_3': None, 'city': 'Sylvania', 'state': 'Ohio', 'county_province': None,
     'postal_code': '43560-9586', 'country': 'United States', 'longitude': None, 'latitude': None, 'phone': None,
     'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'camino-brewing-co-llc-san-jose', 'name': 'Camino Brewing Co LLC', 'brewery_type': 'micro',
     'street': '718 S 1st St', 'address_2': None, 'address_3': None, 'city': 'San Jose', 'state': 'California',
     'county_province': None, 'postal_code': '95113', 'country': 'United States', 'longitude': '-121.8823478',
     'latitude': '37.32530178', 'phone': None, 'website_url': 'http://www.caminobrewing.com',
     'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'cape-ann-lanes-gloucester', 'name': 'Cape Ann Lanes', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Gloucester', 'state': 'Massachusetts', 'county_province': None,
     'postal_code': '01930-2256', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': '9788799714', 'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'center-pivot-quinter', 'name': 'Center Pivot', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Quinter', 'state': 'Kansas', 'county_province': None,
     'postal_code': '67752', 'country': 'United States', 'longitude': None, 'latitude': None, 'phone': '7857548344',
     'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'cerveceria-del-pueblo-pasadena', 'name': 'Cerveceria Del Pueblo', 'brewery_type': 'planning',
     'street': None, 'address_2': None, 'address_3': None, 'city': 'Pasadena', 'state': 'California',
     'county_province': None, 'postal_code': '91105-1822', 'country': 'United States', 'longitude': '-118.1444779',
     'latitude': '34.1476452', 'phone': None, 'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'circle-9-brewing-san-diego', 'name': 'Circle 9 Brewing', 'brewery_type': 'micro',
     'street': '7292 Opportunity Rd Ste C', 'address_2': None, 'address_3': None, 'city': 'San Diego',
     'state': 'California', 'county_province': None, 'postal_code': '92111-2223', 'country': 'United States',
     'longitude': None, 'latitude': None, 'phone': '8586342537', 'website_url': 'http://www.circle9brewing.com',
     'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'cerveza-guajira-miami', 'name': 'Cerveza Guajira', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Miami', 'state': 'Florida', 'county_province': None,
     'postal_code': '33137', 'country': 'United States', 'longitude': None, 'latitude': None, 'phone': '3056005692',
     'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'common-john-brewing-co-manchester', 'name': 'Common John Brewing Co', 'brewery_type': 'planning',
     'street': None, 'address_2': None, 'address_3': None, 'city': 'Manchester', 'state': 'Tennessee',
     'county_province': None, 'postal_code': '37355-6064', 'country': 'United States', 'longitude': None,
     'latitude': None, 'phone': '9314090630', 'website_url': 'http://www.commonjohnbc.com',
     'updated_at': '2021-10-23T02:24:55.243Z', 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'corner-pub-reedsburg', 'name': 'Corner Pub', 'brewery_type': 'brewpub', 'street': '100 E Main St Lowr',
     'address_2': None, 'address_3': None, 'city': 'Reedsburg', 'state': 'Wisconsin', 'county_province': None,
     'postal_code': '53959-1967', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': '6085248989', 'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'cyclers-brewing-montgomery', 'name': "Cycler's Brewing", 'brewery_type': 'micro',
     'street': '17105 Osborn Rd', 'address_2': None, 'address_3': None, 'city': 'Montgomery', 'state': 'Texas',
     'county_province': None, 'postal_code': '77356', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': '7135692485', 'website_url': 'http://www.cyclersbrewing.com', 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'dented-face-brewing-company-delta', 'name': 'Dented Face Brewing Company', 'brewery_type': 'planning',
     'street': None, 'address_2': None, 'address_3': None, 'city': 'Delta', 'state': 'Colorado',
     'county_province': None, 'postal_code': '81416', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': None, 'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'}, {'id': 'dfamle-enterprises-lp-dba-four-sons-brewing-huntington-beach',
                                                 'name': 'Dfamle Enterprises LP (DBA Four Sons Brewing)',
                                                 'brewery_type': 'micro', 'street': '18421 Gothard St Ste 100',
                                                 'address_2': None, 'address_3': None, 'city': 'Huntington Beach',
                                                 'state': 'California', 'county_province': None,
                                                 'postal_code': '92648-1235', 'country': 'United States',
                                                 'longitude': None, 'latitude': None, 'phone': None,
                                                 'website_url': None, 'updated_at': '2021-10-23T02:24:55.243Z',
                                                 'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'devout-brewing-export', 'name': 'Devout Brewing', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Export', 'state': 'Pennsylvania', 'county_province': None,
     'postal_code': '15632', 'country': 'United States', 'longitude': None, 'latitude': None, 'phone': None,
     'website_url': 'http://www.devoutbrewingco.com', 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'},
    {'id': 'dirt-road-brewing-corvallis', 'name': 'Dirt Road Brewing', 'brewery_type': 'planning', 'street': None,
     'address_2': None, 'address_3': None, 'city': 'Corvallis', 'state': 'Oregon', 'county_province': None,
     'postal_code': '97330-3005', 'country': 'United States', 'longitude': None, 'latitude': None,
     'phone': '5415984221', 'website_url': 'http://dirtroadbrewing.com', 'updated_at': '2021-10-23T02:24:55.243Z',
     'created_at': '2021-10-23T02:24:55.243Z'}]
