from config.helpers import BaseTestCase
from django.core.exceptions import ValidationError

from favourite_manager.models import FavouriteUrl


class FavouriteCategoryTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.given_a_new_user()
        self.category = self.given_a_favourite_category(user=self.user)
        self.favourite_url1 = self.given_a_favourite_url(
            self.user, category=self.category
        )
        self.favourite_url2 = self.given_a_favourite_url(
            self.user, url="fav.com", category=self.category
        )
        self.other_user = self.given_a_new_user(username="other")
        self.other_category = self.given_a_favourite_category(user=self.other_user)

    def test_category_associated_urls_count_equals_real_count(self):
        self.assertEqual(self.category.associated_urls_count, 2)
        self.assertEqual(self.other_category.associated_urls_count, 0)


class FavouritetagTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.given_a_new_user()
        self.tag = self.given_a_favourite_tag(user=self.user)
        self.tag_2 = self.given_a_favourite_tag(user=self.user, name="tag2")
        self.favourite_url1 = self.given_a_favourite_url(
            self.user, tags=[self.tag, self.tag_2]
        )
        self.favourite_url2 = self.given_a_favourite_url(
            self.user, url="fav.com", tags=[self.tag]
        )
        self.other_user = self.given_a_new_user(username="other")
        self.other_tag = self.given_a_favourite_tag(user=self.other_user)

    def test_tag_associated_urls_count_equals_real_count(self):
        self.assertEqual(self.tag.associated_urls_count, 2)
        self.assertEqual(self.tag_2.associated_urls_count, 1)
        self.assertEqual(self.other_tag.associated_urls_count, 0)


class FavouriteUrlTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.given_a_new_user()
        self.other_user = self.given_a_new_user(username="other")
        self.other_tag = self.given_a_favourite_tag(user=self.other_user)
        self.other_category = self.given_a_favourite_category(user=self.other_user)

    def test_user_cannot_add_other_tags_on_save_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user)
        with self.assertRaises(ValidationError):
            fav_url.save(tags=[self.other_tag])

    def test_user_cannot_add_other_tags_on_add_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user)
        with self.assertRaises(ValidationError):
            fav_url.tags.add(self.other_tag)

    def test_user_cannot_add_other_tags_on_set_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user)
        with self.assertRaises(ValidationError):
            fav_url.tags.set([self.other_tag])

    def test_user_cannot_add_other_categories_on_save_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user)
        with self.assertRaises(ValidationError):
            fav_url.save(category=self.other_category)

    def test_user_cannot_add_other_categories_on_save_favourite_url(self):
        with self.assertRaises(ValidationError):
            FavouriteUrl.objects.create(
                user=self.user,
                url="tst.com",
                title="title",
                category=self.other_category,
            )
