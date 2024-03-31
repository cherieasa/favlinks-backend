from config.helpers import BaseTestCase
from rest_framework.reverse import reverse

from user_manager.models import User


class AuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.given_a_new_user(username="test")

    def assertInRegisterResponse(self, response):
        self.assertIn("id", response)
        self.assertIn("username", response)
        self.assertIn("email", response)

    def get_user_count(self):
        return User.objects.count()

    def given_register_payload(self, username, password, confirm_password):
        data = {
            "username": username,
            "password": password,
            "confirm_password": confirm_password,
        }
        return data

    def given_login_payload(self, username, password):
        data = {
            "username": username,
            "password": password,
        }
        return data

    def test_register_unique_username_created(self):
        new_username = "new"
        initial_user_count = self.get_user_count()
        self.given_url(reverse("auth-register"))
        data = self.given_register_payload(
            username=new_username, password="Test1234++", confirm_password="Test1234++"
        )
        self.when_user_posts_and_gets_json(data=data)
        self.assertResponseCreated()
        self.assertInRegisterResponse(self.response_json)
        self.assertTrue(User.objects.filter(username=new_username).exists())
        self.assertEqual(initial_user_count + 1, self.get_user_count())

    def test_register_duplicated_username_fails(self):
        initial_user_count = self.get_user_count()
        self.given_url(reverse("auth-register"))
        data = self.given_register_payload(
            username=self.user.username,
            password="Test1234++",
            confirm_password="Test1234++",
        )
        self.when_user_posts_and_gets_json(data=data)
        self.assertResponseBadRequest()
        self.assertEqual(initial_user_count, self.get_user_count())

    def test_register_nonmatching_password_fails(self):
        initial_user_count = self.get_user_count()
        new_username = "new"
        self.given_url(reverse("auth-register"))
        data = self.given_register_payload(
            username=new_username,
            password="Test1234++",
            confirm_password="Tes",
        )
        self.when_user_posts_and_gets_json(data=data)
        self.assertResponseBadRequest()
        self.assertEqual(initial_user_count, self.get_user_count())

    def test_entirely_numeric_password_fails(self):
        initial_user_count = self.get_user_count()
        new_username = "new"
        self.given_url(reverse("auth-register"))
        data = self.given_register_payload(
            username=new_username,
            password="12312312315244",
            confirm_password="12312312315244",
        )
        self.when_user_posts_and_gets_json(data=data)
        self.assertResponseBadRequest()
        self.assertEqual(initial_user_count, self.get_user_count())

    def test_short_password_fails(self):
        initial_user_count = self.get_user_count()
        new_username = "new"
        self.given_url(reverse("auth-register"))
        data = self.given_register_payload(
            username=new_username,
            password="#T4est1",
            confirm_password="#T4est1",
        )
        self.when_user_posts_and_gets_json(data=data)
        self.assertResponseBadRequest()
        self.assertEqual(initial_user_count, self.get_user_count())

    def test_common_password_fails(self):
        initial_user_count = self.get_user_count()
        new_username = "new"
        self.given_url(reverse("auth-register"))
        data = self.given_register_payload(
            username=new_username,
            password="Password12345",
            confirm_password="Password12345",
        )
        self.when_user_posts_and_gets_json(data=data)
        self.assertResponseBadRequest()
        self.assertEqual(initial_user_count, self.get_user_count())
