import json

from config.graphql_root_schema import schema
from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token


class UserUnitTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "http://localhost:8081/graphql"
    USERS_QUERY = "query {users {id, name}}"

    def setUp(self):
        user = get_user_model().objects.create(name="test", email="test@test.com")
        token = get_token(user)
        self.headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

    def test_userrs_response(self):
        response = self.query(self.USERS_QUERY, headers=self.headers,)

        content = json.loads(response.content)
        self.assertEqual(content["data"]["users"][0]["name"], "test")
