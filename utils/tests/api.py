from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase


from users.models import UserRolesChoices

User = get_user_model()


class BaseAPITestCase(TestCase):
    DEFAULT_PASSWORD = 'test-user-password-911'

    client_class = APIClient  # TODO: configure our own client

    def __init__(self, *args):
        super().__init__(*args)
        self.admin_user = None
        self.common_user = None
        self.unregistered_user = None

    def setup_admin_user(self, **kwargs) -> User:
        """Creates, saves and returns an admin user for the test."""
        data = {
            'telegram_id': '0123456789',
            'username': 'test_admin_user',
            'email': 'test_admin_user@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': self.DEFAULT_PASSWORD,
            'role': UserRolesChoices.ADMIN,
        }
        data.update(kwargs)

        user = User.objects.create_user(**data)
        self.admin_user = user

        return user

    def setup_common_user(self, **kwargs) -> User:
        """Creates, saves and returns a common user for the test."""
        data = {
            'telegram_id': '1234567890',
            'username': 'test_common_user',
            'email': 'test_common_user@example.com',
            'first_name': 'Common',
            'last_name': 'User',
            'password': self.DEFAULT_PASSWORD,
            'role': UserRolesChoices.REGISTERED,
        }
        data.update(kwargs)

        user = User.objects.create_user(**data)
        self.common_user = user

        return user

    def setup_unregistered_user(self, **kwargs) -> User:
        """Creates, saves and returns an unregistered user for the test."""
        data = {
            'telegram_id': '2345678901',
            'username': 'test_unregistered_user',
            'email': 'test_unregistered_user@example.com',
            'first_name': 'Unregistered',
            'last_name': 'User',
            'password': self.DEFAULT_PASSWORD,
            'role': UserRolesChoices.UNREGISTERED,
        }
        data.update(kwargs)

        user = User.objects.create_user(**data)
        self.unregistered_user = user

        return user

    def setup_users(self):
        """Creates and saves all the users for the test."""
        self.setup_admin_user()
        self.setup_common_user()
        self.setup_unregistered_user()
