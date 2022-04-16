import cerberus
import requests

RESOURCE = {
    "create new resource": "/posts",
    "get resource by id": "/posts/{resource_id}",
    "get all comments of resource": "/posts/{resource_id}/comments",
    "get all resources": "/posts",
}

ALBUMS = {
    "create new album": "/albums",
    "get album by id": "/user/{album_id}",
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

        url = self.base_url + endpoint
        # print(url)
        return requests.post(url, json=body, headers=headers)

    def put(self, endpoint, body=None, headers=None):
        if body is None:
            body = self.default_body
        if headers is None:
            headers = self.default_headers

        url = self.base_url + endpoint
        # print(url)
        return requests.put(url, json=body, headers=headers)

    def create(self, endpoint, body=None, headers=None):
        return self.post(endpoint, body=body, headers=headers)

    def update(self, endpoint, body=None, headers=None):
        return self.put(endpoint, body=body, headers=headers)


class User(FakeApi):
    USER = {
        "create new user": "/users",
        "get user by id": "/user/{user_id}",
        "get all users": "/users",
        "get user's posts": "/users/{user_id}/posts",
        "get user's todos": "/users/{user_id}/todos",
        "get user's albums": "/users/{user_id}/albums",
    }

    def create(self, **kwargs):
        return super().create(endpoint=self.USER["create new user"], **kwargs).json()

    def update_user(self, **kwargs):
        return super().put(self.USER["get user by id"].format(user_id=self.user_id)).json()

    def get_user_albums(self):
        return super().get(self.USER["get user's albums"].format(user_id=self.user_id)).json()


def validate_json_schema_for_fake_api_items(user=None):
    v = cerberus.Validator()
    base_schema = {'body': {"type": "string"},
                   'id': {"type": "integer"},
                   'title': {"type": "string"},
                   'userId': {"type": "integer"}
                   }

    if user:
        return v.validate(user, base_schema)


class TestUsers:

    def test_create_user(self):
        user = User().create()
        assert validate_json_schema_for_fake_api_items(user)
