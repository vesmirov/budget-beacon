from django.urls import path

from users.views import UserListAPIView, UserDetailAdminAPIView, UserDetailAPIView, UserRegisterAPIView

# Admin access
urlpatterns = [
    path('', UserListAPIView.as_view(), name='users-list'),
    path('<int:pk>/', UserDetailAdminAPIView.as_view(), name='users-detail'),
]

# Common access
urlpatterns += [
    path('account/', UserDetailAPIView.as_view(), name='user-detail'),
    path('sign-up/', UserRegisterAPIView.as_view(), name='user-register'),
]

