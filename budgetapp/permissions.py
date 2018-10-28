from rest_framework import permissions

from .utils.permissions import is_owner_or_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission that only allows owners of an object to view or edit it.
    Requires that the model have an `owner` field or property.
    """

    def has_object_permission(self, request, view, obj):
        return is_owner_or_admin(request.user, obj)
