from django.urls import path


urlpatterns = [
    path('login/', ...),
    path('create/', ...),
    path('<str:id>/', ...),
]
