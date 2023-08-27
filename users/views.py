from django.contrib.auth import get_user_model
from rest_framework.generics import (get_object_or_404, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny

from users.permissions import AdminUserPermission, RegisteredUserPermission
from users.serializers import UserAdminSerializer, UserSerializer

User = get_user_model()


class UserListAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AdminUserPermission,)
    serializer_class = UserAdminSerializer


class UserDetailAdminAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (AdminUserPermission,)
    serializer_class = UserAdminSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = (RegisteredUserPermission,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, {'id': self.request.user.id})
        self.check_object_permissions(self.request, obj)

        return obj


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    authentication_classes = (AllowAny,)
    serializer_class = UserSerializer
