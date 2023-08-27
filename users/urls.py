from django.urls import path

from users.views import UserListAPIView, UserDetailAPIView


urlpatterns = [
    path('', UserListAPIView.as_view(), name='users-list'),
    path('<str:id>/', UserDetailAPIView(), name='users-detail'),
]

