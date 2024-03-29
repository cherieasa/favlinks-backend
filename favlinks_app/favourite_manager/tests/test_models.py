from config.helpers import BaseTestCase
from django.core.exceptions import ValidationError

from favourite_manager.models import FavouriteUrl


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
