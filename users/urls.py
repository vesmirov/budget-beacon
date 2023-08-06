from django.urls import include, path
from rest_framework.routers import DefaultRouter


user_router = DefaultRouter()
user_router.register(r'users', ..., basename='users')

urlpatterns = [
    path('', include(user_router.urls)),
]
