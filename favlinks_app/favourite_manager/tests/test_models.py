from config.helpers import BaseTestCase


class FavouriteUrlTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.given_a_new_user()
        self.other_user = self.given_a_new_user(username="other")
        self.other_tag = self.given_a_favourite_tag(user=self.other_user)
        self.other_category = self.given_a_favourite_category(user=self.other_user)

    def test_user_cannot_add_other_tags_on_save_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user, url="google.com")
        with self.assertRaises(ValueError):
            fav_url.save(tags=[self.other_tag])

    def test_user_cannot_add_other_tags_on_add_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user, url="google.com")
        with self.assertRaises(ValueError):
            fav_url.tags.add(self.other_tag)

    def test_user_cannot_add_other_tags_on_set_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user, url="google.com")
        with self.assertRaises(ValueError):
            fav_url.tags.set([self.other_tag])

    def test_user_cannot_add_other_categories_on_save_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user, url="google.com")
        with self.assertRaises(ValueError):
            fav_url.save(categories=[self.other_category])

    def test_user_cannot_add_other_categories_on_add_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user, url="google.com")
        with self.assertRaises(ValueError):
            fav_url.categories.add(self.other_category)

    def test_user_cannot_add_other_categories_on_set_favourite_url(self):
        fav_url = self.given_a_favourite_url(self.user, url="google.com")
        with self.assertRaises(ValueError):
            fav_url.categories.set([self.other_category])
