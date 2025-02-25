from rest_framework import permissions

from account.models import User


class OnlyAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False
        return request.user.is_authenticated
