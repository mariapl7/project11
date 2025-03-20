from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только пользователям, которые являются модераторами.
    """
    def has_permission(self, request, view):
        # Проверяем, состоит ли пользователь в группе 'moderators'
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ, если пользователь является владельцем объекта
        return obj.owner == request.user
