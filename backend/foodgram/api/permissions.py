from rest_framework import permissions


class AdminOwnerOrReadOnly(
        permissions.BasePermission):
    """
    Разрешение на действия только для admin или автора,
    остальным доступ только на чтение.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or obj.author == request.user)
