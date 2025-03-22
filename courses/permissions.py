from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешение для проверки, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Проверка, что пользователь является владельцем объекта
        return obj.owner == request.user  # Убедитесь, что объект имеет поле owner





class IsModerator(BasePermission):
    """
    Разрешение для проверки, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        # Проверяем, состоит ли пользователь в группе 'Moderators'
        return request.user.groups.filter(name='Moderators').exists()
