from rest_framework import permissions

from .models import User

class OnlyAnon(permissions.BasePermission):
    """Only allow unauthenticated user"""

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class OnlyTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False

        return request.user.role == User.TUTOR


class OnlyLearner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False
        return request.user.role == User.LEARNER

class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.user, User):
            return False
        return request.user.role == User.ADMIN