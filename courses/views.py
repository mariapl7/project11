from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwner, IsModerator  # Импортируем кастомные разрешения


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  # Общая проверка для аутентифицированных пользователей

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAuthenticated()]  # Любой аутентифицированный пользователь может смотреть курсы
        elif self.action == 'create':
            return [IsAuthenticated()]  # Только аутентифицированные могут создавать
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]  # Только владелец может изменять или удалять
        elif self.action == 'moderate':
            return [IsModerator()]  # Только модераторы могут выполнять модерацию
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Привязываем курс к текущему пользователю
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Ограничиваем доступ к курсам: пользователь может видеть только свои курсы
        if self.request.user.groups.filter(name='Модератор').exists():
            return Course.objects.all()  # Модераторы могут видеть все курсы
        return Course.objects.filter(owner=self.request.user)  # Пользователь видит только свои курсы


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]  # Общая проверка для аутентифицированных пользователей

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAuthenticated()]  # Любой аутентифицированный пользователь может смотреть уроки
        elif self.action == 'create':
            return [IsAuthenticated()]  # Только аутентифицированные могут создавать
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]  # Только владелец может изменять или удалять
        elif self.action == 'moderate':
            return [IsModerator()]  # Только модераторы могут выполнять модерацию
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Привязываем урок к текущему пользователю
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Ограничиваем доступ к урокам: пользователь может видеть только свои уроки
        if self.request.user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()  # Модераторы могут видеть все уроки
        return Lesson.objects.filter(owner=self.request.user)  # Пользователь видит только свои уроки
