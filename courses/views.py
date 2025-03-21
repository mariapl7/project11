from django.http import HttpResponseForbidden
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from .models import Course,Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Разделение прав для разных действий в ViewSet.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]  # Создавать курсы могут только авторизованные
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]  # Список доступен всем авторизованным пользователям
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsAuthenticated, IsModerator]  # Модераторы могут редактировать и просматривать
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]  # Удалять могут только администраторы
        return super().get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


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
