from rest_framework.permissions import BasePermission


class AdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        """Returns `True` if used is authenticated and admin. `False` otherwise"""
        return request.user.is_authenticated and request.user.is_admin()


class RegisteredUserPermission(BasePermission):
    def has_permission(self, request, view):
        """Returns `True` if used is authenticated and registered. `False` otherwise"""
        return request.user.is_authenticated and request.user.is_registered()
