from config.helpers import BaseTestCase
from datetime import timedelta
from django.utils import timezone
from rest_framework.reverse import reverse
from unittest.mock import patch

from favourite_manager.models import (
    FavouriteCategory,
    FavouriteTag,
    FavouriteUrl,
    ValidUrl,
)


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
        self.user_tag_1 = self.given_a_favourite_tag(user=self.user, name="tag 1")
        self.user_tag_2 = self.given_a_favourite_tag(user=self.user, name="tag 2")

    def assertTagInResponse(self, response):
        for tag in response:
            self.assertIn("id", tag)
            self.assertIn("user", tag)
            self.assertIn("name", tag)
            self.assertIn("created_at", tag)
            self.assertIn("updated_at", tag)

    def assertTagEqualsResponse(self, user, response):
        for tag in response:
            tag_obj = FavouriteTag.objects.get(id=tag["id"])
            self.assertEqual(user.id, tag["user"])
            self.assertEqual(tag_obj.user.id, tag["user"])
            self.assertEqual(tag_obj.name, tag["name"])
            self.assertEqual(
                tag_obj.created_at.strftime("%Y-%m-%d"),
                tag["created_at"][0:10],
            )
            self.assertEqual(
                tag_obj.updated_at.strftime("%Y-%m-%d"),
                tag["updated_at"][0:10],
            )

    def test_list_favourite_categories_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertTagInResponse(self.response_json)
        self.assertTagEqualsResponse(self.user, self.response_json)

    def test_list_favourite_categories_forbidden_given_not_logged_in(self):
        self.given_url(reverse("favouritetag-list"))
        self.when_user_gets_json()
        self.assertResponseForbidden()

    def test_retrieve_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertIn("id", self.response_json)
        self.assertIn("user", self.response_json)
        self.assertIn("name", self.response_json)
        self.assertIn("created_at", self.response_json)
        self.assertIn("updated_at", self.response_json)
        self.assertEqual(self.user.id, self.response_json["user"])
        self.assertEqual(self.user_tag_1.user.id, self.response_json["user"])
        self.assertEqual(self.user_tag_1.name, self.response_json["name"])
        self.assertEqual(
            self.user_tag_1.created_at.strftime("%Y-%m-%d"),
            self.response_json["created_at"][0:10],
        )
        self.assertEqual(
            self.user_tag_1.updated_at.strftime("%Y-%m-%d"),
            self.response_json["updated_at"][0:10],
        )

    def test_retrieve_non_existing_id(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritetag-detail", kwargs={"pk": "123123"}))
        self.when_user_gets_json()
        self.assertResponseNotFound()

    def test_retrieve_forbidden_given_not_logged_in(self):
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseForbidden()

    def test_retrieve_not_found_given_other_user(self):
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseNotFound()

    def test_create_success(self):
        tag_name = "new tag"
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritetag-list"))
        self.when_user_posts_and_gets_json(data={"name": tag_name})
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteTag.objects.filter(user=self.user, name=tag_name).count(),
            1,
        )

    def test_create_forbidden_given_not_logged_in(self):
        initial_count = FavouriteTag.objects.count()
        tag_name = "new tag"
        self.given_url(reverse("favouritetag-list"))
        self.when_user_posts_and_gets_json(data={"name": tag_name})
        self.assertResponseForbidden()
        self.assertEqual(initial_count, FavouriteTag.objects.count())

    def test_create_bad_request_given_duplicate_name(self):
        initial_count = FavouriteTag.objects.count()
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritetag-list"))
        self.when_user_posts_and_gets_json(data={"name": self.user_tag_1.name})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, FavouriteTag.objects.count())

    def test_create_bad_request_given_no_name(self):
        initial_count = FavouriteTag.objects.count()
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritetag-list"))
        self.when_user_posts_and_gets_json(data={"name": ""})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, FavouriteTag.objects.count())

    def test_update_forbidden_given_not_logged_in(self):
        updated_name = "updated"
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_puts_and_gets_json(data={"name": updated_name})
        self.assertResponseForbidden()
        self.user_tag_1.refresh_from_db()
        self.assertNotEqual(self.user_tag_1.name, updated_name)

    def test_update_not_found_given_other_user(self):
        updated_name = "updated"
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_puts_and_gets_json(data={"name": updated_name})
        self.assertResponseNotFound()
        self.user_tag_1.refresh_from_db()
        self.assertNotEqual(self.user_tag_1.name, updated_name)

    def test_delete_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_deletes()
        self.assertResponseNoContent()
        self.assertFalse(FavouriteTag.objects.filter(pk=self.user_tag_1.pk).exists())

    def test_delete_forbidden_given_not_logged_in(self):
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_deletes()
        self.assertResponseForbidden()
        self.assertTrue(FavouriteTag.objects.filter(pk=self.user_tag_1.pk).exists())

    def test_delete_not_found_given_non_existent(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritetag-detail", kwargs={"pk": "12312312"}))
        self.when_user_deletes()
        self.assertResponseNotFound()
        self.assertTrue(FavouriteTag.objects.filter(pk=self.user_tag_1.pk).exists())

    def test_delete_not_found_given_other_user(self):
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouritetag-detail", kwargs={"pk": self.user_tag_1.pk})
        )
        self.when_user_deletes()
        self.assertResponseNotFound()
        self.assertTrue(FavouriteTag.objects.filter(pk=self.user_tag_1.pk).exists())


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

    def test_list_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertCategoryInResponse(self.response_json)
        self.assertCategoryEqualsResponse(self.user, self.response_json)

    def test_list_forbidden_given_not_logged_in(self):
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_gets_json()
        self.assertResponseForbidden()

    def test_retrieve_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertIn("id", self.response_json)
        self.assertIn("user", self.response_json)
        self.assertIn("name", self.response_json)
        self.assertIn("created_at", self.response_json)
        self.assertIn("updated_at", self.response_json)
        self.assertEqual(self.user.id, self.response_json["user"])
        self.assertEqual(self.user_category_1.user.id, self.response_json["user"])
        self.assertEqual(self.user_category_1.name, self.response_json["name"])
        self.assertEqual(
            self.user_category_1.created_at.strftime("%Y-%m-%d"),
            self.response_json["created_at"][0:10],
        )
        self.assertEqual(
            self.user_category_1.updated_at.strftime("%Y-%m-%d"),
            self.response_json["updated_at"][0:10],
        )

    def test_retrieve_non_existing_id(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-detail", kwargs={"pk": "123123"}))
        self.when_user_gets_json()
        self.assertResponseNotFound()

    def test_retrieve_forbidden_given_not_logged_in(self):
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseForbidden()

    def test_retrieve_not_found_given_other_user(self):
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseNotFound()

    def test_create_success(self):
        category_name = "new category"
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_posts_and_gets_json(data={"name": category_name})
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteCategory.objects.filter(
                user=self.user, name=category_name
            ).count(),
            1,
        )

    def test_create_forbidden_given_not_logged_in(self):
        initial_count = FavouriteCategory.objects.count()
        category_name = "new category"
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_posts_and_gets_json(data={"name": category_name})
        self.assertResponseForbidden()
        self.assertEqual(initial_count, FavouriteCategory.objects.count())

    def test_create_bad_request_given_duplicate_name(self):
        initial_count = FavouriteCategory.objects.count()
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_posts_and_gets_json(data={"name": self.user_category_1.name})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, FavouriteCategory.objects.count())

    def test_create_bad_request_given_no_name(self):
        initial_count = FavouriteCategory.objects.count()
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-list"))
        self.when_user_posts_and_gets_json(data={"name": ""})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, FavouriteCategory.objects.count())

    def test_update_category_name_success(self):
        updated_name = "updated"
        self.given_logged_in_user(self.user)
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_puts_and_gets_json(data={"name": updated_name})
        self.assertResponseSuccess()
        self.user_category_1.refresh_from_db()
        self.assertEqual(self.user_category_1.name, updated_name)

    def test_update_forbidden_given_not_logged_in(self):
        updated_name = "updated"
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_puts_and_gets_json(data={"name": updated_name})
        self.assertResponseForbidden()
        self.user_category_1.refresh_from_db()
        self.assertNotEqual(self.user_category_1.name, updated_name)

    def test_update_not_found_given_other_user(self):
        updated_name = "updated"
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_puts_and_gets_json(data={"name": updated_name})
        self.assertResponseNotFound()
        self.user_category_1.refresh_from_db()
        self.assertNotEqual(self.user_category_1.name, updated_name)

    def test_delete_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_deletes()
        self.assertResponseNoContent()
        self.assertFalse(
            FavouriteCategory.objects.filter(pk=self.user_category_1.pk).exists()
        )

    def test_delete_forbidden_given_not_logged_in(self):
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_deletes()
        self.assertResponseForbidden()
        self.assertTrue(
            FavouriteCategory.objects.filter(pk=self.user_category_1.pk).exists()
        )

    def test_delete_not_found_given_non_existent(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouritecategory-detail", kwargs={"pk": "12312312"}))
        self.when_user_deletes()
        self.assertResponseNotFound()
        self.assertTrue(
            FavouriteCategory.objects.filter(pk=self.user_category_1.pk).exists()
        )

    def test_delete_not_found_given_other_user(self):
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouritecategory-detail", kwargs={"pk": self.user_category_1.pk})
        )
        self.when_user_deletes()
        self.assertResponseNotFound()
        self.assertTrue(
            FavouriteCategory.objects.filter(pk=self.user_category_1.pk).exists()
        )


class FavouriteUrlTestCase(FavouriteManagerBaseTestCase):
    def setUp(self):
        super().setUp()
        self.tag = self.given_a_favourite_tag(self.user, name="User Tag 1")
        self.category = self.given_a_favourite_category(
            self.user, name="User Category 1"
        )
        self.favourite_url_1 = self.given_a_favourite_url(
            self.user, category=self.category, tags=[self.tag]
        )
        self.favourite_url_2 = self.given_a_favourite_url(
            self.user, title="google", url="google.com", tags=[self.tag]
        )
        self.other_favourite_url = self.given_a_favourite_url(
            self.other_user,
            url="google.com",
            tags=[self.other_tag],
            category=self.other_category,
        )

    def get_favourite_url_count(self):
        return FavouriteUrl.objects.count()

    def assertFavUrlInResponse(self, response):
        for favurl in response:
            self.assertIn("id", favurl)
            self.assertIn("user", favurl)
            self.assertIn("title", favurl)
            self.assertIn("created_at", favurl)
            self.assertIn("updated_at", favurl)

            if "category" in favurl and favurl["category"]:
                self.assertIn("id", favurl["category"])
                self.assertIn("user", favurl["category"])
                self.assertIn("name", favurl["category"])
                self.assertIn("created_at", favurl["category"])
                self.assertIn("updated_at", favurl["category"])

            if "tags" in favurl and favurl["tags"]:
                for tag in favurl["tags"]:
                    self.assertIn("id", tag)
                    self.assertIn("user", tag)
                    self.assertIn("name", tag)
                    self.assertIn("created_at", tag)
                    self.assertIn("updated_at", tag)

    def assertFavUrlEqualsResponse(self, user, response):
        for favurl in response:
            favurl_obj = FavouriteUrl.objects.get(id=favurl["id"])
            self.assertEqual(user.id, favurl["user"])
            self.assertEqual(favurl_obj.user.id, favurl["user"])
            self.assertEqual(favurl_obj.title, favurl["title"])
            self.assertEqual(
                favurl_obj.created_at.strftime("%Y-%m-%d"),
                favurl["created_at"][0:10],
            )
            self.assertEqual(
                favurl_obj.updated_at.strftime("%Y-%m-%d"),
                favurl["updated_at"][0:10],
            )

            if favurl["category"]:
                category_obj = FavouriteCategory.objects.get(
                    id=favurl["category"]["id"]
                )
                self.assertEqual(category_obj.name, favurl["category"]["name"])
                self.assertEqual(
                    category_obj.created_at.strftime("%Y-%m-%d"),
                    favurl["category"]["created_at"][0:10],
                )
                self.assertEqual(
                    category_obj.updated_at.strftime("%Y-%m-%d"),
                    favurl["category"]["updated_at"][0:10],
                )

            for tag in favurl["tags"]:
                tag_obj = FavouriteTag.objects.get(id=tag["id"])
                self.assertEqual(tag_obj.name, tag["name"])
                self.assertEqual(
                    tag_obj.created_at.strftime("%Y-%m-%d"), tag["created_at"][0:10]
                )
                self.assertEqual(
                    tag_obj.updated_at.strftime("%Y-%m-%d"), tag["updated_at"][0:10]
                )

    def test_list_favourite_url_paginated_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(
            self.response_json["count"],
            FavouriteUrl.objects.filter(user=self.user).count(),
        )
        self.assertFavUrlInResponse(self.response_json["results"])
        self.assertFavUrlEqualsResponse(self.user, self.response_json["results"])

    def test_list_favourite_url_forbidden_given_not_logged_in(self):
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_gets_json()
        self.assertResponseForbidden()

    def test_list_search_by_title_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"title": self.favourite_url_2.title})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 1)
        self.assertEqual(
            self.response_json["results"][0]["title"], self.favourite_url_2.title
        )

    def test_list_search_by_url_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"url": self.favourite_url_1.url[:-1]})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 1)
        self.assertEqual(
            self.response_json["results"][0]["url"], self.favourite_url_1.url
        )

    def test_list_filter_by_category_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"category_name": self.favourite_url_1.category.name})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 1)
        self.assertEqual(
            self.response_json["results"][0]["category"]["name"],
            self.favourite_url_1.category.name,
        )

    def test_list_filter_by_tag_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"tag_name": self.favourite_url_1.tags.first().name})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 2)
        self.assertIn(
            self.response_json["results"][0]["id"],
            [self.favourite_url_1.id, self.favourite_url_2.id],
        )
        self.assertIn(
            self.response_json["results"][1]["id"],
            [self.favourite_url_1.id, self.favourite_url_2.id],
        )

    def test_list_filter_by_category_and_tag_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params(
            {
                "category_name": self.favourite_url_1.category.name,
                "tag_name": self.favourite_url_1.tags.first().name,
            }
        )
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 1)
        self.assertEqual(
            self.response_json["results"][0]["id"], self.favourite_url_1.id
        )

    def test_list_filter_by_created_after_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"created_after": timezone.now() - timedelta(days=1)})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 2)

    def test_list_filter_by_created_before_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"created_before": timezone.now()})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 2)

    def test_list_filter_by_updated_after_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"updated_after": timezone.now() - timedelta(days=1)})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 2)

    def test_list_filter_by_updated_before_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.given_query_params({"updated_before": timezone.now()})
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertEqual(self.response_json["count"], 2)

    def test_retrieve_given_user_success(self):
        self.given_logged_in_user(self.user)
        self.given_url(
            reverse("favouriteurl-detail", kwargs={"pk": self.favourite_url_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseSuccess()
        self.assertFavUrlInResponse([self.response_json])
        self.assertFavUrlEqualsResponse(self.user, [self.response_json])

    def test_retrieve_non_existing_id(self):
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-detail", kwargs={"pk": "123123"}))
        self.when_user_gets_json()
        self.assertResponseNotFound()

    def test_retrieve_forbidden_given_not_logged_in(self):
        self.given_url(
            reverse("favouriteurl-detail", kwargs={"pk": self.favourite_url_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseForbidden()

    def test_retrieve_not_found_given_other_user(self):
        self.given_logged_in_user(self.other_user)
        self.given_url(
            reverse("favouriteurl-detail", kwargs={"pk": self.favourite_url_1.pk})
        )
        self.when_user_gets_json()
        self.assertResponseNotFound()

    @patch("favourite_manager.models.requests.get")
    @patch("favourite_manager.models.BeautifulSoup")
    def test_create_success(self, mock_bs, mock_requests_get):
        new_fav_url = "https://facebook.com"
        new_fav_title = "Custom test title"
        mock_requests_get.return_value.status_code = 200
        mock_soup = mock_bs.return_value
        mock_soup.title.string = new_fav_title

        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(
            data={"url": new_fav_url, "title": "Use this title"}
        )
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteUrl.objects.filter(
                user=self.user, title="Use this title", url=new_fav_url
            ).count(),
            1,
        )

    @patch("favourite_manager.models.requests.get")
    @patch("favourite_manager.models.BeautifulSoup")
    def test_create_success_with_default_title(self, mock_bs, mock_requests_get):
        initial_valid_url_count = ValidUrl.objects.count()
        new_fav_url = "https://facebook.com"
        new_fav_title = "Custom test title"
        mock_requests_get.return_value.status_code = 200
        mock_soup = mock_bs.return_value
        mock_soup.title.string = new_fav_title

        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(data={"url": new_fav_url})
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteUrl.objects.filter(
                user=self.user, title=new_fav_title, url=new_fav_url
            ).count(),
            1,
        )
        self.assertEqual(initial_valid_url_count + 1, ValidUrl.objects.count())
        self.assertTrue(
            ValidUrl.objects.filter(url=new_fav_url, is_valid=True).exists()
        )

    def test_create_fail_with_is_valid_false_valid_url_object(self):
        initial_count = self.get_favourite_url_count()
        new_fav_url = "https://facebook.com"
        ValidUrl.objects.create(url=new_fav_url, title="random")
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(data={"url": new_fav_url})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, self.get_favourite_url_count())

    def test_create_success_with_is_valid_true_valid_url_object(self):
        new_fav_url = "https://facebook.com"
        ValidUrl.objects.create(url=new_fav_url, title="random", is_valid=True)
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(data={"url": new_fav_url})
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteUrl.objects.filter(
                user=self.user, title="random", url=new_fav_url
            ).count(),
            1,
        )

    def test_create_with_category_success(self):
        new_fav_url = "https://facebook.com"
        ValidUrl.objects.create(url=new_fav_url, title="random", is_valid=True)
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(
            data={"url": new_fav_url, "category": self.category.id}
        )
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteUrl.objects.filter(
                user=self.user, title="random", url=new_fav_url, category=self.category
            ).count(),
            1,
        )

    def test_create_with_tags_success(self):
        new_fav_url = "https://facebook.com"
        ValidUrl.objects.create(url=new_fav_url, title="random", is_valid=True)
        self.new_tag = self.given_a_favourite_tag(user=self.user, name="New Tag")
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(
            data={
                "url": new_fav_url,
                "category": self.category.id,
                "tags": [self.tag.id, self.new_tag.id],
            }
        )
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteUrl.objects.filter(
                user=self.user,
                title="random",
                url=new_fav_url,
                category=self.category,
                tags__in=[self.tag, self.new_tag],
            )
            .distinct()
            .count(),
            1,
        )

    def test_create_with_other_category_ignores(self):
        new_fav_url = "https://facebook.com"
        ValidUrl.objects.create(url=new_fav_url, title="random", is_valid=True)
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(
            data={
                "url": new_fav_url,
                "category": self.other_category.id,
                "tags": [self.other_tag.id],
            }
        )
        self.assertResponseCreated()
        self.assertEqual(
            FavouriteUrl.objects.filter(
                user=self.user, title="random", url=new_fav_url
            ).count(),
            1,
        )

    def test_create_forbidden_given_not_logged_in(self):
        initial_count = self.get_favourite_url_count()
        new_fav_url = "https://facebook.com"
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(data={"url": new_fav_url})
        self.assertResponseForbidden()
        self.assertEqual(initial_count, self.get_favourite_url_count())

    def test_create_bad_request_given_duplicate_url(self):
        initial_count = self.get_favourite_url_count()
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(data={"url": self.favourite_url_1.url})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, self.get_favourite_url_count())

    def test_create_bad_request_given_no_url(self):
        initial_count = self.get_favourite_url_count()
        self.given_logged_in_user(self.user)
        self.given_url(reverse("favouriteurl-list"))
        self.when_user_posts_and_gets_json(data={})
        self.assertResponseBadRequest()
        self.assertEqual(initial_count, self.get_favourite_url_count())
