from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model


class AuthTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(username="john", password="johnpassword")

    def test(self):
        client = Client()

        # Log in
        client.login(username="john", password="johnpassword")

        # Log out
        client.logout()
