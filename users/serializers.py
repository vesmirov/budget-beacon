from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'telegram_id',
            'first_name',
            'last_name',
            'role',
            'is_staff',
            'date_joined',
        )
        read_only_fields = (
            'date_joined',
        )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'telegram_id',
            'username',
            'email',
            'first_name',
            'last_name',
        )
        read_only_fields = (
            'email',
            'telegram_id',
            'date_joined',
        )
