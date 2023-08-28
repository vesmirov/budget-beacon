from rest_framework.reverse import reverse_lazy

from users.models import UserRolesChoices
from utils.tests.api import BaseAPITestCase

LIST_USERS_ENDPOINT_NAME = 'users-list'
DETAIL_ADMIN_USER_ENDPOINT_NAME = 'users-detail-admin'
DETAIL_COMMON_USER_ENDPOINT_NAME = 'users-detail-common'


class AdminUserTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.setup_admin_user()

    def test_create_user(self):
        data = {
            "telegram_id": "355825262",
            "username": "common_user",
            "email": "evan.vesmirov@yandex.ru",
            "first_name": "Common",
            "last_name": "User",
            "role": UserRolesChoices.ADMIN,
            "is_staff": False
        }
        response = self.client.post(reverse_lazy(LIST_USERS_ENDPOINT_NAME), json=data)

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
