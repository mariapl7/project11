from django.http import HttpResponseForbidden
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner  # Импортируем разрешение для владельца
from rest_framework.permissions import BasePermission


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Применяем разные разрешения в зависимости от действия.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут создавать курсы
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]  # Список доступен всем авторизованным пользователям
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator]  # Модераторы могут редактировать курсы
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]  # Удаление курсов — только для администраторов
        return super().get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Применяем разные разрешения в зависимости от действия.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут создавать уроки
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]  # Список доступен всем авторизованным пользователям
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator]  # Модераторы могут редактировать уроки
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]  # Удаление уроков — только для администраторов
        return super().get_permissions()


# Функции редактирования курсов и уроков с проверкой владельца и модератора

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
        return HttpResponseForbidden("Вы не можете редактировать этот курс.")
    # Логика редактирования курса
    return render(request, 'edit_course.html', {'course': course})


def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if lesson.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
        return HttpResponseForbidden("Вы не можете редактировать этот урок.")
    # Логика редактирования урока
    return render(request, 'edit_lesson.html', {'lesson': lesson})


class IsOwner(BasePermission):        # Разрешение для проверки владельца
    """
    Разрешение для проверки, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли текущий пользователь владельцем объекта
        return obj.owner == request.user  # Убедитесь, что объект имеет поле owner
