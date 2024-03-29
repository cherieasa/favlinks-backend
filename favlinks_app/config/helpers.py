from rest_framework import status
from rest_framework.test import APITestCase

from favourite_manager.models import FavouriteCategory, FavouriteTag, FavouriteUrl
from user_manager.models import User


class BaseTestCase(APITestCase):
    def setUp(self):
        self.current_user = None
        self.url = None
        self.query_params = None
        self.response = None
        self.response_json = None

    def given_logged_in_user(self, user):
        self.current_user = user
        self.client.force_login(user)

    def given_query_params(self, query_params):
        self.query_params = query_params

    def given_url(self, url):
        self.url = url

    def given_a_new_user(self, username="test", password="Test1234++"):
        return User.objects.create_user(username=username, password=password)

    def given_a_favourite_tag(self, user, name="tag") -> FavouriteTag:
        return FavouriteTag.objects.create(user=user, name=name)

    def given_a_favourite_category(self, user, name="category") -> FavouriteCategory:
        return FavouriteCategory.objects.create(user=user, name=name)

    def given_a_favourite_url(
        self, user, url="test.com", title="title", tags=None, categories=None
    ) -> FavouriteUrl:
        fav_url = FavouriteUrl.objects.create(user=user, url=url, title=title)
        if tags:
            fav_url.tags.set(tags)
        if categories:
            fav_url.categories.set(categories)

        return fav_url

    def when_user_gets_json(self):
        self.response = self.client.get(self.url, self.query_params, format="json")
        self.response_json = self.response.json()
        return self.response_json

    def assertResponseBadRequest(self):
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertResponseNotAuthorized(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertResponseForbidden(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
