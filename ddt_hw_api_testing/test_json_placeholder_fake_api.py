import cerberus
import pytest
import requests

RESOURCE = {
    "create new resource": "/posts",
    "get resource by id": "/posts/{resource_id}",
    "get all comments of resource": "/posts/{resource_id}/comments",
    "get all resources": "/posts",
}

USER = {
    "create new user": "/users",
    "get user by id": "/users/{user_id}",
    "get all users": "/users",
    "get user's posts": "/users/{user_id}/posts",
    "get user's todos": "/users/{user_id}/todos",
    "get user's albums": "/users/{user_id}/albums",
}

ALBUM = {
    "create new album": "/albums",
    "get album by id": "/albums/{album_id}",
    "get all albums": "/albums",
    "get all photos from album": "/albums/{album_id}/photos",
}


class FakeApi:

    def __init__(self,
                 base_url="https://jsonplaceholder.typicode.com",
                 resource_id=None,
                 user_id=None,
                 album_id=None,
                 comment_id=None):

        self.base_url = base_url
        self.resource_id = resource_id
        self.user_id = user_id
        self.album_id = album_id
        self.comment_id = comment_id
        self.default_headers = {'Content-type': 'application/json; charset=UTF-8'}
        self.default_body = {'title': 'default_title', 'body': 'default_body', 'userId': 1}

    def get(self, endpoint):
        return requests.get(self.base_url + endpoint)

    def post(self, endpoint, body=None, headers=None):
        if body is None:
            body = self.default_body
        if headers is None:
            headers = self.default_headers
        return requests.post(self.base_url + endpoint, json=body, headers=headers)

    def put(self, endpoint, body=None, headers=None):
        if body is None:
            body = self.default_body
        if headers is None:
            headers = self.default_headers
        return requests.put(self.base_url + endpoint, json=body, headers=headers)

    def create(self, endpoint, body=None, headers=None):
        return self.post(endpoint, body=body, headers=headers)

    def update(self, endpoint, body=None, headers=None):
        return self.put(endpoint, body=body, headers=headers)


class User(FakeApi):

    def create(self, **kwargs):
        return super().create(endpoint=USER["create new user"], **kwargs).json()

    def get(self, endpoint=USER["get user by id"]):
        return super().get(endpoint=endpoint.format(user_id=self.user_id)).json()

    def update_user(self, **kwargs):
        return super().update(USER["get user by id"].format(user_id=self.user_id), **kwargs).json()

    def get_user_albums(self):
        return super().get(USER["get user's albums"].format(user_id=self.user_id)).json()


class Album(FakeApi):

    def create(self, **kwargs):
        return super().create(endpoint=ALBUM["create new album"], **kwargs).json()

    def get(self, endpoint=ALBUM["get album by id"]):
        return super().get(endpoint=endpoint.format(album_id=self.album_id)).json()

    def update_album(self, **kwargs):
        return super().update(ALBUM["get album by id"].format(album_id=self.album_id), **kwargs).json()


class Resource(FakeApi):

    def create(self, **kwargs):
        return super().create(endpoint=RESOURCE["create new resource"], **kwargs).json()

    def get(self, endpoint=RESOURCE["get resource by id"]):
        return super().get(endpoint=endpoint.format(resource_id=self.resource_id)).json()

    def update_resource(self, **kwargs):
        return super().update(RESOURCE["get resource by id"].format(resource_id=self.resource_id), **kwargs).json()


def validate_json_schema_for_fake_api_items(base_schema=None, get_user=None):
    v = cerberus.Validator()
    base_item_response_schema = {
        'body': {"type": "string"}, 'id': {"type": "integer"},
        'title': {"type": "string"}, 'userId': {"type": "integer"}
    }
    get_user_by_id_schema = {
        'id': {"type": "integer"}, 'name': {"type": "string"}, 'username': {"type": "string"},
        'email': {"type": "string"}, 'address': {"type": "dict"}, 'phone': {"type": "string"},
        'website': {"type": "string"}, 'company': {"type": "dict"}
    }
    if base_schema:
        return v.validate(base_schema, base_item_response_schema)
    elif get_user:
        return v.validate(get_user, get_user_by_id_schema)


@pytest.mark.smoke
class TestFakeApiHealthCheck:

    def test_user_endpoints_health_check(self):
        """ensure that GET on each USER endpoint returns 200"""

        for (k, v) in USER.items():
            if "{user_id}" in v:
                r = FakeApi().get(v.format(user_id=1))
            else:
                r = FakeApi().get(v)
            assert r.status_code == 200

    def test_albums_endpoints_health_check(self):
        """ensure that GET on each ALBUM endpoint returns 200"""

        for (k, v) in ALBUM.items():
            if "{album_id}" in v:
                r = FakeApi().get(v.format(album_id=1))
            else:
                r = FakeApi().get(v)
            assert r.status_code == 200

    def test_resources_endpoints_health_check(self):
        """ensure that GET on each RESOURCE endpoint returns 200"""

        for (k, v) in RESOURCE.items():
            if "{resource_id}" in v:
                r = FakeApi().get(v.format(resource_id=1))
            else:
                r = FakeApi().get(v)
            assert r.status_code == 200


class TestUsers:

    def test_create_user(self):
        created_user = User().create()
        assert validate_json_schema_for_fake_api_items(base_schema=created_user)

    def test_create_custom_user(self):
        custom_user = {'title': 'custom_user_title', 'body': 'custom_user_body',
                       'userId': 4}  # unable to set 'id'
        created_user = Album().create(body=custom_user)
        assert validate_json_schema_for_fake_api_items(base_schema=created_user)
        assert created_user["title"] == custom_user["title"]
        assert created_user["body"] == custom_user["body"]
        assert created_user["userId"] == custom_user["userId"]

    @pytest.mark.parametrize("user_id", range(1, 11))
    def test_get_user_by_id(self, user_id):
        user = User(user_id=user_id).get()
        assert validate_json_schema_for_fake_api_items(get_user=user)
        assert user["id"] == user_id

    @pytest.mark.parametrize("user_id", range(1, 11))
    def test_update_user(self, user_id):
        twin_user_1 = User(user_id=user_id).get()
        twin_user_2 = User(user_id=user_id).update_user(body={"name": "John", "surname": "Malkovich"})
        assert twin_user_1 != twin_user_2
        assert twin_user_2 == {"id": user_id, "name": "John", "surname": "Malkovich"}


class TestAlbums:

    def test_create_album(self):
        created_album = Album().create()
        assert validate_json_schema_for_fake_api_items(base_schema=created_album)

    def test_create_custom_album(self):
        custom_album = {'title': 'custom_album_title', 'body': 'custom_album_body', 'userId': 4}  # unable to set 'id'
        created_album = Album().create(body=custom_album)
        assert validate_json_schema_for_fake_api_items(base_schema=created_album)
        assert created_album["title"] == custom_album["title"]
        assert created_album["body"] == custom_album["body"]
        assert created_album["userId"] == custom_album["userId"]

    @pytest.mark.parametrize("album_id", range(1, 101))
    def test_get_album_by_id(self, album_id):
        album = Album(album_id=album_id).get()
        assert validate_json_schema_for_fake_api_items(base_schema=album)
        assert album["id"] == album_id


class TestResources:

    def test_create_resource(self):
        created_resource = Album().create()
        assert validate_json_schema_for_fake_api_items(base_schema=created_resource)

    def test_create_custom_resource(self):
        custom_resource = {'title': 'custom_resource_title', 'body': 'custom_resource_body',
                           'userId': 4}  # unable to set 'id'
        created_resource = Resource().create(body=custom_resource)
        assert validate_json_schema_for_fake_api_items(base_schema=created_resource)
        assert created_resource["title"] == custom_resource["title"]
        assert created_resource["body"] == custom_resource["body"]
        assert created_resource["userId"] == custom_resource["userId"]

    @pytest.mark.parametrize("resource_id", range(1, 101))
    def test_get_resource_by_id(self, resource_id):
        resource = Resource(resource_id=resource_id).get()
        assert validate_json_schema_for_fake_api_items(base_schema=resource)
        assert resource["id"] == resource_id
