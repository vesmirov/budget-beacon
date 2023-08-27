from django.contrib.auth import get_user_model
from rest_framework.generics import (get_object_or_404, ListCreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from users.permissions import AdminUserPermission, RegisteredUserPermission
from users.serializers import UserAdminSerializer, UserSerializer

User = get_user_model()


class UserListAPIView(ListCreateAPIView):
    model = User
    permission_classes = (AdminUserPermission,)
    serializer_class = UserAdminSerializer


class UserDetailAdminAPIView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = (AdminUserPermission,)
    serializer_class = UserAdminSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    model = User
    permission_classes = (RegisteredUserPermission,)
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, {'id': self.request.user.id})
        self.check_object_permissions(self.request, obj)

        return obj
