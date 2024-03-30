from django.utils.http import urlencode
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
        self, user, url="test.com", title="title", category=None, tags=None
    ) -> FavouriteUrl:
        fav_url = FavouriteUrl.objects.create(user=user, url=url, title=title)
        if tags:
            fav_url.tags.set(tags)
        if category:
            fav_url.category = category
            fav_url.save()

        return fav_url

    def when_user_gets_json(self):
        self.response = self.client.get(self.url, self.query_params, format="json")
        self.response_json = self.response.json()
        return self.response_json

    def when_user_posts(self, data, format="json"):
        if self.query_params is not None:
            r = {
                "QUERY_STRING": urlencode(self.query_params, doseq=True),
            }
            self.response = self.client.post(self.url, data, format=format, **r)
        else:
            self.response = self.client.post(self.url, data, format=format)

    def when_user_posts_and_gets_json(self, data, format="json"):
        self.when_user_posts(data, format)
        self.response_json = self.response.json()
        return self.response_json

    def when_user_puts_and_gets_json(self, data, format="json"):
        if self.query_params is not None:
            r = {
                "QUERY_STRING": urlencode(self.query_params, doseq=True),
            }
            self.response = self.client.put(self.url, data, format=format, **r)
        else:
            self.response = self.client.put(self.url, data, format=format)
        self.response_json = self.response.json()
        return self.response_json

    def assertResponseSuccess(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def assertResponseCreated(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def assertResponseBadRequest(self):
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertResponseNotAuthorized(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertResponseForbidden(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def assertResponseNotFound(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)
