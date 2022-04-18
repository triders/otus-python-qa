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

ALBUMS = {
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
        return super().put(USER["get user by id"].format(user_id=self.user_id)).json()

    def get_user_albums(self):
        return super().get(USER["get user's albums"].format(user_id=self.user_id)).json()


def validate_json_schema_for_fake_api_items(create_user=None, get_user=None):
    v = cerberus.Validator()
    create_user_response_schema = {
        'body': {"type": "string"}, 'id': {"type": "integer"},
        'title': {"type": "string"}, 'userId': {"type": "integer"}
    }
    get_user_by_id_schema = {
        'id': {"type": "integer"}, 'name': {"type": "string"}, 'username': {"type": "string"},
        'email': {"type": "string"}, 'address': {"type": "dict"}, 'phone': {"type": "string"},
        'website': {"type": "string"}, 'company': {"type": "dict"}
    }
    if create_user:
        return v.validate(create_user, create_user_response_schema)
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

        for (k, v) in ALBUMS.items():
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
        user = User().create()
        assert validate_json_schema_for_fake_api_items(create_user=user)

    @pytest.mark.parametrize("user_id", range(1, 11))
    def test_get_user_by_id(self, user_id):
        user = User(user_id=user_id).get()
        assert validate_json_schema_for_fake_api_items(get_user=user)
        assert user["id"] == user_id
