from typing import NamedTuple

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

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
            telegram_id='1111111111',
            username='admin_user',
            email='admin_user@example.com',
            first_name='Admin',
            last_name='User',
            role=UserRolesChoices.ADMIN,
            is_staff=True,
        ),
        UserCreationCases(
            case_name='Create common user case',
            telegram_id='2222222222',
            username='common_user',
            email='common_user@example.com',
            first_name='Common',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        ),
        UserCreationCases(
            case_name='Create unregistered user case',
            telegram_id='3333333333',
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
                    data={
                        'telegram_id': case.telegram_id,
                        'username': case.username,
                        'email': case.email,
                        'first_name': case.first_name,
                        'last_name': case.last_name,
                        'role': case.role,
                        'is_staff': case.is_staff,
                    }
                )
                self.assertEqual(
                    response.status_code,
                    HTTP_201_CREATED,
                    msg=f'status code mismatch.\nResponse body: {response.data}',
                )
                self.assertIn('id', response.data)

                created_user_queryset = User.objects.filter(id=response.data['id'])
                self.assertTrue(created_user_queryset.exists())

                created_user = created_user_queryset.first()
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
        User.objects.create(
            telegram_id='2222222222',
            username='common_user',
            email='common_user@example.com',
            first_name='Common',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        ).save()

        response = self.client.get(reverse(LIST_USERS_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_200_OK, msg='invalid status code')
        self.assertEqual(len(response.data), 2, msg='invalid amount of users in response')

    def test_retrieve_user(self):
        user = User.objects.create(
            telegram_id='2222222222',
            username='common_user',
            email='common_user@example.com',
            first_name='Common',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        )
        user.save()

        response = self.client.get(reverse(DETAIL_ADMIN_USER_ENDPOINT_NAME, args=(user.id,)))
        self.assertEqual(response.status_code, HTTP_200_OK, msg='invalid status code')
        self.assertIn('id', response.data, msg='user id is not represented in response')
        self.assertEqual(response.data['id'], user.id, msg='user instance cannot be retrieved')

    def test_can_retrieve_himself_via_common_endpoint(self):
        response = self.client.get(reverse(DETAIL_COMMON_USER_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_200_OK, msg='invalid status code')
        self.assertIn('id', response.data, msg='user id is not represented in response')
        self.assertEqual(response.data['id'], self.admin_user.id, msg='user instance cannot be retrieved')

    def test_delete_user(self):
        user = User.objects.create(
            telegram_id='2222222222',
            username='common_user',
            email='common_user@example.com',
            first_name='Common',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        )
        user.save()

        response = self.client.get(reverse(LIST_USERS_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_200_OK, msg='invalid status code')
        self.assertEqual(len(response.data), 2, msg='invalid amount of users in response')

        response = self.client.delete(reverse(DETAIL_ADMIN_USER_ENDPOINT_NAME, args=(user.id,)))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT, msg='invalid status code')

        response = self.client.get(reverse(LIST_USERS_ENDPOINT_NAME))
        self.assertEqual(len(response.data), 1, msg='user still in response')


class CommonUserTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.setup_common_user()

    def test_cannot_create_user(self):
        username = 'common_user'
        user_creation_data = {
            'telegram_id': '2222222222',
            'username': username,
            'email': 'common_user@example.com',
            'first_name': 'Common',
            'last_name': 'User',
            'role': UserRolesChoices.UNREGISTERED,
            'is_staff': False,
        }

        response = self.client.post(reverse(LIST_USERS_ENDPOINT_NAME), data=user_creation_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')
        self.assertFalse(User.objects.filter(username=username).exists())

    def test_cannot_list_users(self):
        response = self.client.get(reverse(LIST_USERS_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')

    def test_can_not_retrieve_other_user(self):
        response = self.client.get(reverse(DETAIL_ADMIN_USER_ENDPOINT_NAME, args=(self.common_user.id,)))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')

    def test_can_retrieve_himself_via_common_endpoint(self):
        response = self.client.get(reverse(DETAIL_COMMON_USER_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_200_OK, msg='invalid status code')
        self.assertIn('id', response.data, msg='user id is not represented in response')
        self.assertEqual(response.data['id'], self.common_user.id, msg='user instance cannot be retrieved')

    def test_cannot_delete_user(self):
        user = User.objects.create(
            telegram_id='2222222222',
            username='common_user',
            email='common_user@example.com',
            first_name='Common',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        )
        user.save()

        response = self.client.delete(reverse(DETAIL_ADMIN_USER_ENDPOINT_NAME, args=(user.id,)))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')
        self.assertTrue(User.objects.filter(id=user.id).exists(), msg='user was deleted by common user request')


class UnregisteredUserTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.setup_unregistered_user()

    def test_cannot_create_user(self):
        username = 'unregistered_user'
        user_creation_data = {
            'telegram_id': '2222222222',
            'username': username,
            'email': 'unregistered_user@example.com',
            'first_name': 'Unregistered',
            'last_name': 'User',
            'role': UserRolesChoices.UNREGISTERED,
            'is_staff': False,
        }

        response = self.client.post(reverse(LIST_USERS_ENDPOINT_NAME), data=user_creation_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')
        self.assertFalse(User.objects.filter(username=username).exists())

    def test_cannot_list_users(self):
        response = self.client.get(reverse(LIST_USERS_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')

    def test_can_not_retrieve_other_users(self):
        response = self.client.get(reverse(DETAIL_ADMIN_USER_ENDPOINT_NAME, args=(self.unregistered_user.id,)))
        self.assertEqual(
            response.status_code, HTTP_403_FORBIDDEN, msg='unregistered user can use admin retrieve endpoint')

    def test_can_not_retrieve_himself_via_common_endpoint(self):
        response = self.client.get(reverse(DETAIL_COMMON_USER_ENDPOINT_NAME))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')

    def test_cannot_delete_user(self):
        user = User.objects.create(
            telegram_id='2222222222',
            username='unregistered_user',
            email='unregistered_user@example.com',
            first_name='Unregistered',
            last_name='User',
            role=UserRolesChoices.UNREGISTERED,
            is_staff=False,
        )
        user.save()

        response = self.client.delete(reverse(DETAIL_ADMIN_USER_ENDPOINT_NAME, args=(user.id,)))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN, msg='invalid status code')
        self.assertTrue(User.objects.filter(id=user.id).exists(), msg='user was deleted by unregistered user request')
