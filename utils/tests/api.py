from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users.models import UserRolesChoices

User = get_user_model()


class BaseAPITestCase(APITestCase):
    DEFAULT_PASSWORD = 'test-user-password-911'

    @classmethod
    def setUpTestData(cls):
        cls.admin_user = None
        cls.common_user = None
        cls.unregistered_user = None

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

        self.client.force_authenticate(user=user)
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

        self.client.force_authenticate(user=user)
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

        self.client.force_authenticate(user=user)
        self.unregistered_user = user

        return user
