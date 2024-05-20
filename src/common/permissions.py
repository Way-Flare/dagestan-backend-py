from rest_framework.permissions import BasePermission


class IsAnonymousUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_anonymous)
