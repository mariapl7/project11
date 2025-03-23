from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешение для проверки, является ли пользователь модератором.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsOwner(permissions.BasePermission):
    """
    Разрешение для проверки, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение для владельца объекта
        return obj.owner == request.user
