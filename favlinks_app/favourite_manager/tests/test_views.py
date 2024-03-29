from config.helpers import BaseTestCase
from rest_framework.reverse import reverse

from favourite_manager.models import FavouriteCategory


class FavouriteManagerBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.given_a_new_user()
        self.other_user = self.given_a_new_user(username="other")
        self.other_tag = self.given_a_favourite_tag(user=self.other_user)
        self.other_category = self.given_a_favourite_category(user=self.other_user)


class FavouriteTagTestCase(FavouriteManagerBaseTestCase):

    def setUp(self):
        super().setUp()

    def test_list_favourite_tags_given_user_success(self):
        pass

    def test_list_favourite_tags_unauthorized_given_not_logged_in(self):
        pass


class FavouriteCategoryTestCase(FavouriteManagerBaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_category_1 = self.given_a_favourite_category(
            user=self.user, name="category 1"
        )
        self.user_category_2 = self.given_a_favourite_category(
            user=self.user, name="category 2"
        )

    def assertCategoryInResponse(self, response):
        for category in response:
            self.assertIn("id", category)
            self.assertIn("user", category)
            self.assertIn("name", category)
            self.assertIn("created_at", category)
            self.assertIn("updated_at", category)

    def assertCategoryEqualsResponse(self, user, response):
        for category in response:
            category_obj = FavouriteCategory.objects.get(id=category["id"])
            self.assertEqual(user.id, category["user"])
            self.assertEqual(category_obj.user.id, category["user"])
            self.assertEqual(category_obj.name, category["name"])
            self.assertEqual(
                category_obj.created_at.strftime("%Y-%m-%d"),
                category["created_at"][0:10],
            )
            self.assertEqual(
                category_obj.updated_at.strftime("%Y-%m-%d"),
                category["updated_at"][0:10],
            )

    def test_list_favourite_categories_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_gets_json()
        self.assertCategoryInResponse(self.response_json)
        self.assertCategoryEqualsResponse(self.user, self.response_json)

    def test_list_favourite_categories_unauthorized_given_not_logged_in(self):
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_gets_json()
        self.assertResponseForbidden()


class FavouriteUrlTestCase(FavouriteManagerBaseTestCase):

    def setUp(self):
        super().setUp()

    def test_list_favourite_url_given_user_success(self):
        pass

    def test_list_favourite_url_unauthorized_given_not_logged_in(self):
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_gets_json()
        self.assertResponseNotAuthorized()
