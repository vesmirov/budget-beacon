from typing import NamedTuple

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED

from users.models import UserRolesChoices
from utils.tests.api import BaseAPITestCase

LIST_USERS_ENDPOINT_NAME = 'users-list'
DETAIL_ADMIN_USER_ENDPOINT_NAME = 'users-detail-admin'
DETAIL_COMMON_USER_ENDPOINT_NAME = 'users-detail-common'

User = get_user_model()


class UserCreationCases(NamedTuple):
    case_name: str
    telegram_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_staff: bool


class AdminUserTestCase(BaseAPITestCase):
    USER_CREATION_SUCCESS_CASES = (
        UserCreationCases(
            case_name='Create admin user case',
            telegram_id='7777777777',
            username='admin_user',
            email='admin_user@example.com',
            first_name='Admin',
            last_name='User',
            role=UserRolesChoices.ADMIN,
            is_staff=True,
        ),
        UserCreationCases(
            case_name='Create common user case',
            telegram_id='7777777777',
            username='common_user',
            email='common_user@example.com',
            first_name='Common',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        ),
        UserCreationCases(
            case_name='Create unregistered user case',
            telegram_id='7777777777',
            username='unregistered_user',
            email='unregistered_user@example.com',
            first_name='Unregistered',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        ),
    )

    def setUp(self) -> None:
        self.setup_admin_user()

    def test_create_user(self):
        for case in self.USER_CREATION_SUCCESS_CASES:
            with self.subTest(case_name=case.case_name):
                response: Response = self.client.post(
                    reverse(LIST_USERS_ENDPOINT_NAME),
                    json={
                        'telegram_id': case.telegram_id,
                        'username': case.username,
                        'email': case.email,
                        'first_name': case.first_name,
                        'last_name': case.last_name,
                        'role': case.role,
                        'is_staff': case.is_staff,
                    }
                )
                self.assertEqual(response.status_code, HTTP_201_CREATED)
                self.assertIn('id', response.data)

                created_user = User.objects.filter(id=response.data['id'])
                self.assertTrue(created_user.exists())

                fields_to_check = ('telegram_id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
                for field in fields_to_check:
                    wanted_value = getattr(case, field)
                    actual_value = getattr(created_user, field)
                    self.assertEqual(
                        wanted_value,
                        actual_value,
                        msg=(
                            'Field value mismatch.'
                            f'field name: "{field}", '
                            f'wanted value: {wanted_value}, '
                            f'actual value: {actual_value}.'
                        ),
                    )

    def test_list_users(self):
        ...

    def test_retrieve_user(self):
        ...

    def test_delete_user(self):
        ...


class CommonUserTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.setup_common_user()

    def test_cannot_create_user(self):
        ...

    def test_cannot_list_users(self):
        ...

    def test_can_not_retrieve_other_user(self):
        ...

    def test_can_retrieve_only_himself(self):
        ...

    def test_cannot_delete_user(self):
        ...


class UnregisteredUserTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.setup_unregistered_user()

    def test_cannot_create_user(self):
        ...

    def test_cannot_list_users(self):
        ...

    def test_can_not_retrieve_any_user(self):
        ...

    def test_cannot_delete_user(self):
        ...
